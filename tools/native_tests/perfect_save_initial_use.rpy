init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-initial_use-regression')
    config.save_persistent=False
init 1000 python:
    import sys,types,json,os,time
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_initial_use_splash'
    state=types.ModuleType('ssct_initial_use')
    state.phase=0
    state.options=json.load(open(os.path.join(config.basedir,'initial_use_options.json')))
    state.tick=state.options['tick']
    state.case=state.options.get('case','bed')
    state.targets=['anon_chair','__map__','tammy_main'] if state.case=='chair' else ['erik_bed']
    state.report={'actions':[],'labels':[],'version':config.version}
    import hashlib
    state.report['mod_sha256']={name:hashlib.sha256(open(os.path.join(config.gamedir,'mods/perfect_save',name),'rb').read()).hexdigest() for name in ('perfect_save.rpy','completion_state.rpy','reacquisition.rpy')}
    state.started=time.monotonic()
    state.last_action=0
    state.pending=None
    state.chair_clicks=0
    sys.modules[state.__name__]=state
    def _ssct_initial_use_label(name,abnormal):
        sys.modules['ssct_initial_use'].report['labels'].append(name)
    config.label_callbacks.append(_ssct_initial_use_label)
    def _ssct_initial_use_write(status):
        state=sys.modules['ssct_initial_use']
        state.report.update(status=status,scene=saga.camera.what.ref,focus=getattr(saga.camera.focus,'ref',None),where=saga.cast.anon.where.ref)
        with open(os.path.join(config.basedir,'initial_use_'+state.case+'_'+str(state.tick)+'.json'),'w',encoding='utf8') as f:json.dump(state.report,f,indent=2)
    def _ssct_initial_use_tick():
        state=sys.modules['ssct_initial_use']
        mode=renpy.get_mode()
        if time.monotonic()-state.started>25:
            _ssct_initial_use_write('timeout');renpy.quit(save=False)
        if renpy.get_screen('corp') or renpy.get_screen('gate'):
            renpy.end_interaction(None);return
        if state.phase==0 and renpy.get_screen('main_menu'):
            state.phase=1;renpy.change_language(None);_ssct_perfect_write();renpy.load('quick-6')
        if state.phase==1 and renpy.get_screen('nav') and mode=='screen':
            state.phase=2
            state.report['baseline']={'date':saga.time.date,'where':saga.cast.anon.where.ref,'maria_memo':sorted(saga.cast.maria.memo),'actor_memos':{actor.ref:sorted(actor.memo) for actor in saga.cast}}
            if state.options.get('snapshot_only'):
                _ssct_initial_use_write('snapshot_only');renpy.quit(save=False)
            saga.time.now=state.tick
            _ssct_perfect_schedule()
            state.report['generation']=ssct_perfect_generation
            if state.case=='bed':
                saga.camera.move(saga.sets.tammy_bed2)
                state.report['preparation']='camera.move(tammy_bed2); actual bed button follows'
            from saga import step
            import dis
            state.report['scenario']={'tick':saga.time.now,'dow':saga.time.dow.ref,'tod':saga.time.tod.ref,'maria':saga.cast.maria.where.ref,'tony':saga.cast.tony.where.ref}
            renpy.end_interaction({});return
        if state.phase not in (2,3):return
        if time.monotonic()-state.last_action<.6:return
        if mode in ('say','pause','nvl','with'):
            renpy.end_interaction(True);return
        if mode=='menu':
            _ssct_initial_use_write('unexpected_menu');renpy.quit(save=False)
        if mode!='screen':return
        if state.pending is not None:
            if state.pending[0]=='chair':
                if ('door' in saga.prop.anon_chair.tags)!=state.pending[1]:return
            elif state.pending[1] not in (saga.camera.what.ref,getattr(saga.camera.focus,'ref',None)):return
            state.pending=None
        _ssct_initial_use_write('observing_screen')
        screen=renpy.get_screen('use') or renpy.get_screen('nav')
        if screen is None:return
        nodes=[];screen.visit_all(nodes.append)
        controls=[node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Emit) and node.is_sensitive()]
        state.report['surface']=[{key:getattr(value,'ref',repr(value)) for key,value in action.value.items()} for action in controls]
        if not state.targets:
            from saga import step
            state.report['validation']={'chair_used':saga.prop.anon_chair.used,
                'chair_repeat_listener':step.anon_chair in saga.event.crowd,
                'chair_blocking_door':'door' in saga.prop.anon_chair.tags,
                'erik_bed_one_off_retired':step.erik_bed not in saga.event.crowd,
                'erik_drawer_one_off_retired':step.erik_drawer not in saga.event.crowd,
                'forbidden_labels':[label for label in state.report['labels'] if label in ('anon_chair','erik_bed')]}
            assert state.report['validation']['chair_used']
            assert state.report['validation']['chair_repeat_listener']
            assert not state.report['validation']['chair_blocking_door']
            assert state.report['validation']['erik_bed_one_off_retired']
            assert not state.report['validation']['forbidden_labels']
            if state.case=='bed':assert saga.camera.what is saga.prop.erik_bed or saga.camera.focus is saga.prop.erik_bed
            renpy.screenshot(os.path.join(config.basedir,'initial_use_erik_bed.png'))
            _ssct_initial_use_write('first_use_interactions_passed');renpy.quit(save=False)
        desired=state.targets[0]
        target=saga.gui.nav if desired=='__map__' else next((getattr(catalogue,desired) for catalogue in (saga.sets,saga.prop,saga.cast) if hasattr(catalogue,desired)),None)
        actions=[action for action in controls if action.value.get('interact') is target]
        if not actions:
            state.report['missing_target']=desired
            state.report['all_controls']=[{'type':type(getattr(node,'clicked',None)).__name__,'action':repr(getattr(node,'clicked',None)),'sensitive':node.is_sensitive()} for node in nodes if getattr(node,'clicked',None) is not None]
            _ssct_initial_use_write('requires_path_adjustment');renpy.quit(save=False)
        if desired=='anon_chair':
            state.chair_clicks+=1;state.pending=('chair',state.chair_clicks==1)
        else:state.pending=('location','map_town' if desired=='__map__' else desired)
        state.last_action=time.monotonic()
        state.targets.pop(0)
        state.report['actions'].append({'from':saga.camera.what.ref,'focus':getattr(saga.camera.focus,'ref',None),'target':desired,'chair_used':saga.prop.anon_chair.used,'chair_door':'door' in saga.prop.anon_chair.tags})
        _ssct_initial_use_write('dispatched')
        renpy.end_interaction(renpy.run(actions[0]))
    config.overlay_screens.append('ssct_initial_use_tick')
    def _ssct_initial_use_menu_hook(original):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_initial_use_tick',_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'initial_use_probe'))
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','use','say','choice','lewd'):screen.function=_ssct_initial_use_menu_hook(screen.function)
label ssct_initial_use_splash:
    return
screen ssct_initial_use_tick():
    timer .1 repeat True action Function(_ssct_initial_use_tick)
