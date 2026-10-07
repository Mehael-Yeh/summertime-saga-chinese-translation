# Isolated native TV subscription regression; never install in a player's game.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-tv-account-regression')
    config.save_persistent=False
init 1000 python:
    import sys,types,json,os,time,hashlib
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_tv_account_splash'
    tvtest=types.ModuleType('ssct_tv_account_test')
    tvtest.phase=0
    tvtest.started=time.monotonic()
    tvtest.changes=0
    tvtest.report={'version':config.version,'inputs':[]}
    sys.modules[tvtest.__name__]=tvtest
    def _ssct_tv_account_tick():
        state=sys.modules['ssct_tv_account_test']
        tv=saga.prop.debbie_tv
        with open(os.path.join(config.basedir,'tv_account_progress.json'),'w',encoding='utf8') as f:
            json.dump({'phase':state.phase,'mode':renpy.get_mode(),'tune':getattr(tv,'tune',None),
                'screens':[name for name in ('main_menu','nav','use','tv','say','choice') if renpy.get_screen(name)],
                'inputs':state.report['inputs']},f)
        if time.monotonic()-state.started>40:renpy.quit(save=False)
        if renpy.get_screen('corp') or renpy.get_screen('gate'):
            renpy.end_interaction(None);return
        if state.phase==0 and renpy.get_screen('main_menu'):
            state.phase=1
            renpy.change_language(None)
            _ssct_perfect_write();renpy.load('quick-6')
        if state.phase==1 and renpy.get_screen('nav') and renpy.get_mode()=='screen':
            renpy.jump('ssct_tv_account_prepare')
        if state.phase in (2,5) and renpy.get_screen('nav') and renpy.get_mode()=='screen':
            if state.phase==5:
                assert not tv.chan.auth and tv.chan.auto
                state.report['after_native_quit']={'auto':tv.chan.auto,'auth':tv.chan.auth}
            nodes=[];renpy.get_screen('nav').visit_all(nodes.append)
            action=next(node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Emit)
                and node.clicked.value.get('interact') is tv and node.is_sensitive())
            state.phase=3 if state.phase==2 else 4
            state.report['inputs'].append('native_tv_interact')
            renpy.end_interaction(renpy.run(action));return
        if state.phase in (3,4) and renpy.get_mode() in ('say','pause','nvl','with'):
            renpy.end_interaction(True);return
        if state.phase in (3,4) and renpy.get_mode()=='menu':
            choice=renpy.get_screen('choice') or renpy.get_screen('lewd')
            if choice is None:return
            item=next(item for item in choice.scope.get('items',()) if item.caption=='Maybe later.')
            state.report['inputs'].append('native_maybe_later')
            renpy.end_interaction(renpy.run(item.action));return
        if state.phase==3 and tv.tune==91 and tv.chan.auth and renpy.get_screen('use') and renpy.get_mode()=='screen':
            state.report['first_boot']={'auto':tv.chan.auto,'auth':tv.chan.auth,'tune':tv.tune}
            nodes=[];renpy.get_screen('use').visit_all(nodes.append)
            action=next(node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Emit)
                and node.clicked.value.get('op')=='quit' and node.is_sensitive())
            state.phase=5
            state.report['inputs'].append('native_tv_quit')
            renpy.end_interaction(renpy.run(action));return
        if state.phase in (3,4) and (renpy.get_screen('use') or renpy.get_screen('tv')) and renpy.get_mode()=='screen' and not (tv.tune==91 and tv.chan.auth):
            nodes=[];(renpy.get_screen('use') or renpy.get_screen('tv')).visit_all(nodes.append)
            action=next(node.clicked for node in nodes if isinstance(getattr(node,'clicked',None),Emit)
                and node.clicked.value.get('op')=='pgup' and node.is_sensitive())
            state.report['inputs'].append('native_pgup')
            state.changes+=1
            assert state.changes<=8
            renpy.end_interaction(renpy.run(action));return
        if state.phase==4 and tv.chan.auth:
            assert tv.chan.auto and tv.tune==91
            state.report['second_boot']={'auto':tv.chan.auto,'auth':tv.chan.auth,'tune':tv.tune}
            state.report['contract']=ssct_perfect_generation['completion_contract']['tv_accounts']
            state.report['manual_credential_inputs']=0
            state.report['source_sha256']=hashlib.sha256(open(os.path.join(config.gamedir,'mods/perfect_save/completion_state.rpy'),'rb').read()).hexdigest()
            state.report['passed']=True
            with open(os.path.join(config.basedir,'tv_account_regression.json'),'w',encoding='utf8') as f:json.dump(state.report,f,indent=2)
            renpy.quit(save=False)
    def _ssct_tv_account_hook(original):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_tv_account_tick',_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'tv_account_probe'))
        return hook
    import renpy.display.screen as screens
    config.overlay_screens.append('ssct_tv_account_tick')
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','use','tv','say','adv','mono_text','choice','lewd'):screen.function=_ssct_tv_account_hook(screen.function)
label ssct_tv_account_splash:
    return
label ssct_tv_account_prepare:
    python:
        state=sys.modules['ssct_tv_account_test']
        state.phase=2
        saga.time.now=6
        _ssct_perfect_schedule()
        saga.cast.anon.where=saga.sets.debbie_lounge
        saga.camera.move(saga.sets.debbie_lounge)
        state.report['preparation']='Native dusk clock and lounge prepared directly; actual TV and channel buttons, no full room entry route.'
        assert saga.prop.debbie_tv.tuner[91].freq.auto
    call screen nav(saga.camera.what)
    $ saga.event.emit(_return)
    jump loop
screen ssct_tv_account_tick():
    timer .2 repeat True action Function(_ssct_tv_account_tick)
