# Isolated-engine inventory: every registered event, script condition and view asset.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-mod-tests')
    config.save_persistent=False
init 1000 python:
    import sys,types
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_gate_splash'
    state=types.ModuleType('ssct_gate_probe')
    state.phase=0
    sys.modules[state.__name__]=state
    def _ssct_gate_export():
        import importlib.util,json,os,functools
        from saga import step
        from saga.enum import dow,tod
        def module(name):
            spec=importlib.util.spec_from_file_location(name,os.path.join(config.basedir,name+'.py'))
            result=importlib.util.module_from_spec(spec)
            sys.modules[name]=result
            spec.loader.exec_module(result)
            return result
        parser=module('gate_catalogue')
        screen_parser=module('screen_catalogue')
        runtime=module('gate_runtime')
        guard=module('ssct_replay_guard')
        options_path=os.path.join(config.basedir,'gate_probe_options.json')
        options=json.load(open(options_path,encoding='utf8')) if os.path.exists(options_path) else {}
        requested_gate_ids=options.get('gate_ids',[])
        requested_branch_offsets=options.get('branch_offsets',[])
        if options.get('rpy_source_roots'):
            source_parser=module('rpy_gate_catalogue')
            import renpy.parser as rpy_parser
            errors_before=list(rpy_parser.parse_errors)
            exception_before=renpy.game.exception_info
            def parse_source(filename,text):
                rpy_parser.parse_errors[:]=[]
                nodes=rpy_parser.parse(filename,text,1)
                if nodes is None or rpy_parser.parse_errors:
                    raise ValueError('\n'.join(str(error) for error in rpy_parser.parse_errors))
                return nodes
            try:
                source_report=source_parser.crawl_sources(options['rpy_source_roots'],parse_source)
            finally:
                rpy_parser.parse_errors[:]=errors_before
                renpy.game.exception_info=exception_before
            source_report['engine_version']=config.version
            source_report['source_fingerprints']=options.get('source_fingerprints',{})
            with open(os.path.join(config.basedir,'rpy_gate_inventory.json'),'w',encoding='utf8') as stream:
                json.dump(source_report,stream,ensure_ascii=False,indent=2)
            if options.get('source_only'):return
        catalogues=_ssct_completion_catalogues()
        if options.get('loaded_snapshot_only'):
            import hashlib
            snapshot_parser=module('native_state_snapshot')
            saves=[os.path.join(config.savedir,name) for name in os.listdir(config.savedir)
                if name.startswith('quick-6-') and name.endswith('.save')]
            if len(saves)!=1:raise ValueError('Ambiguous loaded generated save')
            result={'version':config.version,'baseline_sha256':hashlib.sha256(open(saves[0],'rb').read()).hexdigest(),
                'source_fingerprints':options.get('source_fingerprints',{}),
                'saved_day':saga.time.date,'saved_tick':saga.time.now,
                'camera':getattr(saga.camera.what,'ref',None),
                'snapshot':snapshot_parser.NativeStateSnapshot(catalogues).capture(catalogues),
                'native_postconditions':{kind+'.'+entity.ref:guard.stored_facts(entity,ignored=('when','where','plan'))
                    for kind,catalogue in catalogues.items() if kind in ('cast','prop','flow','sets') for entity in catalogue},
                'routes':ssct_perfect_generation['routes'],
                'scope':'Fresh native quick-6 load; stored facts only; not a sequential execution reference'}
            with open(os.path.join(config.basedir,'loaded_generated_state.json'),'w',encoding='utf8') as stream:
                json.dump(result,stream,ensure_ascii=False,indent=2)
            return
        from saga import zone
        catalogues['zone']=zone
        gates=[]
        functions=[]
        native_predicates={'builtins.getattr':__import__('builtins').getattr,'builtins.len':__import__('builtins').len}
        seen=set()
        def unwrap(callback):
            return parser.unwrap_callback(callback)[0]
        for node in step:
            for index,(callback,requirements,mutex,weight) in enumerate(getattr(node,'pool',())):
                function=unwrap(callback)
                for value in getattr(function,'__globals__',{}).values():
                    if parser.admitted_read_protocol(value):
                        native_predicates[getattr(value,'__module__','')+'.'+getattr(value,'__name__','')]=value
                functions.append(function)
                gates.append({'id':node.ref+':'+str(index),'source':getattr(function,'__module__','')+'.'+getattr(function,'__name__',repr(function)),
                    'requirements':[(name,parser.literal(value)) for name,value in sorted(requirements)],
                    'weight':weight,'mutex':repr(mutex),'analysis':parser.branch_inventory(callback,catalogues,saga.time,
                        {key:value for key,value in requirements if key in getattr(callback,'_req',())}),
                    'dependencies':guard.catalogue_dependencies(function,catalogues),
                    'status':'inventory_only_not_validated'})
        # Bind ctx from actual registered observers, never from a node name.
        # Flow forwards send to its current step; Step exposes its own pool.
        for observer in sorted(saga.event.crowd,key=lambda item:(type(item).__module__,item.ref)):
            node=getattr(observer,'step',observer)
            for index,(callback,requirements,mutex,weight) in enumerate(getattr(node,'pool',())):
                function=unwrap(callback)
                event,provenance,missing=parser.concrete_event_defaults(callback,requirements,saga.time)
                gates.append({'id':'active:'+getattr(observer,'ref','unknown')+':'+str(index),
                    'observer':parser.literal(observer),'node':getattr(node,'ref',None),
                    'source':getattr(function,'__module__','')+'.'+getattr(function,'__name__',repr(function)),
                    'requirements':[(name,parser.literal(value)) for name,value in sorted(requirements)],
                    'event_input':{key:parser.literal(value) for key,value in event.items()},
                    'event_input_provenance':provenance,'missing_event_inputs':missing,
                    'weight':weight,'mutex':repr(mutex),
                    'analysis':parser.branch_inventory(callback,catalogues,saga.time,
                        {key:value for key,value in event.items() if key in getattr(callback,'_req',())},
                        observer_context=observer,
                        clock_bindings=[key for key,origin in provenance.items() if origin=='explicit_test_input_from_native_clock']),
                    'dependencies':guard.catalogue_dependencies(function,catalogues),
                    'status':'active_observer_binding_not_response_validated'})
        # Include shared native prerequisite helpers, not only numbered quests.
        while functions:
            function=unwrap(functions.pop())
            code=getattr(function,'__code__',None)
            if code is None or id(function) in seen:continue
            seen.add(id(function))
            for name in code.co_names:
                helper=unwrap(function.__globals__.get(name))
                if not callable(helper) or not getattr(helper,'__module__','').startswith('saga.logic.'):
                    continue
                if id(helper) not in seen:
                    functions.append(helper)
                    helper_id=getattr(helper,'__module__','')+'.'+getattr(helper,'__name__',name)
                    if any(row['id']=='helper:'+helper_id for row in gates):continue
                    gates.append({'id':'helper:'+helper_id,'source':helper_id,'requirements':[],
                        'analysis':parser.branch_inventory(helper,catalogues,saga.time),
                        'dependencies':guard.catalogue_dependencies(helper,catalogues),
                        'status':'inventory_only_not_validated'})
        conditions=[]
        for statement in renpy.game.script.all_stmts:
            entries=[]
            if isinstance(statement,renpy.ast.If):entries=[(expr,'if') for expr,block in statement.entries]
            elif isinstance(statement,renpy.ast.Menu):entries=[(expr,caption) for caption,expr,block in statement.items if expr]
            for expression,kind in entries:
                conditions.append({'file':str(statement.filename),'line':statement.linenumber,'kind':str(kind),
                    'expression':str(expression),'status':'inventory_only_not_validated'})
        import saga.display.view as native_view
        assets=[]
        for art,(plan,defs,tags) in native_view.cache.items():
            for entity,variants,part,active,dependencies in plan:
                assets.append({'art':art,'entity':parser.literal(entity),'part':repr(part),'active':bool(active),
                    'dependencies':[parser.literal(value) for value in (dependencies or ())],
                    'variants':[{'include':sorted(inc or ()),'goal':goal,'exclude':sorted(exc or ()),'path':str(path)} for inc,goal,exc,path in variants],
                    'status':'inventory_only_not_validated'})
        scenarios=parser.temporal_scenarios(len(tuple(dow)),len(tuple(tod)))
        scalar_facts={}
        for kind,catalogue in catalogues.items():
            for entity in catalogue:
                for name,value in getattr(entity,'__dict__',{}).items():
                    if type(value) in (str,int,float,bool,type(None)):
                        scalar_facts[kind+'.'+entity.ref+'.'+name]=value
        clock_before=saga.time.now
        witnesses=[]
        # A targeted batch still retains the complete syntax inventory. Do not
        # spend every batch solving unrelated handlers; explicitly retain them
        # as untested, never as passed or unreachable.
        for row in gates:
            if requested_gate_ids and row['id'] not in requested_gate_ids:
                row['parameter_scope']='not_requested_in_this_batch'
                for branch in row['analysis']['branches']:
                    branch['native_predicates']=[]
                    branch['scalar_witnesses']=[]
                    branch['prerequisite_search']={side:{'status':'not_requested_in_this_batch'}
                        for side in ('true','false')}
        try:
            for scenario in scenarios:
                saga.time.now=scenario['tick']
                facts=dict(scalar_facts)
                facts.update({'time.date':saga.time.date,'time.now':saga.time.now})
                for row in gates:
                    if row.get('parameter_scope')=='not_requested_in_this_batch':continue
                    for branch in row['analysis']['branches']:
                        branch.setdefault('native_predicates',[]).append(dict(
                            runtime.observe_chain(branch,dict(catalogues,time=saga.time,event=saga.event),native_predicates),
                            temporal_tick=scenario['tick']))
                witnesses.append((scenario['tick'],facts))
            for row in gates:
                if row.get('parameter_scope')=='not_requested_in_this_batch':continue
                for branch in row['analysis']['branches']:
                    branch['scalar_witnesses']=parser.branch_witnesses(branch['expression'],witnesses)
                    branch['prerequisite_search']={}
                    for target in (True,False):
                        outcome=None
                        for identity,facts in witnesses:
                            saga.time.now=identity
                            attempt=runtime.solve_parameter_prerequisites(branch,dict(catalogues,time=saga.time,event=saga.event),native_predicates,target)
                            if attempt['status']=='parameter_witness':
                                outcome=dict(attempt,temporal_tick=identity)
                                saga.time.now=identity
                                outcome['native_witness']=runtime.verify_scalar_witness(branch,attempt,target,
                                    dict(catalogues,time=saga.time,event=saga.event),native_predicates)
                                break
                            if outcome is None or attempt['status']=='unresolved':outcome=attempt
                            if attempt['status'] in ('unresolved','budget_exhausted'):break
                        branch['prerequisite_search'][str(target).lower()]=outcome
        finally:
            saga.time.now=clock_before
        # Parameter-driven native dispatch. Reconstruct a disposable current-
        # engine world for each case, so one callback cannot taint another.
        # No map navigation, button walk or dialogue replay is performed.
        from renpy.rollback import RollbackLog
        import native_branch_trace
        import native_script_continuation
        import native_state_snapshot
        parameter_responses=[]
        options_path=os.path.join(config.basedir,'gate_probe_options.json')
        options=json.load(open(options_path,encoding='utf8')) if os.path.exists(options_path) else {}
        parameter_offset=options.get('parameter_offset',0)
        parameter_budget=options.get('parameter_limit',16)
        requested_gate_ids=options.get('gate_ids',[])
        parameter_index=0
        checkpoint_path=os.path.join(config.basedir,'parameter_gate_checkpoints.jsonl')
        open(checkpoint_path,'w',encoding='utf8').close()
        def checkpoint(case,phase):
            keys=('gate','offset','target','temporal_tick','parameter_index','native_menu_inputs',
                'status','error','target_branch_observed','target_entry_observed','native_task_completed','pending_native_tasks',
                'pending_native_events')
            record={key:case[key] for key in keys if key in case}
            record['phase']=phase
            record['script_results']=[{key:receipt[key] for key in ('label','status','reason','details') if key in receipt}
                for receipt in case.get('native_script_continuations',())]
            with open(checkpoint_path,'a',encoding='utf8') as stream:
                stream.write(json.dumps(record,ensure_ascii=False)+'\n')
        for row in gates:
            if not row['id'].startswith('active:'):continue
            if requested_gate_ids and row['id'] not in requested_gate_ids:continue
            test_branches=list(row['analysis']['branches'])
            if requested_branch_offsets:
                test_branches=[branch for branch in test_branches if branch['offset'] in requested_branch_offsets]
                if not test_branches:continue
            if not test_branches:
                native_node=getattr(step,row['node'])
                native_callback=unwrap(native_node.pool[int(row['id'].rsplit(':',1)[1])][0])
                test_branches.append({'entry_only':True,'offset':None,
                    'module':native_callback.__module__,
                    'code_identity_sha256':parser.code_identity(native_callback.__code__),
                    'expression':{'kind':'literal','value':True},'prerequisites':[],'prior_effects':[],
                    'prerequisite_search':{'true':{'status':'parameter_witness','changes':{},
                        'temporal_tick':clock_before},'false':None}})
            for branch in test_branches:
                for target in (True,False):
                    witness=branch['prerequisite_search'][str(target).lower()]
                    if witness is None or witness.get('status')!='parameter_witness':continue
                    case={'gate':row['id'],'offset':branch['offset'],'target':target,
                        'temporal_tick':witness['temporal_tick'],'native_response_validated':False}
                    case['parameter_index']=parameter_index
                    parameter_index+=1
                    if not parameter_offset<=case['parameter_index']<parameter_offset+parameter_budget:
                        case['status']='not_in_requested_parameter_segment'
                        parameter_responses.append(case)
                        continue
                    template=dict(case)
                    plans=[{}]
                    tested_plans=set()
                    while plans and len(tested_plans)<16:
                        input_plan=plans.pop(0)
                        identity=native_script_continuation.plan_identity(input_plan)
                        if identity in tested_plans:continue
                        tested_plans.add(identity)
                        case=dict(template,native_menu_inputs=input_plan)
                        checkpoint(case,'started')
                        backup=renpy.python.StoreBackup()
                        contexts,log=renpy.game.contexts,renpy.game.log
                        persistent_before=renpy.game.persistent
                        persistent_bindings=[]
                        seen_counts={key:getattr(renpy.game,key) for key in ('seen_translates_count','new_translates_count')
                            if hasattr(renpy.game,key)}
                        random_state=renpy.random.getstate()
                        try:
                            renpy.python.clean_stores()
                            renpy.execute_default_statement(True)
                            renpy.game.persistent=__import__('copy').deepcopy(persistent_before)
                            store.persistent=renpy.game.persistent
                            namespaces=[vars(module) for module in tuple(sys.modules.values()) if isinstance(module,types.ModuleType)]
                            namespaces.extend(unwrap(entry[0]).__globals__ for native_node in step
                                for entry in getattr(native_node,'pool',()) if hasattr(unwrap(entry[0]),'__globals__'))
                            persistent_bindings=native_script_continuation.replace_persistent_aliases(
                                namespaces,persistent_before,renpy.game.persistent)
                            renpy.game.contexts=[renpy.execution.Context(True,clear=True)]
                            renpy.game.log=RollbackLog()
                            _ssct_perfect_construct()
                            saga.time.now=witness['temporal_tick']
                            _ssct_perfect_schedule()
                            # Test inputs alter the already constructed world,
                            # not new-game mode or production generation.
                            native_script_continuation.apply_script_parameters(renpy,input_plan.get('__parameters__',{}))
                            current=_ssct_completion_catalogues()
                            current['zone']=zone
                            observer_ref=row['observer'].get('ref')
                            observer=next((item for item in saga.event.crowd if getattr(item,'ref',None)==observer_ref
                                and parser.literal(item)==row['observer']),None)
                            node=getattr(observer,'step',observer)
                            index=int(row['id'].rsplit(':',1)[1])
                            if observer is None or getattr(node,'ref',None)!=row['node']:
                                case['status']='observer_context_unavailable'
                            else:
                                callback,requirements,mutex,weight=node.pool[index]
                                function=unwrap(callback)
                                if parser.code_identity(function.__code__)!=branch['code_identity_sha256']:
                                    case['status']='callback_source_mismatch'
                                elif row['missing_event_inputs']:
                                    case['status']='event_requires_concrete_input'
                                else:
                                    event,provenance,missing=parser.concrete_event_defaults(callback,requirements,saga.time)
                                    case['event_input']={key:parser.literal(value) for key,value in event.items()}
                                    case['event_input_provenance']=provenance
                                    state_snapshot=native_state_snapshot.NativeStateSnapshot(current)
                                    def observe():
                                        snapshot=state_snapshot.capture(current)
                                        snapshot['clock']={name:parser.literal(getattr(saga.time,name))
                                            for name in ('now','date','dow','tod')}
                                        return snapshot
                                    def invoke():
                                        saga.event.emit(event)
                                        native_event=saga.event.queue[-1]
                                        candidates=list(saga.event.find(native_event))
                                        selected=[entry for entry in candidates if entry[1] is observer
                                            and parser.code_identity(unwrap(entry[3]).__code__)==branch['code_identity_sha256']]
                                        if len(selected)!=1:raise ValueError('Native target handler is not uniquely eligible')
                                        # Run the actual native Task continuation for
                                        # this gate, not unrelated GUI listeners.
                                        # Whole-dispatch ordering stays unverified.
                                        from saga.event import Task
                                        saga.event.queue=renpy.revertable.RevertableList()
                                        saga.event.stack=renpy.revertable.RevertableList([Task(*selected[0][1:])])
                                        saga.event.locks=renpy.revertable.RevertableSet()
                                        # Event.next normally initializes these when
                                        # it builds a fresh stack from the queue.
                                        # A selected-handler stack must do the same;
                                        # otherwise Event.call reuses a stale return
                                        # and silently skips the native script.
                                        dispatch_globals=saga.event.next.__func__.__globals__
                                        dispatch_globals['dynamic'](_choice=renpy.revertable.RevertableList())
                                        store._return=dispatch_globals['null']
                                        case['dispatch_scope']='selected_initial_handler_then_native_queue_order'
                                        case['other_candidate_count']=len(candidates)-1
                                        case['native_script_continuations']=[]
                                        for continuation_index in range(64):
                                            try:
                                                saga.event.next()
                                                case['native_task_completed']=not bool(saga.event.stack)
                                                case['pending_native_tasks']=len(saga.event.stack)
                                                case['pending_native_events']=len(saga.event.queue)
                                                if not saga.event.stack and not saga.event.queue:
                                                    case['native_queue_drained']=True
                                                    break
                                            except renpy.game.CallException as transfer:
                                                response=native_script_continuation.ScriptContinuation(renpy,inputs=input_plan).run(
                                                    transfer.label,transfer.args,transfer.kwargs)
                                                actual_return=response.get('value')
                                                receipt=dict(response,label=transfer.label)
                                                if response['status']=='native_script_returned':receipt['value']=parser.literal(actual_return)
                                                case['native_script_continuations'].append(receipt)
                                                if response['status']!='native_script_returned':
                                                    raise ValueError('Native script continuation requires unresolved input or adapter')
                                                store._return=actual_return
                                        else:raise ValueError('Native task/queue continuation budget exhausted')
                                    # Saved-world proposals cannot be reused as
                                    # current-world solutions: native setup may
                                    # choose new seeds or change dependencies.
                                    # Solve after setup/scheduling and immediately
                                    # before executing the current gate.
                                    execution_roots=dict(current,time=saga.time,event=saga.event)
                                    execution_witness=runtime.solve_parameter_prerequisites(
                                        branch,execution_roots,native_predicates,target)
                                    case['baseline_witness']=witness
                                    case['execution_witness']=execution_witness
                                    if execution_witness.get('status')!='parameter_witness':
                                        case.update(status='current_prerequisite_unresolved')
                                    else:
                                        case.update(runtime.execute_parameter_case(branch,execution_witness,target,
                                            execution_roots,native_predicates,invoke,
                                            native_branch_trace.NativeBranchTrace(),observe))
                        except Exception as error:
                            case.update(status='parameter_case_error',error={'type':type(error).__name__,'message':str(error)})
                        finally:
                            renpy.game.contexts,renpy.game.log=contexts,log
                            native_script_continuation.restore_persistent_aliases(persistent_bindings)
                            renpy.game.persistent=persistent_before
                            for key,value in seen_counts.items():setattr(renpy.game,key,value)
                            backup.restore()
                            renpy.random.setstate(random_state)
                        parameter_responses.append(case)
                        checkpoint(case,'finished')
                        plans.extend(native_script_continuation.expand_menu_plans(
                            input_plan,case.get('native_script_continuations',())))
                    if plans:
                        parameter_responses.append(dict(template,status='native_menu_plan_budget',
                            pending_plans=plans,native_response_validated=False))
        import hashlib
        baseline_files=[os.path.join(config.savedir,name) for name in os.listdir(config.savedir)
            if name.startswith('quick-6-') and name.endswith('.save')]
        if len(baseline_files)!=1:raise ValueError('Ambiguous native baseline save')
        result={'version':config.version,'saved_day':saga.time.date,'saved_tick':saga.time.now,
            'source_fingerprints':options.get('source_fingerprints',{}),
            'baseline_sha256':hashlib.sha256(open(baseline_files[0],'rb').read()).hexdigest(),
            'gates':gates,'script_conditions':conditions,'view_assets':assets,
            'parameter_native_responses':parameter_responses,
            'parameter_segment':{'offset':parameter_offset,'limit':parameter_budget,'candidate_count':parameter_index,
                'gate_ids':requested_gate_ids,'branch_offsets':requested_branch_offsets},
            'screen_syntax':screen_parser.screen_inventory(__import__('renpy.display.screen',fromlist=['screens']).screens),
            'temporal_scenarios':scenarios,
            'acceptance':{'validation_mode':'gate_only','route_endpoint_validation_required':False,
                'all_gates_passed':False,'unknown_branches':sum(not branch['supported'] for row in gates for branch in row['analysis']['branches']),
                'prerequisite_statuses':dict(__import__('collections').Counter(
                    outcome['status'] for row in gates for branch in row['analysis']['branches']
                    for outcome in branch['prerequisite_search'].values())),
                'native_predicate_statuses':dict(__import__('collections').Counter(
                    observation['status'] for row in gates for branch in row['analysis']['branches']
                    for observation in branch['native_predicates'])),
                'scope':'Inventory, not completed prerequisites or native interaction acceptance'}}
        assert saga.time.date==1, 'Generated save must start on day one'
        with open(os.path.join(config.basedir,'perfect_gate_inventory.json'),'w',encoding='utf8') as f:
            json.dump(result,f,indent=2,ensure_ascii=False)
        with open(os.path.join(config.basedir,'perfect_gate_inventory.md'),'w',encoding='utf8') as f:
            f.write(parser.render_inventory(result))
    def _ssct_gate_tick(kind):
        state=sys.modules['ssct_gate_probe']
        if kind in ('corp','gate'):renpy.end_interaction(None)
        elif state.phase==0 and kind=='main_menu':
            state.phase=1
            renpy.load('quick-6')
        elif state.phase==1 and kind=='nav':
            state.phase=2
            try:
                _ssct_gate_export()
            except Exception:
                import traceback,os
                with open(os.path.join(config.basedir,'gate_probe_failure.txt'),'w',encoding='utf8') as f:
                    f.write(traceback.format_exc())
            renpy.quit(save=False)
    def _ssct_gate_hook(original,kind):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_gate_tick',kind=kind,_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'gate_probe'))
        hook.__wrapped__=original
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','corp','gate'):screen.function=_ssct_gate_hook(screen.function,name)
label ssct_gate_splash:
    return
screen ssct_gate_tick(kind):
    timer .2 repeat True action Function(_ssct_gate_tick,kind)
