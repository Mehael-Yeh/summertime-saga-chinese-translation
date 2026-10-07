# Targeted isolated regression: generate, reload, and reach both Maria branches.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-maria-regression')
    config.save_persistent=False
init 1000 python:
    import sys,types
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_maria_regression_splash'
    state=types.ModuleType('ssct_maria_regression')
    state.phase=0
    sys.modules[state.__name__]=state
    def _ssct_maria_regression_tick(kind):
        import json,os,hashlib
        from native_script_continuation import ScriptContinuation
        state=sys.modules['ssct_maria_regression']
        if kind in ('corp','gate'):
            renpy.end_interaction(None)
        elif state.phase==0 and kind=='main_menu':
            state.phase=1
            _ssct_perfect_write()
            renpy.load('quick-6')
        elif state.phase==1 and kind=='nav':
            state.phase=2
            result={'version':config.version,'loaded_slot':'quick-6',
                'loaded_date':saga.time.date,'loaded_room':saga.cast.anon.where.ref,
                'conditions':{flag:saga.cast.tony > flag for flag in ('ogle','poly','trio')},
                'source_sha256':hashlib.sha256(open(os.path.join(config.gamedir,'mods/perfect_save/completion_state.rpy'),'rb').read()).hexdigest()}
            assert all(result['conditions'].values())
            result['menu']=ScriptContinuation(renpy).run('mar_dark_maria',(0.75,))
            assert result['menu']['reason']=='native_menu_input_required'
            details=result['menu']['details']
            assert [row['caption'] for row in details['available']]==['Threeway?','Not tonight.']
            result['branches']=[]
            for option in details['available']:
                _ssct_perfect_construct()
                store._choice=set()
                receipt=ScriptContinuation(renpy,{details['source']:option['value']}).run('mar_dark_maria',(0.75,))
                assert any(row.get('native_menu_input')==option['value'] for row in receipt['statements'])
                assert receipt['reason']=='native_menu_input_required' and receipt['details']['source']!=details['source']
                result['branches'].append({'selected':option,'receipt':receipt})
            result['passed']=True
            result['scope']='Native save reload, menu and both branches up to the next menu; presentation suppressed, no full scene playback or daytime reservation sequence.'
            with open(os.path.join(config.basedir,'maria_regression.json'),'w',encoding='utf8') as f:json.dump(result,f,indent=2)
            renpy.quit(save=False)
    def _ssct_maria_regression_hook(original,kind):
        def hook(*args,**kwargs):
            original(*args,**kwargs)
            renpy.use_screen('ssct_maria_regression_tick',kind=kind,_scope=kwargs.get('_scope',{}),_name=(kwargs.get('_name',()),'maria_probe'))
        return hook
    import renpy.display.screen as screens
    for (name,variant),screen in tuple(screens.screens.items()):
        if name in ('main_menu','nav','corp','gate'):
            screen.function=_ssct_maria_regression_hook(screen.function,name)
label ssct_maria_regression_splash:
    return

screen ssct_maria_regression_tick(kind):
    timer .2 repeat True action Function(_ssct_maria_regression_tick,kind)
