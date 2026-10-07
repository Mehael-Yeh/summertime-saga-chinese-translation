# Install only through run_name_probe.py in an isolated official-game copy.
init python early:
    import os
    config.savedir = os.path.join(config.basedir, 'ssct-name-probe-saves')
init 1000 python:
    import sys, types
    config.label_overrides.pop('_start', None)
    config.label_overrides['splashscreen'] = 'ssct_name_splash'
    persistent._preferences.language = None
    _ssct_name_state = types.ModuleType('ssct_name_probe')
    _ssct_name_state.phase = 0
    sys.modules[_ssct_name_state.__name__] = _ssct_name_state
    def _ssct_name_tick(kind):
        state = sys.modules['ssct_name_probe']
        if kind in ('corp', 'gate'):
            renpy.end_interaction(None)
        elif state.phase == 0 and kind == 'main_menu':
            state.phase = 1
            renpy.load('quick-6')
        elif state.phase == 1 and kind == 'nav':
            state.phase = 2
            import json, traceback
            result = {'version': config.version, 'checks': []}
            try:
                for slot in renpy.list_saved_games(fast=True):
                    renpy.unlink_save(slot)
                assert _ssct_perfect_latest_name() == 'Anon'
                result['checks'].append('no saves defaults to Anon')
                saga.cast.anon.name = '旧档玩家'
                config.save_json_callbacks.remove(_ssct_perfect_name_json)
                try:
                    renpy.save('1-1', extra_info='legacy name fixture')
                finally:
                    config.save_json_callbacks.append(_ssct_perfect_name_json)
                assert 'ssct_protagonist_name' not in renpy.slot_json('1-1')
                assert _ssct_perfect_legacy_name('1-1') == '旧档玩家'
                assert _ssct_perfect_latest_name() == '旧档玩家'
                result['checks'].append('signed legacy native save supplies Chinese name')
                saga.cast.anon.name = 'LatestPlayer'
                renpy.save('auto-1', extra_info='latest name fixture')
                assert renpy.slot_mtime('auto-1') >= renpy.slot_mtime('1-1')
                assert _ssct_perfect_latest_name() == 'LatestPlayer'
                saga.cast.anon.name = 'UnsavedLiveName'
                before = renpy.random.getstate()
                record = _ssct_perfect_record()
                roots, unused_log = renpy.loadsave.loads(record.log)
                assert roots['#saga.cast.anon.name'] == 'LatestPlayer'
                assert json.loads(record.json)['ssct_protagonist_name'] == 'LatestPlayer'
                assert saga.cast.anon.name == 'UnsavedLiveName'
                assert renpy.random.getstate() == before
                result['checks'].extend(['newest save beats current unsaved name',
                    'generated native payload and metadata inherit name',
                    'generation preserves live name and random state'])
                result['passed'] = True
            except Exception:
                result['passed'] = False
                result['error'] = traceback.format_exc()
            with open(os.path.join(config.basedir, 'perfect_name_report.json'), 'w', encoding='utf8') as stream:
                json.dump(result, stream, ensure_ascii=False, indent=2)
            renpy.quit(save=False)
    def _ssct_name_hook(original, kind):
        def hook(*args, **kwargs):
            original(*args, **kwargs)
            renpy.use_screen('ssct_name_tick', kind=kind,
                _scope=kwargs.get('_scope', {}), _name=(kwargs.get('_name', ()), 'name_probe'))
        return hook
    import renpy.display.screen as screens
    for (name, variant), screen in tuple(screens.screens.items()):
        if name in ('main_menu', 'nav', 'corp', 'gate'):
            screen.function = _ssct_name_hook(screen.function, name)
label ssct_name_splash:
    return
screen ssct_name_tick(kind):
    timer .2 repeat True action Function(_ssct_name_tick, kind)
