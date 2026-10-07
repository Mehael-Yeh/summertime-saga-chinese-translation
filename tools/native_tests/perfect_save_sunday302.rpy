init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-sunday302-regression')
    config.save_persistent=False
init 1000 python:
    import sys,types,json,os,time
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_sunday302_splash'
    state=types.ModuleType('ssct_sunday302')
    state.phase=0
    state.options=json.load(open(os.path.join(config.basedir,'sunday302_options.json')))
    state.tick=state.options['tick']
    state.targets=['__map__','apt_main','apt_lobby','apt_lift','apt_pad','apt_hall3','maria_lounge']
    state.report={'actions':[],'labels':[],'version':config.version}
    import hashlib
    state.report['mod_sha256']={name:hashlib.sha256(open(os.path.join(config.gamedir,'mods/perfect_save',name),'rb').read()).hexdigest() for name in ('perfect_save.rpy','completion_state.rpy','reacquisition.rpy')}
    state.started=time.monotonic()
    sys.modules[state.__name__]=state
    def _ssct_sunday302_label(name,abnormal):
        sys.modules['ssct_sunday302'].report['labels'].append(name)
    config.label_callbacks.append(_ssct_sunday302_label)
    def _ssct_sunday302_write(status):
        state=sys.modules['ssct_sunday302']
        state.report.update(status=status,scene=saga.camera.what.ref,focus=getattr(saga.camera.focus,'ref',None),where=saga.cast.anon.where.ref)
        with open(os.path.join(config.basedir,'sunday302_'+str(state.tick)+'.json'),'w',encoding='utf8') as f:json.dump(state.report,f,indent=2)
    def _ssct_sunday302_tick():
        state=sys.modules['ssct_sunday302']
        mode=renpy.get_mode()
        if time.monotonic()-state.started>45:
            _ssct_sunday302_write('timeout');renpy.quit(save=False)
        if renpy.get_screen('corp') or renpy.get_screen('gate'):
            renpy.end_interaction(None);return
        if state.phase==0 and renpy.get_screen('main_menu'):
            state.phase=1;renpy.change_language(None);_ssct_perfect_write();renpy.load('quick-6')
        if state.phase==1 and renpy.get_screen('nav') and mode=='screen':
            state.phase=2
            state.report['baseline']={'date':saga.time.date,'where':saga.cast.anon.where.ref,'maria_memo':sorted(saga.cast.maria.memo),'actor_memos':{actor.ref:sorted(actor.memo) for actor in saga.cast}}
            state.report['gallery_couch']=[{'ref':scene.ref,'description':scene.desc,'label':getattr(scene,'label',None),'state':{key:repr(value) for key,value in scene.state.items()}} for scene in saga.lewd if getattr(scene,'image',None)=='maria/couch_sex' and hasattr(scene,'state')]
            if state.options.get('snapshot_only'):
                _ssct_sunday302_write('snapshot_only');renpy.quit(save=False)
            saga.time.now=state.tick
            _ssct_perfect_schedule()
            state.report['scenario']={'tick':saga.time.now,'dow':saga.time.dow.ref,'tod':saga.time.tod.ref,'maria':saga.cast.maria.where.ref,'tony':saga.cast.tony.where.ref}
            renpy.end_interaction({});return
        if state.phase not in (2,3):return
        if mode in ('say','pause','nvl','with'):
            renpy.end_interaction(True);return
        if mode=='menu':
            choice=renpy.get_screen('choice') or renpy.get_screen('lewd')
            if choice is None:
                _ssct_sunday302_write('unknown_menu_screen');renpy.quit(save=False)
            nodes=[];choice.visit_all(nodes.append)
            items=[item for item in choice.scope.get('items',()) if any(getattr(node,'clicked',None) is item.action and node.is_sensitive() for node in nodes)]
            captions=[item.caption for item in items]
            state.report.setdefault('menus',[]).append(captions)
            if 'Fool around.' in captions:
                item=next(item for item in items if item.caption=='Fool around.')
                state.report['fool_around_selected']=True
                renpy.end_interaction(renpy.run(item.action));return
            if state.phase==3 and any('Cum' in caption for caption in captions):
                expected='mar_couch.noon2' if saga.time.noon else 'mar_couch.dusk2'
                state.report['expected_repeat_label']=expected
                state.report['repeat_observed']=expected in state.report['labels']
                assert state.report['repeat_observed']
                renpy.screenshot(os.path.join(config.basedir,'sunday302_'+str(state.tick)+'_menu.png'))
                _ssct_sunday302_write('interaction_menu_reached');renpy.quit(save=False)
            _ssct_sunday302_write('unexpected_menu');renpy.quit(save=False)
        if mode!='screen':return
        _ssct_sunday302_write('observing_screen')
        screen=renpy.get_screen('use') or renpy.get_screen('nav')
        if screen is None:return
        nodes=[];screen.visit_all(nodes.append)
        controls=[node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Emit) and node.is_sensitive()]
        state.report['surface']=[{key:getattr(value,'ref',repr(value)) for key,value in action.value.items()} for action in controls]
        if not state.targets:
            if state.phase==2:
                state.report['entry_result']={'where':saga.cast.anon.where.ref,'labels':list(state.report['labels'])}
                if saga.time.noon or saga.time.dusk:
                    assert saga.cast.anon.where is saga.sets.maria_lounge
                    state.phase=3;state.targets=['tony']
                else:
                    assert saga.cast.anon.where is saga.sets.apt_hall3
                    expected='maria_lounge.self' if saga.time.dawn else 'maria_lounge.dark'
                    assert expected in state.report['labels']
                    state.report['expected_closed_label']=expected
                    _ssct_sunday302_write('native_schedule_closed');renpy.quit(save=False)
            else:
                _ssct_sunday302_write('returned_without_interaction_menu');renpy.quit(save=False)
        desired=state.targets[0]
        target=saga.gui.nav if desired=='__map__' else getattr(saga.prop,desired) if desired=='apt_pad' else getattr(saga.cast,desired) if desired=='tony' else getattr(saga.sets,desired)
        actions=[action for action in controls if action.value.get('interact') is target]
        if not actions:
            state.report['missing_target']=desired
            state.report['all_controls']=[{'type':type(getattr(node,'clicked',None)).__name__,'action':repr(getattr(node,'clicked',None)),'sensitive':node.is_sensitive()} for node in nodes if getattr(node,'clicked',None) is not None]
            _ssct_sunday302_write('requires_path_adjustment');renpy.quit(save=False)
        state.targets.pop(0)
        state.report['actions'].append({'from':saga.camera.what.ref,'focus':getattr(saga.camera.focus,'ref',None),'target':desired})
        _ssct_sunday302_write('dispatched')
        renpy.end_interaction(renpy.run(actions[0]))
    config.overlay_screens.append('ssct_sunday302_tick')
    def _ssct_sunday302_menu_hook(original):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_sunday302_tick',_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'sunday302_probe'))
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','use','say','choice','lewd'):screen.function=_ssct_sunday302_menu_hook(screen.function)
label ssct_sunday302_splash:
    return
screen ssct_sunday302_tick():
    timer .1 repeat True action Function(_ssct_sunday302_tick)
