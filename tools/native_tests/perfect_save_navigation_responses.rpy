# Isolated native navigation responses. No teleportation to inaccessible rooms.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-mod-tests')
    config.save_persistent=False
init 1000 python:
    import sys,types,os,json,time
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_navigation_probe_splash'
    state=types.ModuleType('ssct_navigation_probe')
    state.phase=0
    state.rows=[]
    state.pending=[]
    state.seen=set()
    state.labels=[]
    state.cases=0
    state.clock_inputs=[]
    state.temporal_exits=[]
    state.unhandled_controls={}
    state.current_path=[]
    state.is_replay=False
    state.world_variants={}
    state.surface_worlds={}
    import native_branch_trace
    import native_wallet_protocol
    import ssct_replay_guard
    state.tracer=native_branch_trace.NativeBranchTrace()
    state.run_started=time.monotonic()
    sys.modules[state.__name__]=state
    def _ssct_navigation_serial(value):
        from collections.abc import Mapping
        if value is None or isinstance(value,(str,bool,int,float)):return value
        if isinstance(value,Mapping):return {key:_ssct_navigation_serial(item) for key,item in value.items()}
        if isinstance(value,(tuple,list,set,frozenset)):return [_ssct_navigation_serial(item) for item in value]
        return {'type':type(value).__module__+'.'+type(value).__name__,'ref':getattr(value,'ref',None)}
    def _ssct_navigation_write(status,error=None):
        state=sys.modules['ssct_navigation_probe']
        result={'version':config.version,'status':status,'tick':getattr(state,'tick',None),
            'rows':state.rows,'pending':state.pending,'seen':sorted(state.seen),
            'error':error,'active':getattr(state,'active',None),'labels':state.labels[-40:],
            'mode':renpy.get_mode(),'script_statement':str(renpy.game.context().current),
            'dialogue':getattr(renpy.get_screen('say'),'scope',{}).get('what'),
            'baseline_sha256':getattr(state,'baseline_sha256',None),
            'clock_inputs':state.clock_inputs,
            'include_interactions':getattr(state,'include_interactions',False),
            'temporal_exits':state.temporal_exits,
            'unhandled_controls':state.unhandled_controls,
            'baseline_slot':getattr(state,'baseline_slot',None),
            'probe_sha256':getattr(state,'probe_sha256',None),
            'probe_dependencies':getattr(state,'probe_dependencies',{}),
            'source_difference':getattr(state,'source_difference',None),
            'failed_branch_trace':getattr(state,'failed_branch_trace',None),
            'seed_case':getattr(state,'seed_case',None),
            'unexplored_world_variants':state.world_variants,
            'surface_worlds':state.surface_worlds,
            'replay_pending':getattr(state,'replay_pending',[]),
            'diagnosed_recovery':getattr(state,'recovered_failure',None),
            'place_program_retirements':_ssct_navigation_serial(getattr(store,'ssct_perfect_generation',{}).get('completed_enter_programs',[])),
            'all_gates_passed':False,'scope':'Actual rendered navigation and enabled interaction inputs with native branch observations; unsupported controls, unexplored state variants, unvisited branches and semantic postconditions remain unverified'}
        with open(os.path.join(config.basedir,'perfect_navigation_responses.json'),'w',encoding='utf8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
    def _ssct_navigation_label(name,abnormal):
        state=sys.modules['ssct_navigation_probe']
        state.labels.append(name)
    config.label_callbacks.append(_ssct_navigation_label)
    def _ssct_navigation_sensitivity(node):
        predicate=getattr(node,'is_sensitive',None)
        return bool(predicate()) if callable(predicate) else None
    def _ssct_navigation_called_screen():
        # Read only the literal native call-screen statement, never eval it.
        import re
        statement=renpy.game.script.namemap.get(renpy.game.context().current)
        match=re.match(r'call\s+screen\s+([A-Za-z_]\w*)\s*(?:\(|$)',getattr(statement,'line',''))
        if match:
            if match[1] in ('use','nav','choice'):return None,None
            screen=renpy.get_screen(match[1])
            if screen is not None:return match[1],screen
        return None,None
    def _ssct_navigation_input_screen():
        name,screen=_ssct_navigation_called_screen()
        return screen or renpy.get_screen('use') or renpy.get_screen('nav')
    def _ssct_navigation_controls():
        screen=_ssct_navigation_input_screen()
        if screen is None:raise ValueError('Native navigation screen missing')
        nodes=[]
        screen.visit_all(nodes.append)
        from collections.abc import Mapping
        return [(node,node.clicked) for node in nodes
            if isinstance(getattr(node,'clicked',None),Emit) and _ssct_navigation_sensitivity(node) is True
            and isinstance(node.clicked.value,Mapping)]
    def _ssct_navigation_choices():
        screen=renpy.get_screen('choice')
        if screen is None:return []
        nodes=[]
        screen.visit_all(nodes.append)
        return [(index,item) for index,item in enumerate(screen.scope.get('items',()))
            if any(getattr(node,'clicked',None) is item.action and _ssct_navigation_sensitivity(node) is True for node in nodes)]
    def _ssct_navigation_returns():
        screen=_ssct_navigation_input_screen()
        if screen is None:return []
        nodes=[]
        screen.visit_all(nodes.append)
        return [node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Return) and _ssct_navigation_sensitivity(node) is True]
    def _ssct_navigation_signature(values):
        return json.dumps(_ssct_navigation_serial(values),sort_keys=True,ensure_ascii=False)
    def _ssct_navigation_surface():
        screen=_ssct_navigation_input_screen()
        if screen is None:return []
        nodes=[]
        screen.visit_all(nodes.append)
        surface=[]
        for node in nodes:
            action=getattr(node,'clicked',None)
            sensitivity=_ssct_navigation_sensitivity(node)
            if action is None or sensitivity is False:continue
            if isinstance(action,(Emit,Return)):
                descriptor=(type(action).__name__,_ssct_navigation_serial(action.value))
            else:
                function=getattr(action,'callable',action)
                descriptor=(type(action).__module__+'.'+type(action).__name__,
                    getattr(function,'__module__',None),getattr(function,'__qualname__',None),
                    _ssct_navigation_serial(getattr(action,'args',())),
                    _ssct_navigation_serial(getattr(action,'kwargs',{})))
            surface.append(_ssct_navigation_signature((sensitivity,descriptor)))
        return sorted(surface)
    def _ssct_navigation_context():
        if renpy.get_screen('choice'):
            state=sys.modules['ssct_navigation_probe']
            root=next((item.get('event_signature',item.get('target')) for item in state.current_path if item['protocol']=='interaction'),None)
            return 'choice|'+str(root)+'|'+saga.camera.what.ref+'|'+str(renpy.game.context().current)+'|'+str([(i,item.caption) for i,item in _ssct_navigation_choices()])
        context='|'.join((saga.gui.step.ref,saga.camera.what.ref,getattr(saga.camera.focus,'ref','')))
        called_name,called_screen=_ssct_navigation_called_screen()
        if called_screen is not None:context='call-screen:'+called_name+'|'+context
        state=sys.modules['ssct_navigation_probe']
        if getattr(state,'include_interactions',False):
            import ssct_replay_guard,hashlib
            catalogues=_ssct_completion_catalogues()
            facts={name:[(entity.ref,ssct_replay_guard.stored_facts(entity,ignored=('plan','view','when')))
                for entity in catalogues[name]] for name in ('cast','prop','flow','sets')}
            state.latest_facts=_ssct_navigation_serial(facts)
            state.world_identity=hashlib.sha256(repr(facts).encode('utf8')).hexdigest()
            # Window geometry and launch timestamps need not reproduce. The
            # rendered input surface is the UI identity, not a proof that all
            # hidden gameplay state is equivalent. Preserve world differences
            # separately instead of either ignoring them or generating the
            # cross-product of every unrelated transaction.
            context+='|'+str(saga.time.now)+'|'+hashlib.sha256(repr(_ssct_navigation_surface()).encode('utf8')).hexdigest()[:24]
        return context
    def _ssct_navigation_expand():
        state=sys.modules['ssct_navigation_probe']
        source=saga.camera.what.ref
        if saga.time.now!=state.tick:
            state.temporal_exits.append({'requested_tick':state.tick,'actual_tick':saga.time.now,'source':source})
            return
        # Each interaction case is rooted in the completed baseline. Once its
        # native flow returns to ordinary navigation, finish that case rather
        # than exploring the whole town again with its transaction effects.
        # Devices and native menus continue until they actually return there.
        if (getattr(state,'include_interactions',False) and _ssct_navigation_called_screen()[1] is None and saga.gui.step.ref=='nav'
                and saga.camera.focus is None and any(item['protocol'] in ('interaction','choice') for item in state.current_path)):
            if state.rows:state.rows[-1]['interaction_case_terminal']=True
            return
        context=_ssct_navigation_context()
        if context in state.seen:
            if getattr(state,'include_interactions',False) and state.surface_worlds.get(context)!=getattr(state,'world_identity',None):
                state.world_variants[context+'|'+getattr(state,'world_identity','menu')]={
                    'context':context,'status':'same_rendered_surface_not_semantic_equivalence_not_validated'}
            return
        state.seen.add(context)
        if getattr(state,'include_interactions',False):state.surface_worlds[context]=getattr(state,'world_identity',None)
        if getattr(state,'include_interactions',False) and not renpy.get_screen('choice'):
            screen=_ssct_navigation_input_screen()
            nodes=[]
            screen.visit_all(nodes.append)
            for node in nodes:
                action=getattr(node,'clicked',None)
                sensitivity=_ssct_navigation_sensitivity(node)
                if action is None or sensitivity is False:continue
                if isinstance(action,(Emit,Return)) and sensitivity is True:continue
                name=type(action).__module__+'.'+type(action).__name__
                function=getattr(action,'callable',None)
                identity=context+'|'+name+'|'+str(getattr(function,'__module__',None))+'|'+str(getattr(function,'__name__',None))
                state.unhandled_controls[identity]={'context':context,'action_type':name,
                    'callback':str(getattr(function,'__module__',None))+'.'+str(getattr(function,'__name__',None)),
                    'sensitivity':sensitivity,
                    'status':'requires_native_input_adapter_not_validated'}
        import hashlib
        slot='ssct-nav-'+str(state.tick)+'-'+hashlib.sha256(context.encode('utf8')).hexdigest()[:32]
        renpy.save(slot)
        pending_start=len(state.pending)
        anchor=getattr(state,'replay_anchor',None)
        if (saga.gui.step.ref=='nav'
                and _ssct_navigation_called_screen()[1] is None and not renpy.get_screen('choice')):
            anchor={'kind':'ordinary_navigation','slot':slot,'path':list(state.current_path)}
        if getattr(state,'include_interactions',False):
            with open(os.path.join(config.basedir,slot+'.facts.json'),'w',encoding='utf8') as file:
                json.dump(state.latest_facts,file,ensure_ascii=False)
        if renpy.get_screen('choice'):
            for index,item in _ssct_navigation_choices():
                state.pending.append({'slot':slot,'source':source,'source_context':context,
                    'target':item.caption,'protocol':'choice','choice_index':index,'source_path':list(state.current_path),
                    'replay_anchor':anchor})
            return
        if getattr(state,'include_interactions',False):
            signatures=set()
            for action in _ssct_navigation_returns():
                signature=_ssct_navigation_signature(action.value)
                if signature in signatures:continue
                signatures.add(signature)
                state.pending.append({'slot':slot,'source':source,'source_context':context,
                    'target':signature,'protocol':'return','return_signature':signature,'source_path':list(state.current_path)})
        import saga.logic.util as native_util
        from saga import step
        places={id(place):place for place in saga.sets if place in native_util.graph}
        navigation=saga.gui.nav
        targets=set()
        for node,action in _ssct_navigation_controls():
            target=places.get(id(action.value.get('interact')))
            protocol='sets'
            if target is None:
                value=action.value.get('interact')
                if value is navigation:target=value;protocol='gui-nav'
                elif value is saga.mode.nav:target=value;protocol='mode-nav'
                elif getattr(state,'include_interactions',False):
                    if any(value is clock for clock in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark)):continue
                    if any(getattr(entry[0],'__module__','')=='saga.logic.nav' and getattr(entry[0],'__name__','')=='rest'
                           and dict(entry[1]).get('interact') is value for entry in step.nav.pool):continue
                    signature=_ssct_navigation_signature(action.value)
                    if signature in targets:continue
                    targets.add(signature)
                    state.pending.append({'slot':slot,'source':source,'source_context':context,
                        'target':getattr(value,'ref',signature),'protocol':'interaction','event_signature':signature,'source_path':list(state.current_path)})
                    continue
                else:continue
            identity=(protocol,target.ref)
            if (protocol=='sets' and target.ref==source) or identity in targets:continue
            targets.add(identity)
            state.pending.append({'slot':slot,'source':source,'source_context':context,
                'target':target.ref,'target_type':type(target).__module__+'.'+type(target).__name__,'protocol':protocol,'source_path':list(state.current_path)})
        for case in state.pending[pending_start:]:case['replay_anchor']=anchor
    def _ssct_navigation_baseline():
        state=sys.modules['ssct_navigation_probe']
        if state.include_interactions:
            state.baseline_slot='ssct-interaction-base-'+state.baseline_sha256[:24]+'-'+str(state.tick)
            renpy.save(state.baseline_slot)
    def _ssct_navigation_initial_frontier():
        state=sys.modules['ssct_navigation_probe']
        if getattr(state,'seed_case',None) is None:
            _ssct_navigation_expand()
            return
        from collections.abc import Mapping,Sequence
        case=state.seed_case
        if not isinstance(case,Mapping) or not {'source_context','source_path','target','protocol'}<=set(case):
            raise ValueError('Invalid serialized native seed case')
        if not isinstance(case['source_path'],Sequence) or isinstance(case['source_path'],str):
            raise ValueError('Invalid native input path')
        state.pending=[case]
    def _ssct_navigation_device_run(action):
        result=renpy.run(action)
        if result is not None:renpy.end_interaction(result)
    def _ssct_navigation_path_input():
        state=sys.modules['ssct_navigation_probe']
        if state.is_replay:
            state.case_replayed_inputs=getattr(state,'case_replayed_inputs',0)+1
        else:
            state.row['checkpoint_prefix_length']=getattr(state,'checkpoint_prefix_length',0)
            state.row['replayed_input_count']=getattr(state,'case_replayed_inputs',0)
        descriptor={key:value for key,value in state.dispatch.items()
            if key in ('protocol','target','target_type','event_signature','return_signature','choice_index')}
        state.current_path.append(descriptor)
    def _ssct_navigation_next():
        state=sys.modules['ssct_navigation_probe']
        if not state.pending or state.cases>=state.limit or time.monotonic()-state.run_started>48:
            _ssct_navigation_write('navigation_scan_complete' if not state.pending else 'segment_complete')
            renpy.quit(save=False)
        state.active=state.pending.pop(0)
        state.wallet_owner=None
        state.phase=3
        state.case_started=time.monotonic()
        slot,state.current_path,state.replay_pending=ssct_replay_guard.native_replay_start(
            state.active,state.baseline_slot,state.include_interactions)
        state.checkpoint_prefix_length=len(state.current_path)
        state.case_replayed_inputs=0
        state.replay_anchor=state.active.get('replay_anchor')
        _ssct_navigation_write('running')
        renpy.load(slot)
    def _ssct_navigation_tick():
        state=sys.modules['ssct_navigation_probe']
        mode=renpy.get_mode()
        # Check before device/clock early returns: a waiting device must not
        # bypass the watchdog, nor may replay reset the whole-case deadline.
        if state.phase in (3,4) and time.monotonic()-getattr(state,'case_started',state.started if hasattr(state,'started') else time.monotonic())>30:
            raise ValueError('Native case replay deadline exceeded')
        if state.phase in (4,6) and time.monotonic()-state.started>15:
            raise ValueError('Native response interaction deadline exceeded')
        if state.phase==0:
            if renpy.get_screen('main_menu'):
                state.phase=1
                renpy.load('quick-6')
            elif renpy.get_screen('corp') or renpy.get_screen('gate'):renpy.end_interaction(None)
            return
        if state.phase==4:
            called_name,called_screen=_ssct_navigation_called_screen()
            game=called_screen.scope.get('game') if called_screen is not None else None
            if mode=='screen' and native_wallet_protocol.supports(game):
                nodes=[]
                called_screen.visit_all(nodes.append)
                if getattr(state,'wallet_owner',None) is None:
                    owner=called_screen.scope.get('who')
                    if owner is None or (owner.cash,owner.bank)!=(game.cash,game.bank):
                        raise ValueError('Native wallet owner is not bound to the displayed ledgers')
                    state.wallet_owner=owner
                receipt=state.row.setdefault('native_wallet_transaction',{})
                native_wallet_protocol.step(game,nodes,receipt,_ssct_navigation_device_run)
                return
            receipt=state.row.get('native_wallet_transaction')
            if receipt and not receipt.get('native_caller_commit_validated'):
                owner=getattr(state,'wallet_owner',None)
                if receipt.get('phase')!=5 or owner is None or (owner.cash,owner.bank)!=(receipt['before']['cash'],receipt['before']['bank']):
                    raise ValueError('Native wallet caller did not commit the verified ledgers')
                receipt['native_caller_commit_validated']=True
            if mode=='screen' and called_screen is not None and called_name!='mini_keypad':
                state.row['native_branch_trace']=state.tracer.finish()
                _ssct_navigation_path_input()
                if state.is_replay:
                    state.phase=3
                    return
                state.row.update(actual_scene=saga.camera.what.ref,
                    native_labels=state.labels[state.row.pop('labels_start'):],
                    actual_context=_ssct_navigation_context(), reached_target=None,
                    native_called_screen=called_name, native_screen_inputs_validated=False)
                state.rows.append(state.row)
                state.cases+=1
                if state.include_interactions:_ssct_navigation_expand()
                state.phase=2
                _ssct_navigation_next()
            if time.monotonic()-state.started>15:
                raise ValueError('Native response interaction deadline exceeded')
            if mode in ('say','pause','nvl','with'):
                state.advances+=1
                if state.advances>500:raise ValueError('Native response dialogue budget exceeded')
                renpy.end_interaction(True)
                return
            if mode=='menu' and renpy.get_screen('choice'):
                state.row['native_branch_trace']=state.tracer.finish()
                _ssct_navigation_path_input()
                if state.is_replay:
                    state.phase=3
                    return
                state.row.update(actual_scene=saga.camera.what.ref,native_labels=state.labels[state.row.pop('labels_start'):],
                    reached_target=None,response_returned_to_navigation=False,response_returned_to_menu=True,
                    offered_choices=[item.caption for index,item in _ssct_navigation_choices()])
                state.rows.append(state.row)
                state.cases+=1
                if state.include_interactions:_ssct_navigation_expand()
                state.phase=2
                _ssct_navigation_next()
            keypad=renpy.get_screen('mini_keypad')
            if keypad is not None:
                game=keypad.scope.get('game')
                if game is None:raise ValueError('Native keypad game missing')
                if game.wait:return
                import importlib
                goal=getattr(importlib.import_module(type(game).__module__),'goal',None)
                if not isinstance(goal,str) or not goal.isdecimal() or not goal.startswith(game.code):
                    raise ValueError('Unsupported native keypad recipe')
                digit=goal[len(game.code)] if len(game.code)<len(goal) else '#'
                nodes=[]
                keypad.visit_all(nodes.append)
                actions=[node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Function)
                    and node.is_sensitive()
                    and node.clicked.callable==game.input and node.clicked.args==(digit,)]
                if not actions:raise ValueError('Native keypad input control missing')
                state.row.setdefault('device_inputs',[]).append({'screen':'mini_keypad','input':digit,'return_stubbed':False})
                renpy.run(actions[0])
                return
        if state.phase==6:
            if time.monotonic()-state.started>15:raise ValueError('Native clock response deadline exceeded')
            if mode in ('say','pause','nvl','with'):
                renpy.end_interaction(True)
                return
        if mode not in ('screen','menu') or not (renpy.get_screen('nav') or renpy.get_screen('use') or renpy.get_screen('choice')):return
        if state.phase in (5,6):
            if saga.time.now>state.tick:raise ValueError('Native clock overshot requested scenario')
            if saga.time.now==state.tick:
                state.phase=2
                _ssct_navigation_baseline()
                _ssct_navigation_initial_frontier()
                _ssct_navigation_next()
            controls=_ssct_navigation_controls()
            later=[value for value in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark)
                if saga.time.tod<value and saga.time.now+int(value)-int(saga.time.tod)<=state.tick]
            if later:
                target=later[0]
            else:
                from saga import step
                beds=[dict(entry[1]).get('interact') for entry in step.nav.pool
                    if getattr(entry[0],'__module__','')=='saga.logic.nav' and getattr(entry[0],'__name__','')=='rest']
                target=next((value for value in beds if any(action.value.get('interact') is value for node,action in controls)),None)
            actions=[action for node,action in controls if action.value.get('interact') is target]
            if target is None or not actions:raise ValueError('Native clock or sleep control missing in baseline room')
            state.clock_inputs.append({'before_tick':saga.time.now,'target':_ssct_navigation_serial(target)})
            state.phase=6
            state.started=time.monotonic()
            renpy.end_interaction(renpy.run(actions[0]))
        if state.phase==1:
            options_path=os.path.join(config.basedir,'navigation_probe_options.json')
            options=json.load(open(options_path,encoding='utf8')) if os.path.exists(options_path) else {}
            state.tick=int(options.get('tick',saga.time.now))
            state.limit=int(options.get('limit',20))
            state.include_interactions=bool(options.get('include_interactions'))
            state.probe_sha256=options.get('probe_sha256')
            state.probe_dependencies=options.get('probe_dependencies',{})
            state.seed_case=options.get('seed_case')
            if state.seed_case is not None and (not state.include_interactions or options.get('resume')):
                raise ValueError('Targeted case requires a fresh native input replay')
            import hashlib
            files=[os.path.join(config.savedir,name) for name in os.listdir(config.savedir)
                if name.startswith('quick-6-') and name.endswith('.save')]
            if len(files)!=1:raise ValueError('Ambiguous native baseline save')
            state.baseline_sha256=hashlib.sha256(open(files[0],'rb').read()).hexdigest()
            report_path=os.path.join(config.basedir,'perfect_navigation_responses.json')
            if options.get('resume') and os.path.exists(report_path):
                previous=json.load(open(report_path,encoding='utf8'))
                if previous.get('baseline_sha256')!=state.baseline_sha256 or previous.get('tick')!=state.tick or previous.get('version')!=config.version:
                    raise ValueError('Native checkpoint baseline mismatch; refusing stale continuation')
                if previous.get('include_interactions',False)!=state.include_interactions:raise ValueError('Frontier exploration scope mismatch')
                if previous.get('probe_sha256')!=state.probe_sha256:raise ValueError('Probe changed; restart the baseline rather than inherit incomplete frontier coverage')
                if _ssct_navigation_signature(previous.get('probe_dependencies',{}))!=_ssct_navigation_signature(state.probe_dependencies):raise ValueError('Probe dependencies changed; restart the baseline')
                if previous['status']=='failed' and options.get('retry_failed'):
                    if previous.get('active') is None:raise ValueError('Failed before frontier creation; restart the baseline instead of resuming')
                    state.recovered_failure={'error':previous['error'],'note':options.get('recovery_note')}
                    previous['pending'].insert(0,previous['active'])
                elif previous['status'] not in ('segment_complete','navigation_scan_complete'):
                    raise ValueError('Failed or interrupted frontier requires explicit diagnosis')
                state.rows=previous['rows']
                state.pending=previous['pending']
                state.seen=set(previous['seen'])
                state.clock_inputs=previous.get('clock_inputs',[])
                state.temporal_exits=previous.get('temporal_exits',[])
                state.unhandled_controls=previous.get('unhandled_controls',{})
                state.baseline_slot=previous.get('baseline_slot')
                state.world_variants=previous.get('unexplored_world_variants',{})
                state.surface_worlds=previous.get('surface_worlds',{})
                if state.include_interactions and not state.baseline_slot:raise ValueError('Old interaction frontier has no replay baseline; restart with native input paths')
                state.phase=2
                _ssct_navigation_next()
            state.phase=2
            # Each temporal scenario starts from the unchanged quick-6 file,
            # using rendered native clock/sleep actions, never assigning now.
            if state.tick<saga.time.now:raise ValueError('Requested scenario precedes baseline')
            if state.tick!=saga.time.now:
                state.phase=5
                return
            _ssct_navigation_baseline()
            _ssct_navigation_initial_frontier()
            if not state.pending:raise ValueError('No rendered scene-navigation actions; empty coverage is not success')
            _ssct_navigation_next()
        elif state.phase==3:
            state.is_replay=bool(state.replay_pending)
            state.dispatch=state.replay_pending.pop(0) if state.is_replay else state.active
            if not state.is_replay and _ssct_navigation_context()!=state.active['source_context']:
                expected_path=os.path.join(config.basedir,state.active['slot']+'.facts.json')
                expected=json.load(open(expected_path,encoding='utf8')) if os.path.exists(expected_path) else {}
                actual=getattr(state,'latest_facts',{})
                def fields(facts):
                    return {kind+'.'+ref+'.'+key:value for kind,entries in facts.items()
                        for ref,values in entries for key,value in values}
                old,new=fields(expected),fields(actual)
                state.source_difference={key:{'expected':old.get(key),'actual':new.get(key)}
                    for key in sorted(set(old)|set(new)) if old.get(key)!=new.get(key)}
                raise ValueError('Checkpoint source changed')
            request=state.dispatch
            if request['protocol']=='return':
                actions=[action for action in _ssct_navigation_returns() if _ssct_navigation_signature(action.value)==request['return_signature']]
                if not actions:raise ValueError('Native Return button missing during replay')
                state.row=dict(request,rendered_sensitive=True,labels_start=len(state.labels))
                state.phase=4
                state.started=time.monotonic()
                state.advances=0
                state.tracer.begin()
                renpy.run(actions[0])
                return
            if request['protocol']=='choice':
                choices=[item for index,item in _ssct_navigation_choices() if index==request['choice_index'] and item.caption==request['target']]
                if len(choices)!=1:raise ValueError('Native menu choice changed after checkpoint load')
                state.row=dict(request,rendered_sensitive=True,labels_start=len(state.labels))
                state.phase=4
                state.started=time.monotonic()
                state.advances=0
                state.tracer.begin()
                renpy.run(choices[0].action)
                return
            controls=[action for node,action in _ssct_navigation_controls()
                if (_ssct_navigation_signature(action.value)==request['event_signature'] if request['protocol']=='interaction' else
                getattr(action.value.get('interact'),'ref',None)==request['target']
                and type(action.value.get('interact')).__module__+'.'+type(action.value.get('interact')).__name__==request['target_type'])]
            if not controls:raise ValueError('Previously rendered scene action missing after load')
            action=controls[0]
            saga.event.emit(action.value)
            candidates=list(saga.event.find(saga.event.queue[-1])) if saga.event.queue else []
            saga.event.queue.clear()
            state.row=dict(request,event=_ssct_navigation_serial(action.value),
                handlers=[{'source':str(getattr(fn,'__module__',''))+'.'+str(getattr(fn,'__name__','')),
                    'observer':getattr(ctx,'ref',None),'weight':weight} for weight,ctx,args,fn,mutex in candidates],
                rendered_sensitive=True,labels_start=len(state.labels))
            state.phase=4
            state.started=time.monotonic()
            state.advances=0
            _ssct_navigation_write('dispatched')
            state.tracer.begin()
            renpy.end_interaction(renpy.run(action))
        elif state.phase==4:
            state.row['native_branch_trace']=state.tracer.finish()
            _ssct_navigation_path_input()
            if state.is_replay:
                state.phase=3
                return
            actual=saga.camera.what.ref
            protocol=state.active['protocol']
            reached=(None if protocol in ('interaction','choice','return') else actual==state.active['target'] if protocol=='sets' else
                saga.camera.focus is None if protocol=='mode-nav' else
                _ssct_navigation_context()!=state.active['source_context'])
            state.row.update(actual_scene=actual,native_labels=state.labels[state.row.pop('labels_start'):],
                actual_context=_ssct_navigation_context(),reached_target=reached,response_returned_to_navigation=True)
            state.rows.append(state.row)
            state.cases+=1
            _ssct_navigation_expand()
            state.phase=2
            _ssct_navigation_write('running')
            _ssct_navigation_next()
    def _ssct_navigation_checked_tick():
        try:_ssct_navigation_tick()
        except Exception as error:
            if type(error).__name__ in ('QuitException','EndInteraction','LoadException','JumpException','JumpOutException','RestartException') and type(error).__module__.startswith('renpy.'):
                raise
            state=sys.modules['ssct_navigation_probe']
            if state.tracer.active:state.failed_branch_trace=state.tracer.finish()
            import traceback
            _ssct_navigation_write('failed',traceback.format_exc())
            renpy.quit(save=False)
    def _ssct_navigation_interaction():
        renpy.ui.timer(.03,action=Function(_ssct_navigation_checked_tick,_update_screens=False),repeat=True)
    config.interact_callbacks.append(_ssct_navigation_interaction)
label ssct_navigation_probe_splash:
    return
