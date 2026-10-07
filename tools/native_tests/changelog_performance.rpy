# Run only in an isolated official-game copy through run_changelog_probe.py.
init python early:
    import os
    config.savedir = os.path.join(config.basedir, 'ssct-changelog-compat-tests')
init 1000 python:
    import time, json, sys, types
    config.label_overrides.pop('_start', None)
    config.label_overrides['splashscreen'] = 'ssct_changelog_probe_splash'
    persistent._preferences.language = None
    _cl_probe = types.ModuleType('ssct_changelog_probe')
    _cl_probe.phase = 0
    _cl_probe.metrics = []
    _cl_probe.logs = dict(saga.menu.logs)
    with open(os.path.join(config.basedir, 'changelog_probe_pairs.json'), encoding='utf8') as stream:
        _cl_probe.pairs = json.load(stream)
    _cl_probe.optimized = hasattr(store, '_ssct_changelog_sections')
    sys.modules[_cl_probe.__name__] = _cl_probe
    _cl_native_render = renpy.text.text.Text.render
    def _cl_render(self, *args, **kwargs):
        start = time.perf_counter()
        result = _cl_native_render(self, *args, **kwargs)
        if any(isinstance(text, str) and '{=logs_menu_group}' in text for text in self.text):
            state = sys.modules['ssct_changelog_probe']
            state.metrics.append({'phase': state.phase, 'language': _preferences.language,
                'seconds': time.perf_counter() - start})
        return result
    renpy.text.text.Text.render = _cl_render
    def _cl_tick(kind):
        state = sys.modules['ssct_changelog_probe']
        try:
            if kind in ('corp', 'gate'):
                renpy.end_interaction(None)
            elif kind == 'main_menu' and state.phase == 0:
                state.phase = 1
                renpy.run(ShowMenu('logs'))
            elif kind == 'logs':
                if state.phase == 1:
                    state.phase = 2
                    renpy.change_language('zh_hans')
                elif state.phase == 2:
                    state.coverage = []
                    for key, content in state.logs.items():
                        actual = _ssct_changelog_text(content)
                        native_lines = [line for line in content.splitlines() if line.startswith('- ')]
                        expected = [state.pairs.get(line + '{#ssct_changelog}', line).removesuffix('{#ssct_changelog}') for line in native_lines]
                        actual_lines = [line for line in actual.splitlines() if line.startswith('- ')]
                        assert actual_lines == expected, [(index, a, b) for index, (a, b) in enumerate(zip(actual_lines, expected)) if a != b][:2]
                        assert actual.count('{=logs_menu_group}') == content.count('{=logs_menu_group}')
                        if state.optimized:
                            assert '\n'.join(_ssct_changelog_sections(content)) == actual
                            assert _ssct_changelog_sections(content) is _ssct_changelog_sections(content)
                        state.coverage.append({'key': key, 'entries': len(native_lines),
                            'headers': content.count('{=logs_menu_group}'),
                            'translated_entries': sum(line + '{#ssct_changelog}' in state.pairs for line in native_lines),
                            'english_fallback_entries': [line for line in native_lines if line + '{#ssct_changelog}' not in state.pairs]})
                    renpy.screenshot(os.path.join(config.basedir, 'changelog_probe_top.png'))
                    state.phase = 3
                    renpy.get_screen('logs').scope['scroll'].change(100000)
                    renpy.restart_interaction()
                elif state.phase == 3:
                    screen = renpy.get_screen('logs')
                    if state.optimized and screen.scope['shown'] < len(_ssct_changelog_sections(state.logs[screen.scope['log']])):
                        screen.scope['scroll'].change(100000)
                        renpy.restart_interaction()
                        return
                    state.fully_revealed = True
                    screen.scope['scroll'].change(100000)
                    state.phase = 4
                    renpy.restart_interaction()
                elif state.phase == 4:
                    renpy.screenshot(os.path.join(config.basedir, 'changelog_probe_bottom.png'))
                    state.phase = 5
                    renpy.change_language(None)
                elif state.phase == 5:
                    assert dict(saga.menu.logs) == state.logs
                    assert all(_ssct_changelog_text(content) == content for content in state.logs.values())
                    state.phase = 6
                    # Exercise the existing Older panel too.
                    screen = renpy.get_screen('logs')
                    screen.scope['log'] = None
                    renpy.restart_interaction()
                else:
                    result = {'passed': True, 'version': config.version, 'optimized': state.optimized,
                        'coverage': state.coverage, 'fully_revealed': state.fully_revealed,
                        'english_roundtrip_exact': True, 'native_data_unchanged': True,
                        'older_panel_rendered': True,
                        'initial_chinese_text_render_seconds': sum(row['seconds'] for row in state.metrics if row['phase'] == 2),
                        'metrics': state.metrics}
                    with open(os.path.join(config.basedir, 'changelog_probe_report.json'), 'w', encoding='utf8') as stream:
                        json.dump(result, stream, ensure_ascii=False, indent=2)
                    renpy.quit(save=False)
        except renpy.game.QuitException:
            raise
        except Exception:
            import traceback
            with open(os.path.join(config.basedir, 'changelog_probe_report.json'), 'w', encoding='utf8') as stream:
                json.dump({'passed': False, 'error': traceback.format_exc()}, stream)
            renpy.quit(save=False)
    def _cl_hook(original, kind):
        def hook(*args, **kwargs):
            original(*args, **kwargs)
            renpy.use_screen('ssct_changelog_probe_tick', kind=kind,
                _scope=kwargs.get('_scope', {}), _name=(kwargs.get('_name', ()), 'changelog_probe'))
        return hook
    import renpy.display.screen as screens
    for (name, variant), screen in tuple(screens.screens.items()):
        if name in ('main_menu', 'logs', 'corp', 'gate'):
            screen.function = _cl_hook(screen.function, name)
label ssct_changelog_probe_splash:
    return
screen ssct_changelog_probe_tick(kind):
    timer .15 repeat True action Function(_cl_tick, kind)
