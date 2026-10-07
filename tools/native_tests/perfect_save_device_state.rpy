# State/bytecode probe only; no scene navigation or dialogue playback.
init python early:
    import os
    config.savedir=os.path.join(config.basedir,'ssct-perfect-device-probe')
init 999 python:
    config.label_overrides.pop('_start',None)
    config.label_overrides['splashscreen']='ssct_device_state_probe'
init 999 python:
    def _ssct_device_state_probe():
        import json,os
        from renpy.rollback import RollbackLog
        backup=renpy.python.StoreBackup()
        original_contexts=renpy.game.contexts
        original_log=renpy.game.log
        random_state=renpy.random.getstate()
        try:
            renpy.python.clean_stores()
            renpy.execute_default_statement(True)
            renpy.game.contexts=[renpy.execution.Context(True,clear=True)]
            renpy.game.log=RollbackLog()
            _ssct_perfect_construct()
            laptop=saga.prop.jenny_laptop
            assert 'remote' in laptop.tags
            assert laptop.auto is True
            assert saga.prop.anon_pc.auto is True
            assert saga.prop.anon_pc.step.ref=='anon_pc_idle'
            assert saga.prop.library_card.where is saga.cast.anon
            assert saga.prop.library_shelf not in saga.event.crowd
            report=ssct_perfect_generation['completion_contract']
            assert ['prop','jenny_laptop','remote',True] in report['device_tags']
            assert not report['failures']
            result={'version':config.version,'remote_tag':True,'native_auth_auto':True,
                'anon_pc_ready':True,'completion_postconditions':report['checked'],
                'device_tags':report['device_tags'],'scene_or_dialogue_playback':False,
                'library_card_native_owner':saga.prop.library_card.where.ref,
                'library_shelf_step':saga.prop.library_shelf.step.ref,
                'library_shelf_attached':False,
                'acquired_terminals':report['acquired_terminals'],
                'unsupported_callbacks_remaining':report['unsupported_callbacks']}
        finally:
            backup.restore()
            renpy.game.contexts=original_contexts
            renpy.game.log=original_log
            renpy.random.setstate(random_state)
        with open(os.path.join(config.basedir,'perfect_device_state.json'),'w',encoding='utf8') as f:
            json.dump(result,f,ensure_ascii=False,indent=2)
        renpy.quit(save=False)

label ssct_device_state_probe:
    $ _ssct_device_state_probe()
