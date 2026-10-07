# Isolated native event execution; never install in a player's game.
# Inputs come from active event filters; no quest-step/flag/reward fabrication.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-native-route-formal')
    config.extra_savedirs=[]

init 999 python:
    import sys,types
    import importlib.util,os
    _ssct_guard_spec=importlib.util.spec_from_file_location('ssct_replay_guard',os.path.join(config.basedir,'ssct_replay_guard.py'))
    _ssct_guard_module=importlib.util.module_from_spec(_ssct_guard_spec)
    _ssct_guard_spec.loader.exec_module(_ssct_guard_module)
    _ssct_replay=types.ModuleType('ssct_native_route_execution')
    _ssct_replay.original_difficulty=persistent.mode
    sys.modules[_ssct_replay.__name__]=_ssct_replay
    def _ssct_replay_restore_preferences():
        persistent.mode=sys.modules['ssct_native_route_execution'].original_difficulty
    config.quit_callbacks.append(_ssct_replay_restore_preferences)
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_native_route_splash'
    config.label_overrides['start']='ssct_native_route_start'
    config.predict_statements=0
    config.save_persistent=False
    config.overlay_screens.append('ssct_native_route_tick')
    def _ssct_replay_interaction():
        renpy.ui.timer(.02,action=Function(_ssct_replay_tick,_update_screens=False),repeat=True)
    config.interact_callbacks.append(_ssct_replay_interaction)
    # Observe the engine's own reservation predicate during real callbacks.
    # Do not call quest callbacks speculatively or alter reservations.
    import saga.logic.util as _ssct_native_util
    import functools
    _ssct_replay.original_req=_ssct_native_util.req
    @functools.wraps(_ssct_native_util.req)
    def _ssct_replay_req(*args,**kwargs):
        result=sys.modules['ssct_native_route_execution'].original_req(*args,**kwargs)
        state=sys.modules['ssct_native_route_execution']
        if result is not True and hasattr(state,'events'):
            participants=[]
            for value in args:
                if value in tuple(saga.cast):
                    participants.append({'actor':value.ref,'where':getattr(value.where,'ref',None),
                        'current_reservations':[_ssct_replay_serial(value.plan[i]) for i in range(2)]})
            state.last_native_reservation_failure={'kwargs':_ssct_replay_serial(kwargs),
                'args':_ssct_replay_serial(args),'participants':participants,
                'current_routes':_ssct_replay_state()}
        return result
    for _ssct_module in tuple(sys.modules.values()):
        if getattr(_ssct_module,'__name__','').startswith('saga.logic.'):
            for _ssct_name,_ssct_value in tuple(vars(_ssct_module).items()):
                if _ssct_value is _ssct_replay.original_req:setattr(_ssct_module,_ssct_name,_ssct_replay_req)
    from saga import step as _ssct_native_steps
    for _ssct_node in _ssct_native_steps:
        for _ssct_entry in getattr(_ssct_node,'pool',()):
            _ssct_globals=getattr(_ssct_entry[0],'__globals__',{})
            for _ssct_name,_ssct_value in tuple(_ssct_globals.items()):
                if _ssct_value is _ssct_replay.original_req:_ssct_globals[_ssct_name]=_ssct_replay_req
                elif isinstance(_ssct_value,functools.partial) and _ssct_value.func is _ssct_replay.original_req:
                    _ssct_globals[_ssct_name]=functools.partial(_ssct_replay_req,*_ssct_value.args,**_ssct_value.keywords)
    def _ssct_replay_menu_input(items,*args,**kwargs):
        # Feed only an enabled value supplied by the native menu. The original
        # saga menu still processes choice notes and the actual script branch.
        # This replaces menu rendering, not scene returns or quest callbacks.
        state=sys.modules['ssct_native_route_execution']
        offered=[(caption,item) for caption,item in items if getattr(item,'value',None) is not None
            and (not getattr(item,'args',()) or item.args[0])]
        if not offered:raise ValueError('No supported enabled native menu choice')
        menu_key=(str(renpy.game.context().current),tuple(repr(item.value) for caption,item in offered))
        chosen=None
        menu=renpy.game.script.namemap.get(renpy.game.context().current)
        goal=getattr(state,'menu_goal',None)
        if goal is not None and isinstance(menu,renpy.ast.Menu):
            for caption,item in offered:
                if not isinstance(item.value,int) or not 0<=item.value<len(menu.items):continue
                block=menu.items[item.value][2] or ()
                if any(isinstance(statement,renpy.ast.Return) and
                        _ssct_guard_module.native_choice_target(statement.expression)==goal for statement in block):
                    chosen=(caption,item);break
        caption,item=chosen or _ssct_guard_module.choose_unexplored(offered,state.menu_visits,menu_key)
        if chosen is not None:
            visit_key=(menu_key,offered.index(chosen))
            state.menu_visits[visit_key]=state.menu_visits.get(visit_key,0)+1
            state.menu_goal=None
        state.choices.append({'caption':caption,'offered':[row[0] for row in offered],
            'input_value':item.value,'menu_rendered':False,'native_goal_selected':chosen is not None,
            'native_goal':goal,'native_menu_type':type(menu).__name__})
        _ssct_replay_write('running')
        return item.value
    import saga.renpy.menu as _ssct_menu_module
    _ssct_menu_module.menu.__globals__['display_menu']=_ssct_replay_menu_input

    def _ssct_replay_serial(value):
        from collections.abc import Mapping
        if isinstance(value,(str,int,float,bool)) or value is None:return value
        if isinstance(value,Mapping):return {str(k):_ssct_replay_serial(v) for k,v in value.items()}
        if isinstance(value,(list,tuple,set,frozenset)):return [_ssct_replay_serial(v) for v in value]
        return getattr(value,'ref',repr(value))

    def _ssct_replay_notes():
        state=sys.modules['ssct_native_route_execution']
        if not hasattr(state,'notes_query'):
            import renpy.display.screen as native_screens
            queries=set()
            for (name,variant),screen in native_screens.screens.items():
                if name!='tel_note':continue
                for node in screen.function.children:
                    if type(node).__name__!='SLDefault':continue
                    query=_ssct_guard_module.native_screen_query(node.expression)
                    if query is not None:queries.add(query)
            if len(queries)!=1:raise ValueError('Native Notes screen query is missing or ambiguous: '+repr(queries))
            state.notes_query=queries.pop()
        return tuple(getattr(saga.prop.anon_phone,state.notes_query)())

    def _ssct_replay_analysis(function,kind):
        # Cache source metadata only. Entity values, native predicates and
        # rendered controls are read again for each decision.
        state=sys.modules['ssct_native_route_execution']
        if not hasattr(state,'analysis_cache'):state.analysis_cache={}
        catalogues=_ssct_completion_catalogues()
        owners={id(value) for value in catalogues.values()}
        aliases=tuple(sorted((name,id(value)) for name,value in getattr(function,'__globals__',{}).items()
            if id(value) in owners))
        key=(id(function),id(getattr(function,'__code__',None)),kind,aliases)
        if key not in state.analysis_cache:
            query={'references':_ssct_guard_module.catalogue_references,
                'dependencies':_ssct_guard_module.catalogue_dependencies,
                'effects':_ssct_guard_module.catalogue_effect_fields,
                'clock_places':_ssct_guard_module.clock_navigation_places}[kind]
            state.analysis_cache[key]=(function,query(function,catalogues))
        return state.analysis_cache[key][1]

    def _ssct_replay_write(status):
        import json,os,time
        from saga import flow,step
        state=sys.modules['ssct_native_route_execution']
        now=time.monotonic()
        if status=='running' and now-getattr(state,'written_at',0)<2:return
        state.written_at=now
        _ssct_replay_compact()
        if not hasattr(state,'stage_refs'):
            import re
            catalogue=tuple(step)
            state.stage_refs={route.ref:sorted(item.ref for item in catalogue
                if re.fullmatch(re.escape(route.ref)+r'[0-9]+_.+',item.ref))
                for route in flow}
        if not hasattr(state,'terminal_observations'):state.terminal_observations={}
        routes=[]
        for route in flow:
            stages=state.stage_refs.get(route.ref,())
            if not stages:continue
            current=getattr(route,'step',None)
            endpoint=_ssct_guard_module.finite_endpoint_kind(getattr(current,'ref',None),stages,
                getattr(current,'done',False),getattr(current,'hint',None),len(getattr(current,'pool',())))
            if endpoint and state.terminal_observations.get(route.ref,{}).get('field_schema')!='direct-callback-effects-v2':
                dependencies={}
                for node in step:
                    if node.ref not in stages:continue
                    for entry in getattr(node,'pool',()):
                        for kind,ref,names in _ssct_replay_analysis(entry[0],'effects'):
                            dependencies.setdefault((kind,ref),set(('memo','step','lock','noop','auto','grade','lust'))).update(names)
                facts={}
                for kind,ref in sorted(dependencies):
                    if kind not in ('cast','prop','flow','sets'):continue
                    entity=getattr(_ssct_completion_catalogues()[kind],ref,None)
                    if entity is None:continue
                    facts[kind+'.'+ref]=_ssct_guard_module.stored_facts(entity,
                        included=dependencies[kind,ref]-{'when','where','plan'})
                earlier=state.terminal_observations.get(route.ref)
                state.terminal_observations[route.ref]={'endpoint':endpoint,'step':getattr(current,'ref',None),
                    'field_schema':'direct-callback-effects-v2','earlier_scope_observation':earlier,
                    'time':saga.time.now,'native_done':sorted(item.ref for item in getattr(route,'done',())),
                    'source':'native execution, no projected state assignments',
                    'all_mutually_exclusive_dialogues_verified':False,'postconditions':facts}
            routes.append({'route':route.ref,'step':getattr(getattr(route,'step',None),'ref',None),
                'native_todo':getattr(getattr(route,'step',None),'todo',None),
                'native_hint':getattr(getattr(route,'step',None),'hint',None),
                'native_wait':getattr(route,'wait',None),
                'registered_stages':len(stages),'registered_stage_refs':stages,
                'native_done_tracking':hasattr(route,'done'),
                'native_done':sorted(item.ref for item in getattr(route,'done',()))})
        notes_error=None
        try:notes=_ssct_replay_notes()
        except Exception as exc:
            notes=()
            notes_error=repr(exc)
            state.stop={'reason':'unsupported_native_notes_query','error':notes_error}
            status='blocked'
        result={'version':config.version,'status':status,'scope':'native callback and actual RenPy dialogue execution with controlled event inputs',
            'full_player_playthrough':False,'all_routes_verified':False,
            'menu_rendering_replaced_by_enabled_native_input':True,
            'fabricated_quest_steps':False,'constructed_mod_save':False,
            'difficulty':'easy',
            'native_fast_forward':True,
            'official_start_path':getattr(state,'preview_path',[]),
            'save_locations':[location.directory for location in renpy.loadsave.location.locations],
            'minigame_policy':'Official easy-mode skip where implemented; unsupported screens block',
            'events':state.events,'labels':state.labels,'choices':state.choices,
            'history_segments':state.history_segments,
            'record_counts':{key:state.history_totals[key]+len(getattr(state,key)) for key in state.history_totals},
            'native_notes':[{'route':route.ref,'step':route.step.ref,
                'todo':route.step.todo,'hint':route.step.hint} for route in notes],
            'notes_source':{'screen':'tel_note','query':getattr(state,'notes_query',None),'error':notes_error},
            'dependency_scheduler':{'policy':'native Notes goals; suspend unchanged outcomes until observed prerequisites change',
                'suspended':[{'goal':key,'revision':value} for key,value in getattr(state,'scheduler_waiting',{}).items()],
                'complete_semantic_dependency_graph':False},
            'transitions':state.transitions,'unsupported_inputs':state.unsupported,
            'routes':routes,'stop':getattr(state,'stop',None),
            'terminal_observations':state.terminal_observations,
            'last_dependency_changes':getattr(state,'last_dependency_changes',None),
            'last_native_reservation_failure':getattr(state,'last_native_reservation_failure',None),
            'native_snapshot':{'time':saga.time.now,'camera':saga.camera.what.ref,
                'time_context':{name:getattr(saga.time,name) for name in ('date','dow','tod')},
                'focus':repr(saga.camera.focus),'cash':getattr(saga.cast.anon,'cash',None),
                'stats':{name:getattr(saga.cast.anon,name) for name in ('chr','dex','int','str')},
                'basket':[item.ref for item in saga.gui.buy.sift()] if saga.gui.buy is not None else [],
                'inventory':[item.ref for item in saga.prop.anon_bag.sift(saga.prop)],
                'item_locations':{item.ref:getattr(getattr(item,'where',None),'ref',None)
                    for item in saga.prop if any(base.__name__=='Collectable' for base in type(item).__mro__)},
                'actors':{actor.ref:getattr(getattr(actor,'where',None),'ref',None) for actor in saga.cast},
                'active_inputs':{observer.ref:[{'callback':getattr(fn,'__module__','')+'.'+getattr(fn,'__name__',repr(fn)),
                    'filters':dict(signature),
                    'target_origins':[place.ref for place in getattr(state,'origins',{}).get(
                        getattr(dict(signature).get('interact'),'ref',None),())]}
                    for fn,signature,mutex,weight in getattr(getattr(observer,'step',observer),'pool',())]
                    for observer in saga.event.crowd if state.stage_refs.get(observer.ref)}}}
        path=os.path.join(config.basedir,'native_route_execution.json')
        with open(path+'.tmp','w',encoding='utf8') as f:
            json.dump(_ssct_replay_serial(result),f,ensure_ascii=False,indent=2)
        import time
        for attempt in range(10):
            try:
                os.replace(path+'.tmp',path)
                break
            except PermissionError:
                # Windows readers temporarily deny replacement. Never turn a
                # live report read into a game/Mod exception.
                if attempt==9:
                    if status!='running':raise
                    return
                time.sleep(.01)

    def _ssct_replay_compact():
        import json,uuid,hashlib
        state=sys.modules['ssct_native_route_execution']
        limits={'events':128,'labels':128,'choices':128,'transitions':16}
        if not hasattr(state,'history_totals'):state.history_totals=dict.fromkeys(limits,0)
        if not hasattr(state,'history_segments'):state.history_segments=[]
        prefixes={key:getattr(state,key)[:-limit] for key,limit in limits.items()
            if len(getattr(state,key))>limit*2}
        if not prefixes:return
        name='native-route-history-'+uuid.uuid4().hex+'.json'
        path=os.path.join(config.basedir,name)
        with open(path+'.tmp','w',encoding='utf8') as output:
            json.dump(_ssct_replay_serial(prefixes),output,ensure_ascii=False,separators=(',',':'))
        os.replace(path+'.tmp',path)
        with open(path,'rb') as source:digest=hashlib.sha256(source.read()).hexdigest()
        state.history_segments.append({'file':name,'sha256':digest,'ranges':{
            key:[state.history_totals[key],state.history_totals[key]+len(rows)] for key,rows in prefixes.items()}})
        # Archive succeeds before trimming memory. No test evidence is dropped.
        for key,rows in prefixes.items():
            state.history_totals[key]+=len(rows)
            setattr(state,key,getattr(state,key)[len(rows):])

    def _ssct_replay_label(name,abnormal=False):
        state=sys.modules['ssct_native_route_execution']
        if hasattr(state,'labels'):
            node=renpy.game.script.namemap.get(name)
            source=str(getattr(node,'filename','')).replace('\\','/')
            # Native fast-forward still executes the original script and
            # post-dialogue effects. Do not return a synthetic scene result.
            if '/plot/' in source:config.skipping='fast'
            elif ('/gui/' in source or source.endswith(('/loop.rpy','/mini.rpy'))
                    or name.startswith('ssct_native_route_')):config.skipping=None
            state.labels.append(name)
            _ssct_replay_write('running')
    config.label_callbacks.append(_ssct_replay_label)

    def _ssct_replay_restore():
        import time
        state=sys.modules['ssct_native_route_execution']
        data=getattr(store,'ssct_replay_checkpoint_data',None)
        if not data or getattr(store,'ssct_replay_checkpoint_protocol',None)!='visible-input-v5':return
        state.__dict__.update(data)
        # Old controller counted successful journeys toward its retry limit.
        # Reset controller counters only; preserve the actual native save.
        if getattr(state,'nav_counter_protocol',None)!=2:
            state.attempts={key:value for key,value in state.attempts.items()
                if key[0] not in ('navigation','navigation_back')}
        state.nav_counter_protocol=2
        state.scheduler=_ssct_guard_module.DependencyScheduler()
        state.scheduler.waiting=getattr(state,'scheduler_waiting',{})
        state.scheduler.journeys=getattr(state,'scheduler_journeys',{})
        state.scheduler_waiting=state.scheduler.waiting
        if not hasattr(state,'intent'):state.intent=None
        if not hasattr(state,'returning_home'):state.returning_home=False
        state.menu_goal=None
        state.started=time.monotonic()
        state.segment_event_start=state.history_totals.get('events',0)+len(state.events)
        state.guard=_ssct_guard_module.ReplayGuard()
        state.stop=None
        state.resumed=True
        renpy.run(SetField(persistent,'mode','easy'))
        _ssct_replay_write('resumed')
        # Preserve the native call stack: a checkpoint can be inside dialogue,
        # and its callback must still execute the real post-dialogue effects.
    config.after_load_callbacks.append(_ssct_replay_restore)

    def _ssct_replay_checkpoint(force=False):
        import time
        state=sys.modules['ssct_native_route_execution']
        if not force and time.monotonic()-getattr(state,'checkpoint_at',0)<5:return
        state.resumed=False
        fields=('events','labels','choices','transitions','unsupported','attempts',
            'clock','last','menu_visits','pending','awaiting_gui','intent','returning_home','preview_path','nav_counter_protocol','scheduler_waiting',
            'history_segments','history_totals','scheduler_journeys','terminal_observations')
        state.scheduler_journeys=state.scheduler.journeys
        store.ssct_replay_checkpoint_data={key:getattr(state,key) for key in fields}
        store.ssct_replay_checkpoint_protocol='visible-input-v5'
        renpy.save('ssct-visible-route-v5',extra_info='Native replay boundary; not a completed save')
        state.checkpoint_at=time.monotonic()

    def _ssct_replay_start():
        import time
        state=sys.modules['ssct_native_route_execution']
        state.events=[];state.labels=[];state.choices=[];state.transitions=[];state.unsupported=[]
        state.segment_event_start=0
        state.attempts={};state.started=time.monotonic();state.clock=0;state.last=None
        state.pending=None;state.awaiting_gui=False
        state.intent=None
        state.returning_home=False
        state.menu_goal=None
        state.guard=_ssct_guard_module.ReplayGuard()
        state.menu_visits={}
        state.nav_counter_protocol=2
        state.scheduler=_ssct_guard_module.DependencyScheduler()
        state.scheduler_waiting=state.scheduler.waiting
        state.preview_path=[]
        renpy.run(SetField(persistent,'mode','easy'))
        persistent._preferences.language=None
        renpy.game.preferences.transitions=0
        store.main_menu=False
        # Resume only a test-owned native save, never reconstructed quest flags.
        if renpy.can_load('ssct-visible-route-v5'):
            renpy.load('ssct-visible-route-v5')
        from saga.game import init as init_game
        init_game()
        # Execute the official preview-with-money setup block, as requested,
        # without taking its final jump into the uncontrolled normal loop.
        label='start.cheat'
        while label!='loop':
            if label in state.preview_path:raise ValueError('Official startup label cycle')
            preview=renpy.game.script.namemap.get(label)
            if preview is None:raise ValueError('Official preview startup missing: '+label)
            state.preview_path.append(label)
            next_label=None
            for statement in preview.block:
                if isinstance(statement,renpy.ast.Python):
                    renpy.python.py_exec_bytecode(statement.code.bytecode,hide=statement.hide)
                elif isinstance(statement,renpy.ast.Jump) and not statement.expression:
                    next_label=statement.target;break
                elif isinstance(statement,renpy.ast.Pass):continue
                else:raise ValueError('Unsupported official startup node: '+type(statement).__name__)
            if next_label is None:raise ValueError('Official startup does not reach native loop')
            label=next_label
        _ssct_replay_write('initialized')

    def _ssct_replay_state():
        return tuple(sorted((observer.ref,getattr(getattr(observer,'step',None),'ref',None))
            for observer in saga.event.crowd))

    def _ssct_replay_revision(references=()):
        import hashlib
        from saga import cast,prop,flow
        catalogues=_ssct_completion_catalogues()
        facts=[]
        state=sys.modules['ssct_native_route_execution']
        if not hasattr(state,'dependency_fact_cache'):state.dependency_fact_cache={}
        for dependency in references:
            catalogue,ref=dependency[:2]
            included=dependency[2] if len(dependency)>2 else ('memo','step','where')
            item=getattr(catalogues[catalogue],ref,None)
            if item is not None:
                fields=_ssct_guard_module.stored_facts(item,ignored=('where',) if item is cast.anon else (),included=included)
                previous=state.dependency_fact_cache.get((catalogue,ref))
                if previous is not None and previous!=fields:
                    before=dict(previous);after=dict(fields)
                    changes=[(name,before.get(name),after.get(name)) for name in before.keys()|after.keys()
                        if before.get(name)!=after.get(name)]
                    state.last_dependency_changes=(catalogue,ref,changes)
                state.dependency_fact_cache[(catalogue,ref)]=fields
                facts.append((catalogue,ref,fields))
        inventory=tuple(sorted(item.ref for item in prop.anon_bag.sift(prop)))
        # Route and inventory changes can satisfy shared prerequisites. Camera
        # movement and unrelated entities' visual caches cannot revive a goal.
        state=sys.modules['ssct_native_route_execution']
        routes=tuple((route.ref,getattr(getattr(route,'step',None),'ref',None))
            for route in flow if state.stage_refs.get(route.ref))
        return hashlib.sha256(repr((saga.time.now,routes,inventory,facts)).encode('utf8')).hexdigest()

    def _ssct_replay_plan():
        import time,re,inspect
        state=sys.modules['ssct_native_route_execution']
        state.menu_goal=None
        snapshot=_ssct_replay_state()
        revision=_ssct_replay_revision()
        state.revision=revision
        if state.events and state.events[-1].get('dispatch')=='accepted_native_input':
            state.events[-1]['camera_after']=saga.camera.what.ref
            state.events[-1]['focus_after']=repr(saga.camera.focus)
            previous=state.events[-1]
            if 'inventory_before' in previous:
                current_inventory={item.ref for item in saga.prop.anon_bag.sift(saga.prop)}
                previous['inventory_added']=sorted(current_inventory-set(previous['inventory_before']))
                previous['inventory_removed']=sorted(set(previous['inventory_before'])-current_inventory)
            counter_key=previous.get('counter_key')
            if counter_key and _ssct_guard_module.navigation_succeeded(counter_key[0],
                    previous.get('camera_before'),previous.get('focus_before'),saga.camera.what.ref,
                    repr(saga.camera.focus) if counter_key[0]=='navigation_back' else getattr(saga.camera.focus,'ref',None),
                    getattr(previous.get('input',{}).get('interact'),'ref',None)):
                state.attempts.pop(counter_key,None)
                previous['navigation_reached_target']=True
            if 'dependency_outcome' not in previous and previous.get('intent') is not None:
                is_navigation=bool(counter_key and counter_key[0] in ('navigation','navigation_back'))
                dependency_revision=_ssct_replay_revision(previous.get('dependency_refs',()))
                previous['world_after']=dependency_revision
                previous['dependency_outcome']=state.scheduler.observe(previous['intent'],
                    previous.get('world_before'),dependency_revision,
                    reached=not is_navigation or previous.get('navigation_reached_target',False),
                    navigation=is_navigation)
                if is_navigation and previous.get('navigation_reached_target',False):
                    edge=(previous.get('camera_before'),previous.get('focus_before'),
                        saga.camera.what.ref,repr(saga.camera.focus))
                    if state.scheduler.navigation_cycle(previous['intent'],dependency_revision,edge):
                        previous['dependency_outcome']='navigation_cycle_await_prerequisite_change'
                        state.intent=None
                if previous['dependency_outcome']=='await_prerequisite_change':state.intent=None
            wait=previous.get('native_wait_path',previous.get('native_home_navigation',{}))
            target=wait.get('interact')
            if (state.returning_home and target in tuple(saga.sets)
                    and target is not saga.camera.what and previous.get('camera_before')==saga.camera.what.ref
                    and previous.get('focus_before')==repr(saga.camera.focus)):
                # A native story fence vetoed the attempted journey. Do not
                # keep forcing that same homeward hop instead of public wait.
                state.returning_home=False
                previous['native_home_navigation_vetoed']=True
        if state.last is not None and snapshot!=state.last:
            state.transitions.append({'after_event':state.history_totals['events']+len(state.events),'before':state.last,'after':snapshot})
        state.last=snapshot
        if state.history_totals['events']+len(state.events)-state.segment_event_start>=20000 or time.monotonic()-state.started>300:
            state.stop={'reason':'bounded_execution_limit','events':state.history_totals['events']+len(state.events)}
            _ssct_replay_write('incomplete');return False
        focus=saga.camera.focus
        if saga.gui.step.ref=='use' and getattr(focus,'screen',None)!='inv':
            # Inspect the rendered device, not guessed app names or internal
            # focus values. Dispatch is delayed until the native screen exists.
            state.awaiting_device=True
            return True
        candidates=[]
        candidate_dependencies={}
        from saga import cast,prop,sets,flow
        progress_key=tuple((route.ref,getattr(getattr(route,'step',None),'ref',None))
            for route in flow if state.stage_refs.get(route.ref))
        entities={item for catalogue in (cast,prop) for item in catalogue}
        places=set(sets)
        inventory_key=tuple(sorted(item.ref for item in prop.anon_bag.sift(prop)))
        view_nodes=places|{item for item in prop if hasattr(type(item),'view')}
        if not hasattr(state,'origins'):
            from saga.art.view import cache as view_cache
            state.origins={}
            for place in sorted(view_nodes,key=lambda entity:entity.ref):
                try:layout=view_cache[place.art].plan
                except (KeyError,AttributeError):continue
                for row in layout:
                    entity=row[0]
                    if entity is not None:state.origins.setdefault(entity.ref,[]).append(place)
        town_map=prop.map_town
        def traversable(place):
            # Device views show distant artwork/characters without providing
            # a physical route there. Devices may be destinations, not roads.
            return place in places or place is town_map
        neighbor_cache={}
        def neighbors(place):
            if place in neighbor_cache:return neighbor_cache[place]
            try:
                targets=[entity for entity,path in place.view if entity in view_nodes]
            except (KeyError,AttributeError) as exc:
                if place is saga.camera.what:raise
                row={'place':place.ref,'missing':['unavailable native scene view',str(exc)]}
                if row not in state.unsupported:state.unsupported.append(row)
                neighbor_cache[place]=[]
                return []
            if place in places:targets.append(town_map)
            escape=getattr(place,'esc',None)
            if escape is True and place is saga.camera.what:escape=saga.camera.last
            if escape in places:targets.append(escape)
            neighbor_cache[place]=targets
            return targets
        focus=saga.camera.focus
        if state.returning_home:
            if saga.camera.what is sets.debbie_bed3 and focus is None:
                next_times=[tod for tod in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark)
                    if tod>saga.time.tod]
                if next_times:params={'interact':next_times[0]}
                else:
                    from saga import step
                    visible={entity for entity,path in saga.camera.what.view if entity is not None}
                    beds=[dict(entry[1]).get('interact') for entry in step.nav.pool
                        if getattr(entry[0],'__module__','')=='saga.logic.nav' and getattr(entry[0],'__name__','')=='rest']
                    bed=next((item for item in beds if item in visible),None)
                    if bed is None:
                        state.stop={'reason':'native_bed_control_not_discovered'}
                        _ssct_replay_write('blocked');return False
                    params={'interact':bed}
                state.returning_home=False
            elif focus is not None and saga.camera.what is not town_map:
                params={'interact':None if saga.gui.step.ref=='nav' else saga.mode.nav}
            else:
                hop=_ssct_guard_module.first_visible_hop(saga.camera.what,sets.debbie_bed3,neighbors,traversable)
                if hop is None:
                    state.stop={'reason':'no_visible_path_home_for_clock','camera':saga.camera.what.ref}
                    _ssct_replay_write('blocked');return False
                params={'interact':hop}
            state.events.append({'native_wait_path':params})
            state.pending=params;state.awaiting_gui=True
            _ssct_replay_write('running');return True
        basket=getattr(saga.gui,'buy',None)
        basket_items=tuple(basket.sift()) if basket is not None else ()
        notes=set(_ssct_replay_notes())
        required_public_entities=set()
        for goal_observer in tuple(saga.event.crowd):
            goal_node=getattr(goal_observer,'step',goal_observer)
            if goal_node is None or not re.match(r'^[a-z]+[0-9]+_',goal_node.ref):continue
            for entry in getattr(goal_node,'pool',()):
                for kind,ref in _ssct_replay_analysis(entry[0],'references'):
                    if kind not in ('cast','prop'):continue
                    entity=getattr(_ssct_completion_catalogues()[kind],ref,None)
                    if entity is not None:required_public_entities.add(entity)
        for observer in tuple(saga.event.crowd):
            node=getattr(observer,'step',observer)
            if node is None:continue
            # Include NPC conversation and item/device prerequisite programs;
            # finite quests alone cannot issue cards or initialize computers.
            # GUI/navigation internals and optional infinite repeat flows are
            # not independent actions to synthesize.
            checkout_node=bool(basket_items and any(
                getattr(entry[0],'__module__','')=='saga.logic.shop' and
                getattr(entry[0],'__name__','')=='pay' for entry in getattr(node,'pool',())))
            # Global native programs can own public item/NPC interactions
            # without being an Actor/Prop observer (jobs and transactions).
            # Admit their input declarations, not their internal notifications;
            # the normal visibility and action sensitivity gates below apply.
            public_program=_ssct_guard_module.has_public_program_input(getattr(node,'pool',()),required_public_entities)
            if not (re.match(r'^[a-z]+[0-9]+_',node.ref) or node.ref=='prologue'
                    or observer in entities or checkout_node or public_program):continue
            for fn,signature,mutex,weight in getattr(node,'pool',()):
                params=dict(signature)
                missing=set(getattr(fn,'_req',()))-set(params)
                for key in tuple(missing):
                    if key in ('tod','dow','tick','skip'):
                        params[key]=getattr(saga.time,key if key!='tick' else 'now',0) if key!='skip' else 0
                        missing.remove(key)
                is_finite=bool(re.match(r'^[a-z]+[0-9]+_',node.ref) or node.ref=='prologue')
                task_priority=_ssct_guard_module.task_priority(observer in notes,getattr(node,'todo',None)) if is_finite else 2
                if public_program and not is_finite:task_priority=1
                if task_priority is None:continue
                intent=(observer.ref,node.ref,getattr(fn,'__name__',type(fn).__name__),_ssct_guard_module.filter_key(signature))
                dependencies=_ssct_replay_analysis(fn,'dependencies')
                dependency_revision=_ssct_replay_revision(dependencies)
                candidate_dependencies[intent]=(dependencies,dependency_revision)
                if not state.scheduler.eligible(intent,dependency_revision):continue
                key=(observer.ref,node.ref,getattr(fn,'__name__',type(fn).__name__),_ssct_guard_module.filter_key(signature),
                    dependency_revision)
                if missing:
                    row={'observer':observer.ref,'node':node.ref,'callback':key[2],'missing':sorted(missing)}
                    if row not in state.unsupported:state.unsupported.append(row)
                    continue
                # Event filters describe facts, not permission to fabricate
                # them. Clock facts must match now; internal pump/actor moves
                # must be produced by the game, not injected by this driver.
                if any(name in params and params[name]!=getattr(saga.time,name)
                        for name in ('tod','dow')):continue
                if 'pump' in params:continue
                if 'item' in params:
                    if len(params)!=1:continue
                    params={'interact':params['item']}
                if params=={'focus':None}:
                    # Nav's hud_prop Back returns interact=None; gui.use's
                    # hud_back returns mode.nav. Both cause a native focus
                    # change; focus=None itself is not an input to fabricate.
                    params={'interact':None if saga.gui.step.ref=='nav' else saga.mode.nav}
                elif params=={'focus':observer}:
                    # Native HUD opens the entity using interact, not focus.
                    params={'interact':observer}
                if 'focus' in params:
                    row={'observer':observer.ref,'node':node.ref,'callback':key[2],
                        'missing':['native device opening input adapter; focus is an internal fact']}
                    if row not in state.unsupported:state.unsupported.append(row)
                    continue
                if 'enter' in params:
                    if params.get('what') is saga.cast.anon:
                        params={'interact':params['enter']}
                    elif params.get('enter') is saga.cast.anon and any(
                            base.__name__=='Collectable' for base in type(params.get('what')).__mro__):
                        # Inventory ownership is produced by actual pickup /
                        # checkout, not an injected enter=Anon notification.
                        params={'interact':params['what']}
                    else:continue
                if not any(name in params for name in ('interact','choice')):
                    # Schedules/clock facts belong to native time dispatch.
                    continue
                if 'choice' in params and params['choice'] is None:
                    # These are menu-completion notifications, emitted by the
                    # native dialogue wrapper; they are not player buttons.
                    continue
                if 'choice' in params:
                    # Choice facts must be emitted by a real native menu,
                    # never injected while standing in another scene.
                    who=params.get('who')
                    if who is None:continue
                    params={'interact':who}
                desired=params.get('interact')
                goal=desired if desired in view_nodes else None
                source_filters=dict(signature)
                if ('enter' in source_filters and source_filters.get('what') is cast.anon
                        and desired is saga.camera.what):
                    escape=getattr(desired,'esc',None)
                    if escape is True:escape=saga.camera.last
                    leave=escape if escape in places else next((place for place in neighbors(desired)
                        if place in places and place is not desired),None)
                    if leave is None:continue
                    key=('navigation',desired.ref,leave.ref,saga.time.now,progress_key)
                    params={'interact':leave}
                    goal=None
                if goal is None and 'who' in params:
                    where=getattr(params['who'],'where',None)
                    if where in view_nodes:goal=where
                if goal is None and desired is not None and desired not in places:
                    where=getattr(desired,'where',None)
                    if where in view_nodes:goal=where
                    elif where is not cast.anon:
                        visited=set()
                        while where is not None and where not in visited:
                            visited.add(where)
                            if where in view_nodes:
                                goal=where;break
                            where=getattr(where,'where',None)
                if (goal is None and desired in tuple(prop) and saga.camera.what in view_nodes
                        and getattr(desired,'where',None) is None):
                    # Fixed scenery controls need not have a where field.
                    # Use this version's art plan only to propose a route;
                    # actual visibility is checked again before clicking.
                    for origin in state.origins.get(desired.ref,()):
                        if origin is saga.camera.what or _ssct_guard_module.first_visible_hop(
                                saga.camera.what,origin,neighbors,traversable) is not None:
                            goal=origin;break
                if goal is not None and goal is not saga.camera.what:
                    from saga.logic.auto import graph as native_graph
                    if focus is not None and (saga.gui.step.ref!='nav' or
                            (saga.camera.what not in native_graph and saga.camera.what is not town_map)):
                        key=('navigation_back',saga.camera.what.ref,saga.time.now,progress_key)
                        params={'interact':None if saga.gui.step.ref=='nav' else saga.mode.nav}
                    else:
                        hop=_ssct_guard_module.first_visible_hop(saga.camera.what,goal,neighbors,traversable)
                        if hop is None:continue
                        if hop is not goal or desired not in view_nodes:
                            key=('navigation',saga.camera.what.ref,hop.ref,saga.time.now,progress_key)
                            params={'interact':hop}
                focus=saga.camera.focus
                if focus is not None and getattr(focus,'screen',None)=='inv' and 'interact' in params:
                    # The callback registry contains all items; the visible
                    # inventory does not. Do not inspect nonexistent buttons.
                    if params['interact'] not in tuple(focus.sift(prop)) and params['interact'] is not saga.mode.nav:
                        continue
                if 'interact' in params and params['interact'] is not None:
                    target=params['interact']
                    if target in entities and target not in (prop.anon_bag,prop.anon_phone,town_map):
                        if getattr(focus,'screen',None)=='inv':visible=list(focus.sift(prop))
                        else:visible=[entity for entity,path in saga.camera.what.view if entity is not None]
                        if target not in visible:
                            if getattr(state,'intent',None)==intent and key[0] not in ('navigation','navigation_back'):
                                state.attempts[key]=2
                                state.scheduler.observe(intent,dependency_revision,dependency_revision,reached=False)
                                state.intent=None
                                row={'observer':observer.ref,'node':node.ref,'target':target.ref,
                                    'camera':saga.camera.what.ref,'time':saga.time.now,
                                    'missing':['target reached but not a visible native control at this time']}
                                if row not in state.unsupported:state.unsupported.append(row)
                            continue
                    if target in places and target not in neighbors(saga.camera.what):continue
                if 'interact' in params and isinstance(params['interact'],(int,float)) and not type(params['interact']).__module__.startswith('saga.enum'):
                    row={'observer':observer.ref,'node':node.ref,'callback':key[2],
                        'missing':['validated UI control context for numeric interact']}
                    if row not in state.unsupported:state.unsupported.append(row)
                    continue
                target=params.get('interact')
                if type(target).__module__.startswith('saga.enum') and target in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark):
                    if not _ssct_guard_module.clock_button_allowed(saga.gui.step.ref,
                            saga.camera.focus is not None,saga.time.tod,target):continue
                if state.attempts.get(key,0)>=2:continue
                if not Emit(**params).get_sensitive():
                    if saga.camera.what is town_map:
                        row={'observer':observer.ref,'node':node.ref,
                            'missing':['native map action insensitive',repr(params)]}
                        if row not in state.unsupported:state.unsupported.append(row)
                    continue
                priority=task_priority
                if getattr(state,'intent',None)==intent:priority=-3
                if checkout_node and getattr(fn,'__name__','')=='pay':
                    priority=-4
                    if key[0] not in ('navigation','navigation_back'):
                        key=('native_checkout',node.ref,repr(tuple(item.ref for item in basket_items)),saga.time.now,progress_key)
                    if state.attempts.get(key,0)>=2:continue
                candidates.append((priority,state.attempts.get(key,0),node.ref,weight,key,params,intent))
        if saga.gui.step.ref=='nav':
            for entity,path in saga.camera.what.view:
                if any(base.__name__=='Actor' for base in type(entity).__mro__):
                    params={'interact':entity}
                    key=('visible_conversation',saga.camera.what.ref,entity.ref,
                        getattr(getattr(entity,'step',None),'ref',None),
                        repr(_ssct_guard_module.stored_facts(entity,included=('memo','step'))),
                        saga.time.tod,saga.time.dow)
                    if state.attempts.get(key,0)<2 and Emit(**params).get_sensitive():
                        candidates.append((2,state.attempts.get(key,0),'visible_conversation',0,key,params,None))
                if not any(base.__name__=='Collectable' for base in type(entity).__mro__) or entity.where is cast.anon:continue
                params={'interact':entity}
                key=('visible_acquisition',saga.camera.what.ref,entity.ref,saga.time.now)
                if state.attempts.get(key,0)>=2 or not Emit(**params).get_sensitive():continue
                candidates.append((-5,state.attempts.get(key,0),'visible_acquisition',0,key,params,None))
            for target in neighbors(saga.camera.what):
                if target not in places and target is not town_map:continue
                key=('visible_exploration',saga.camera.what.ref,target.ref,
                    saga.time.tod,saga.time.dow,
                    repr(_ssct_guard_module.stored_facts(target,included=('memo','step','lock'))))
                if state.attempts.get(key,0) or not Emit(interact=target).get_sensitive():continue
                candidates.append((3,0,'visible_exploration',0,key,{'interact':target},None))
        if state.intent is not None and not any(row[6]==state.intent for row in candidates):
            # A journey can reach a locked-room boundary or an absent NPC
            # without ever producing a clickable final action. This is a
            # failed goal expansion, not permission to start the journey again.
            refs,goal_revision=candidate_dependencies.get(state.intent,
                ((),_ssct_replay_revision()))
            state.scheduler.observe(state.intent,goal_revision,goal_revision,reached=False)
            state.events.append({'goal_expansion_blocked':state.intent,
                'dependency_refs':refs,'world_after':goal_revision,
                'camera':saga.camera.what.ref,'dependency_outcome':'await_prerequisite_change'})
            state.intent=None
        if candidates:
            priority,unused,ref,weight,key,params,intent=min(candidates,key=lambda row:row[:4])
            state.attempts[key]=state.attempts.get(key,0)+1
            state.intent=intent if key[0] in ('navigation','navigation_back') else None
            filters=dict(intent[3]) if intent is not None else {}
            if 'choice' in filters and key[0] not in ('navigation','navigation_back'):
                import ast
                topic=ast.literal_eval(filters['choice'])
                who=params.get('interact')
                if isinstance(topic,str) and who in tuple(cast):state.menu_goal=(topic,who.ref)
            state.events.append({'intent':intent,'observer':key[0],'node':ref,'callback':key[2],'input':params,
                'counter_key':key,'world_before':candidate_dependencies.get(intent,((),revision))[1],
                'dependency_refs':candidate_dependencies.get(intent,((),revision))[0]})
        else:
            if state.clock<1400 and saga.gui.step.ref=='nav' and saga.camera.focus is None:
                later=[tod for tod in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark)
                    if tod>saga.time.tod]
                key=('public_wait',saga.camera.what.ref,saga.time.now,progress_key)
                if later and state.attempts.get(key,0)==0 and Emit(interact=later[0]).get_sensitive():
                    state.attempts[key]=1;state.clock+=1
                    params={'interact':later[0]}
                    state.events.append({'native_public_wait':params})
                    state.pending=params;state.awaiting_gui=True
                    _ssct_replay_write('running');return True
            # Public clock controls can be vetoed by native venue programs.
            # Travel home through visible controls before waiting/sleeping.
            if state.clock<1400 and saga.gui.step.ref=='nav' and saga.camera.what is not sets.debbie_bed3:
                if saga.camera.focus is None or saga.camera.what is town_map:
                    hop=_ssct_guard_module.first_visible_hop(saga.camera.what,sets.debbie_bed3,neighbors,traversable)
                    if hop is not None and Emit(interact=hop).get_sensitive():
                        state.clock+=1
                        state.returning_home=True
                        params={'interact':hop}
                        state.events.append({'native_home_navigation':params})
                        state.pending=params;state.awaiting_gui=True
                        _ssct_replay_write('running');return True
            if saga.camera.focus is not None:
                params={'interact':None if saga.gui.step.ref=='nav' else saga.mode.nav}
                if Emit(**params).get_sensitive():
                    state.events.append({'native_device_back_button':params})
                    state.pending=params;state.awaiting_gui=True
                    _ssct_replay_write('running');return True
            next_times=[tod for tod in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark)
                if tod>saga.time.tod]
            if state.clock<1400 and saga.camera.focus is None and saga.gui.step.ref=='nav' and next_times:
                # Actual hud_time button input; native code advances time and
                # dispatches schedules. Never assign time.now or inject ticks.
                state.clock+=1
                params={'interact':next_times[0]}
                state.events.append({'native_clock_button':params})
                state.pending=params;state.awaiting_gui=True
                _ssct_replay_write('running');return True
            if state.clock<1400 and saga.camera.focus is None and saga.gui.step.ref=='nav' and saga.time.tod is saga.time.dark:
                # Explicit test fixture: go home and use the native sleep
                # control there. Do not inject a night tick in another scene.
                from saga import sets,step
                beds=[dict(entry[1]).get('interact') for entry in step.nav.pool
                    if getattr(entry[0],'__module__','')=='saga.logic.nav' and getattr(entry[0],'__name__','')=='rest']
                visible={entity for entity,path in saga.camera.what.view if entity is not None}
                bed=next((item for item in beds if item in visible),None)
                if saga.camera.what is sets.debbie_bed3 and bed is None:
                    state.stop={'reason':'native_bed_control_not_discovered'}
                    _ssct_replay_write('blocked');return False
                params={'interact':bed if bed is not None else sets.debbie_bed3}
                state.clock+=1
                state.events.append({'native_home_sleep_input':params})
                state.pending=params;state.awaiting_gui=True
                _ssct_replay_write('running');return True
            state.stop={'reason':'native_navigation_device_or_clock_adapter_required',
                'camera':repr(saga.camera.what),'focus':repr(saga.camera.focus),
                'native_time':saga.time.now}
            _ssct_replay_write('blocked');return False
        state.pending=params
        state.awaiting_gui=True
        _ssct_replay_write('running');return True

    def _ssct_replay_plan_checked():
        try:
            ready=_ssct_replay_plan()
            if ready:
                import time
                sys.modules['ssct_native_route_execution'].guard.begin_interaction(time.monotonic())
            return ready
        except Exception as exc:
            import traceback
            state=sys.modules['ssct_native_route_execution']
            state.stop={'reason':'planner_exception','error':repr(exc),'traceback':traceback.format_exc()}
            _ssct_replay_write('blocked')
            return False

    def _ssct_replay_emitted(value):
        state=sys.modules['ssct_native_route_execution']
        if state.events:
            state.events[-1]['native_gui_return']=value
        if value is None:return
        saga.event.emit(value)
        if state.events and saga.event.queue:
            state.events[-1]['native_matched_callbacks']=[
                {'observer':getattr(ctx,'ref',repr(ctx)),
                    'callback':getattr(fn,'__module__','')+'.'+getattr(fn,'__name__',repr(fn)),
                    'weight':weight}
                for weight,ctx,args,fn,mutex in saga.event.find(saga.event.queue[-1])]
        _ssct_replay_write('running')

    def _ssct_replay_tick(items=None):
        import time
        state=sys.modules['ssct_native_route_execution']
        if getattr(state,'input_dispatching',False):return
        if not hasattr(state,'started'):
            if renpy.get_screen('main_menu') is not None:
                renpy.run(Start())
            return
        mode=renpy.get_mode()
        context=renpy.game.context()
        say=renpy.get_screen('say')
        dialogue=repr(say.scope.get('what')) if say else None
        garden=renpy.get_screen('mini_garden')
        garden_game=garden.scope.get('game') if garden is not None else None
        paint=renpy.get_screen('mini_paint')
        paint_game=paint.scope.get('game') if paint is not None else None
        camera=renpy.get_screen('mini_camera')
        camera_game=camera.scope.get('game') if camera is not None else None
        if getattr(state,'manual_hold',False):return
        if paint_game is not None and os.path.isfile(os.path.join(config.basedir,'ssct-manual-paint.request')):
            state.manual_hold=True
            config.skipping=None
            _ssct_replay_checkpoint(force=True)
            state.stop={'reason':'manual_paint_ready','automation_paused':True}
            _ssct_replay_write('manual_test_ready')
            renpy.screenshot(os.path.join(config.basedir,'manual_paint_ready.png'))
            return
        mini_progress=(repr(getattr(garden_game,'gone',None)),
            repr(getattr(paint_game,'spots',None)),repr(getattr(paint_game,'mix',None)),
            repr(getattr(camera_game,'pics',None)))
        fingerprint=(mode,str(getattr(context,'current',None)),dialogue,
            str(saga.gui.step.ref),saga.camera.what.ref,repr(saga.camera.focus),getattr(state,'awaiting_gui',False),
            repr(getattr(state,'pending',None)),mini_progress)
        reason=state.guard.observe(time.monotonic(),fingerprint,
            (_ssct_replay_state(),saga.time.now))
        if reason:
            state.stop={'reason':reason,'interaction':fingerprint,
                'last_label':state.labels[-1] if state.labels else None,
                'choice_screen_present':renpy.get_screen('choice') is not None,
                'last_requested_input':state.events[-1] if state.events else None}
            _ssct_replay_write('blocked');renpy.quit(save=False)
        if getattr(state,'mode',None)!=mode:
            state.mode=mode
            state.stop={'current_mode':mode}
            _ssct_replay_write('running')
        if time.monotonic()-state.started>305:
            state.stop={'reason':'interaction_timeout','mode':mode,'screens':[str(key) for key in renpy.get_screen('say').scope] if renpy.get_screen('say') else [],'last_label':state.labels[-1] if state.labels else None}
            _ssct_replay_write('blocked');renpy.quit(save=False)
        choice=renpy.get_screen('choice') if mode=='menu' else None
        if items is None and mode=='menu':items=getattr(state,'current_items',None)
        if items is not None or choice is not None:
            if items is None:items=choice.scope['items']
            offered=[item for item in items if (not item.args or item.args[0]) and getattr(item,'action',None) is not None and renpy.is_sensitive(item.action)]
            if offered:
                chosen=offered[0]
                state.choices.append({'caption':chosen.caption,'offered':[item.caption for item in offered]})
                renpy.run(chosen.action)
        elif mode in ('say','pause','nvl','with'):
            if time.monotonic()-getattr(state,'checkpoint_at',0)>5:
                _ssct_replay_checkpoint(force=True)
            renpy.end_interaction(True)
        elif mode=='screen' and garden_game is not None:
            # Use the exact Function(clear, ref, cash) action declared by the
            # native screen. Never assign goal/gone/cash or fake its return.
            if garden_game.wait:return
            offered=[row for row in garden_game.layout if row[0] is not None
                and row[0] not in garden_game.gone and row[2]>0]
            if offered:
                ref,name,cash,path,reveal=offered[0]
                if not any(event.get('native_minigame')=='garden' for event in state.events):
                    renpy.screenshot(os.path.join(config.basedir,'native_route_garden.png'))
                state.events.append({'native_minigame':'garden','visible_button':ref,
                    'caption':name,'value':cash,'return_stubbed':False})
                renpy.run(Function(garden_game.clear,ref,cash))
                _ssct_replay_write('running')
            else:
                state.stop={'reason':'native_garden_has_no_supported_positive_button'}
                _ssct_replay_write('blocked');renpy.quit(save=False)
        elif mode=='screen' and camera_game is not None:
            if camera_game.wait.pool:return
            controls=[]
            def collect_camera(displayable):
                action=getattr(displayable,'clicked',None)
                if isinstance(action,Return) and action.value in camera_game.pics:
                    controls.append((0,action))
                elif isinstance(action,Function) and action.callable==camera_game.take and renpy.is_sensitive(action):
                    controls.append((1,action))
            camera.visit_all(collect_camera)
            if not controls:
                state.stop={'reason':'camera_has_no_supported_rendered_action'}
                _ssct_replay_write('blocked');renpy.quit(save=False)
                return
            priority,action=min(controls,key=lambda row:row[0])
            state.events.append({'native_minigame':'camera','visible_action':'Thumbnail' if priority==0 else 'Shutter',
                'snapshot':_ssct_replay_serial(action.value) if priority==0 else None,'return_stubbed':False})
            state.input_dispatching=True
            try:
                value=renpy.run(action)
                if value is not None:renpy.end_interaction(value)
            finally:state.input_dispatching=False
        elif mode=='screen' and paint_game is not None:
            # Solve the displayed target using this build's color mixing rules,
            # then click actual tube buttons. A wrong pair ends this native
            # game; brute-force guesses cannot be treated as one puzzle round.
            if paint_game.wait.pool:return
            import importlib
            rules=importlib.import_module(type(paint_game).__module__).plan
            rule=rules.get(paint_game.paint)
            if not rule or not set(rule[1]).issubset(set(paint_game.tubes)):
                state.stop={'reason':'unsupported_native_color_rule','visible_color':str(paint_game.paint)}
                _ssct_replay_write('blocked');renpy.quit(save=False)
                return
            pair=set(rule[1])
            extra=set(paint_game.mix)-pair
            missing=pair-set(paint_game.mix)
            tube=next(iter(sorted(extra or missing)),None)
            if tube is None:return
            controls=[]
            def collect_tube(displayable):
                action=getattr(displayable,'clicked',None)
                if (isinstance(action,Function) and action.callable==paint_game.toggle
                        and action.args==(tube,) and renpy.is_sensitive(action)):
                    controls.append(action)
            paint.visit_all(collect_tube)
            if not controls:
                state.stop={'reason':'paint_tube_has_no_rendered_action','tube':tube}
                _ssct_replay_write('blocked');renpy.quit(save=False)
                return
            state.events.append({'native_minigame':'paint','visible_tube':tube,
                'visible_color':str(paint_game.paint),'solver':'native color mixing rules',
                'return_stubbed':False})
            state.input_dispatching=True
            try:renpy.run(controls[0])
            finally:state.input_dispatching=False
        elif mode=='screen' and getattr(state,'awaiting_device',False):
            state.awaiting_device=False
            screen=renpy.get_screen('use')
            device=saga.camera.focus
            controls=[]
            inputs=[]
            def control_value(action):
                if isinstance(action,Emit):return action.value
                return {'app':getattr(action.__self__,'ref',None),'native_method':action.__name__}
            def collect(displayable):
                # Composite actions, Function, SetField and InputValue require
                # separate contracts. Admit native Emit and declared window
                # methods on this device; do not run arbitrary callbacks.
                action=getattr(displayable,'clicked',None)
                if isinstance(action,Emit) and action.get_sensitive():
                    controls.append((displayable,action))
                elif callable(action) and getattr(action,'__name__',None) in ('init','quit'):
                    owner=getattr(action,'__self__',None)
                    if type(owner).__module__.startswith('saga.tech.') and getattr(owner,'dev',None) is device:
                        controls.append((displayable,action))
                if isinstance(displayable,renpy.display.behavior.Input):
                    value=getattr(displayable,'value',None)
                    if value is not None and any(base.__name__=='AuthValue' for base in type(value).__mro__):
                        inputs.append(value)
            if screen is not None:screen.visit_all(collect)
            if not hasattr(state,'device_visits'):state.device_visits=set()
            application=getattr(device,'app',None)
            app=getattr(application,'ref',None)
            revision=repr(_ssct_replay_revision(()))
            # Context includes stored device state: a channel or page switch
            # changes the visible content even when the app name stays sys.
            # Do not call computed view/plan properties or observe wall time.
            window_state=_ssct_guard_module.window_input_state(getattr(device,'ram',None))
            context=('rendered-emit-v8',getattr(device,'ref',None),app,
                repr(_ssct_guard_module.stored_facts(device,ignored=('when','ram') if window_state is not None else ('when',))),
                repr(_ssct_guard_module.stored_facts(application,ignored=('when',))),revision)
            choices=[]
            if inputs:
                # Credentials are native test data, not proof that every
                # password-revealing dialogue was visited. Submit via the
                # actual rendered InputValue and its native validation method.
                state.input_dispatching=True
                try:
                    for value in inputs:
                        value.focus(True)
                        value.set_text(value.key)
                    result=inputs[-1].enter()
                    state.events.append({'native_rendered_auth_input':getattr(device,'ref',None),
                        'input_count':len(inputs),'credentials_source':'native AuthValue test data',
                        'knowledge_prerequisite_verified':False,'return_stubbed':False,
                        'native_result':_ssct_replay_serial(result)})
                    if result is not None:renpy.end_interaction(result)
                finally:state.input_dispatching=False
                return
            for displayable,action in controls:
                # The surrounding view includes navigation buttons. Restrict
                # exploration to app controls on the current device.
                values=control_value(action)
                target=values.get('interact')
                if not any(name in values for name in ('app','event','op')) and (
                        target is None or type(target).__module__.startswith('saga.enum')):continue
                local_window=dict(window_state or ()).get(values.get('app'))
                key=(context,repr(_ssct_replay_serial(local_window)),repr(_ssct_replay_serial(values)))
                if key not in state.device_visits:choices.append((key,displayable,action))
            if choices:
                # Common app exit controls are explored after content controls;
                # screen declaration order often puts Close at the very top.
                key,displayable,action=min(choices,key=lambda row:(
                    control_value(row[2]).get('op',control_value(row[2]).get('native_method')) in ('quit','close','back'),
                    control_value(row[2]).get('op')=='pgdn'))
                state.device_visits.add(key)
                state.events.append({'native_rendered_device_control':_ssct_replay_serial(control_value(action)),
                    'device':getattr(device,'ref',None),'app':app,
                    'context':_ssct_replay_serial(context),
                    'rendered_actions':[_ssct_replay_serial(control_value(item)) for node,item in controls],
                    'displayable':type(displayable).__name__,'dispatch':'accepted_native_input',
                    'return_stubbed':False})
                _ssct_replay_write('running')
                renpy.end_interaction(renpy.run(action))
            else:
                row={'device':getattr(device,'ref',None),'app':app,
                    'screen':getattr(device,'screen',None),
                    'missing':['remaining device prerequisites or non-Emit input contracts'],
                    'rendered_emit_controls':len(controls),
                    'stored_device_fields':_ssct_replay_serial(_ssct_guard_module.stored_facts(device,ignored=('when',))),
                    'rendered_actions':[_ssct_replay_serial(control_value(action)) for node,action in controls]}
                if row not in state.unsupported:state.unsupported.append(row)
                if state.intent is not None:
                    revision=_ssct_replay_revision(())
                    state.scheduler.observe(state.intent,revision,revision,reached=False)
                    state.intent=None
                action=next((action for node,action in controls
                    if isinstance(action,Emit) and action.value.get('interact') is saga.mode.nav),None)
                if action is None:
                    state.stop={'reason':'device_has_no_supported_rendered_control','device':row}
                    _ssct_replay_write('blocked');renpy.quit(save=False)
                else:
                    back_key=(context,repr(_ssct_replay_serial(action.value)))
                    if getattr(state,'last_exhausted_device_back',None)==back_key:
                        state.stop={'reason':'native_device_back_did_not_leave_exhausted_context','device':row}
                        _ssct_replay_write('blocked');renpy.quit(save=False)
                        return
                    state.last_exhausted_device_back=back_key
                    state.events.append({'native_rendered_device_back':_ssct_replay_serial(action.value)})
                    renpy.end_interaction(renpy.run(action))
        elif mode=='screen' and getattr(state,'awaiting_gui',False):
            state.awaiting_gui=False
            state.events[-1]['camera_before']=saga.camera.what.ref
            state.events[-1]['focus_before']=repr(saga.camera.focus)
            state.events[-1]['inventory_before']=[item.ref for item in saga.prop.anon_bag.sift(saga.prop)]
            action=Emit(**state.pending)
            target=state.pending.get('interact')
            if type(target).__module__.startswith('saga.enum') and target in (saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark):
                if not _ssct_guard_module.clock_button_allowed(saga.gui.step.ref,
                        saga.camera.focus is not None,saga.time.tod,target):
                    state.events[-1]['dispatch']='rejected_by_public_clock_context'
                    renpy.end_interaction({})
                    return
            if not action.get_sensitive():
                state.events[-1]['dispatch']='rejected_by_native_sensitivity'
                _ssct_replay_write('running')
                renpy.end_interaction({})
                return
            clock_input=type(target).__module__.startswith('saga.enum') and target in (
                saga.time.dawn,saga.time.noon,saga.time.dusk,saga.time.dark)
            if not clock_input:
                native_screen=renpy.get_screen(saga.gui.step.ref)
                rendered=[]
                def collect_pending_control(displayable):
                    candidate=getattr(displayable,'clicked',None)
                    if isinstance(candidate,Emit) and candidate.get_sensitive() and _ssct_guard_module.declared_input_matches(
                            candidate.value,state.pending):rendered.append(candidate)
                if native_screen is not None:native_screen.visit_all(collect_pending_control)
                if not rendered:
                    state.events[-1]['dispatch']='rejected_missing_rendered_control'
                    _ssct_replay_write('running')
                    renpy.end_interaction({})
                    return
                action=rendered[0]
            state.events[-1]['dispatch']='accepted_native_input'
            renpy.end_interaction(renpy.run(action))
        elif mode=='screen':
            state.stop={'reason':'unhandled_screen_during_native_callback',
                'interaction':fingerprint,'last_label':state.labels[-1] if state.labels else None}
            _ssct_replay_write('blocked');renpy.quit(save=False)

label ssct_native_route_splash:
    return

label ssct_native_route_start:
    $ _ssct_replay_start()
    jump ssct_native_route_loop

label ssct_native_route_loop:
    call loop.drain from ssct_native_route_drain
    if not _ssct_replay_plan_checked():
        $ renpy.quit(save=False)
    $ _ssct_replay_checkpoint()
    call expression 'gui.' + saga.gui.step.ref from ssct_native_route_gui
    $ _ssct_replay_emitted(_return)
    jump ssct_native_route_loop

screen ssct_native_route_tick():
    timer .01 repeat True action Function(_ssct_replay_tick,_update_screens=False)
