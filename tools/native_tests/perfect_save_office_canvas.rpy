# Isolated Smith office controls: native defaults / completion / native task stage.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-smith-controls')
    config.save_persistent=False
init 1000 python:
    import sys,types,json,os,time
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_smith_splash'
    state=types.ModuleType('ssct_smith_controls')
    state.phase=0
    state.options=json.load(open(os.path.join(config.basedir,'smith_options.json')))
    state.case=state.options['case']
    state.target=state.options.get('target')
    state.report_name='smith_'+state.case+('_'+state.target if state.target else '')
    state.started=time.monotonic()
    state.report={'case':state.case,'version':config.version}
    sys.modules[state.__name__]=state
    def _ssct_smith_tick():
        state=sys.modules['ssct_smith_controls']
        if time.monotonic()-state.started>30:renpy.quit(save=False)
        if renpy.get_screen('corp') or renpy.get_screen('gate'):
            renpy.end_interaction(None);return
        if state.phase==0 and renpy.get_screen('main_menu'):
            state.phase=1
            renpy.change_language(None)
            if state.case.startswith('native'):
                from saga.game import init as init_game
                init_game()
                renpy.jump('ssct_smith_render')
            else:
                _ssct_perfect_write();renpy.load('quick-6')
        if state.phase==1 and renpy.get_screen('nav') and renpy.get_mode()=='screen':
            renpy.jump('ssct_smith_render')
        if state.phase==3 and renpy.get_mode()=='screen' and (renpy.get_screen('use') or renpy.get_screen('nav')):
            reached=state.target in (saga.camera.what.ref,getattr(saga.camera.focus,'ref',None))
            if not reached:return
            state.report['native_action_reached']=state.target
            state.report['passed']=True
            with open(os.path.join(config.basedir,state.report_name+'.json'),'w',encoding='utf8') as f:json.dump(state.report,f,indent=2)
            renpy.quit(save=False)
        if state.phase!=2 or renpy.get_mode()!='screen':return
        screen=renpy.get_screen('nav')
        if screen is None:return
        nodes=[];screen.visit_all(nodes.append)
        state.report['controls']=[]
        for node in nodes:
            action=getattr(node,'clicked',None)
            if isinstance(action,Emit):
                state.report['controls'].append({'event':{k:getattr(v,'ref',repr(v)) for k,v in action.value.items()},'sensitive':bool(node.is_sensitive())})
        state.report['scene']=saga.camera.what.ref
        state.report['anon_where']=saga.cast.anon.where.ref
        state.report['ursula_where']=getattr(saga.cast.ursula.where,'ref',None)
        state.report['target_controls']=[row for row in state.report['controls'] if row['event'].get('interact') in ('school_desk','school_cabinet','school_bin','school_canvas')]
        import hashlib
        modpath=os.path.join(config.gamedir,'mods/perfect_save/completion_state.rpy')
        state.report['completion_sha256']=hashlib.sha256(open(modpath,'rb').read()).hexdigest() if os.path.exists(modpath) else None
        state.report['mod_loaded']='_ssct_perfect_write' in globals()
        state.report['canvas_tags']=sorted(saga.prop.school_canvas.tags)
        state.report['completion_contract']=getattr(store,'ssct_perfect_generation',{}).get('completion_contract') if getattr(store,'ssct_perfect_generation',None) else None
        state.report['noop']={name:getattr(getattr(saga.prop,name),'noop',None) for name in ('school_desk','school_cabinet','school_bin','school_canvas')}
        assert state.report['scene']=='school_office1'
        state.report['layers']=[{'entity':getattr(entity,'ref',None),'path':repr(path)} for entity,path in saga.camera.what.view]
        state.report['source_sha256']=state.report['completion_sha256']
        if state.case in ('perfect','task'):
            assert 'egypt' in state.report['canvas_tags']
            assert all(not value for value in state.report['noop'].values())
            assert {row['event'].get('interact') for row in state.report['target_controls'] if row['sensitive']}==set(state.report['noop'])
            assert any('school_canvas/day;egypt.png' in row['path'] for row in state.report['layers'])
            assert not state.report['completion_contract']['failures']
        state.report['passed']=state.target is None
        with open(os.path.join(config.basedir,state.report_name+'.json'),'w',encoding='utf8') as f:json.dump(state.report,f,indent=2)
        renpy.screenshot(os.path.join(config.basedir,state.report_name+'.png'))
        if state.target:
            action=next(node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Emit) and getattr(node.clicked.value.get('interact'),'ref',None)==state.target and node.is_sensitive())
            state.phase=3
            renpy.end_interaction(renpy.run(action));return
        renpy.quit(save=False)
    def _ssct_smith_hook(original):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_smith_tick',_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'smith_probe'))
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','use','say'):screen.function=_ssct_smith_hook(screen.function)
label ssct_smith_splash:
    return
label ssct_smith_render:
    python:
        from saga import step,flow
        state=sys.modules['ssct_smith_controls']
        state.phase=2
        saga.cast.ursula.where=None
        saga.cast.anon.where=saga.sets.school_office1
        saga.camera.move(saga.sets.school_office1)
        if state.case=='task':saga.event.attach(step.tor05_tissue_take)
        state.report['task_registered']=step.tor05_tissue_take in saga.event.crowd
        state.report['gui_step']=flow.gui.step.ref
        state.report['constructed']=bool(getattr(store,'ssct_perfect_generation',None))
        state.report['preparation']='Empty office rendered directly with native nav screen; no entry/prologue walkthrough.'
    call screen nav(saga.camera.what)
    $ saga.event.emit(_return)
    jump loop
screen ssct_smith_tick():
    timer .2 repeat True action Function(_ssct_smith_tick)
