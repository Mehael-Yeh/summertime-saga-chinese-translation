# Isolated native conception and preferences regression; never loads user saves.
init python early:
    import os
    config.savedir = os.path.join(config.basedir, 'ssct-pregnancy-tests')
    config.save_persistent = False
init 1000 python:
    import sys, types, json, copy
    config.label_overrides['_start'] = 'ssct_pregnancy_probe_splash'
    config.label_overrides['splashscreen'] = 'ssct_pregnancy_probe_splash'
    persistent._preferences.language = None
    _preg_probe = types.ModuleType('ssct_pregnancy_probe')
    _preg_probe.phase = 0
    _preg_probe.result = {'version': config.version, 'passed': False, 'rolls': [], 'ui': []}
    _preg_probe.result['install'] = [(repr(key), getattr(value.function, '_ssct_pregnancy_installed', False)) for key, value in _ssct_pregnancy_screens.screens.items() if 'pref' in str(key)]
    sys.modules[_preg_probe.__name__] = _preg_probe

    def _preg_probe_write():
        state = sys.modules['ssct_pregnancy_probe']
        with open(os.path.join(config.basedir, 'pregnancy_probe_report.json'), 'w', encoding='utf8') as f:
            json.dump(state.result, f, ensure_ascii=False, indent=2)

    def _preg_probe_rolls():
        import saga.obgyn as native
        state = sys.modules['ssct_pregnancy_probe']
        womb = copy.copy(saga.cast.maria.womb)
        original_random = native.random
        previous = persistent.ssct_pregnancy_multiplier
        try:
            # Verify the relative native child-type boundaries after scaling.
            womb.risk = .2
            quota = tuple(womb.quota)
            for conditional in (.1, .49, .51, .9):
                kinds = []
                for mode, chance in ((.5, .1), (1, .2), (2, .4), ('always', 1.)):
                    persistent.ssct_pregnancy_multiplier = mode
                    native.random = lambda: 1 - chance + chance * conditional
                    kinds.append(womb.next())
                assert all(kind == kinds[0] for kind in kinds)
            assert tuple(womb.quota) == quota
            state.result['child_type_distribution_preserved'] = True
            for risk in (0.0, .2, .8, 1.0):
                womb.risk = risk
                for mode, expected in ((0, 0), (.5, risk * .5), (1, risk), (2, min(1., risk * 2)), ('always', 1)):
                    persistent.ssct_pregnancy_multiplier = mode
                    kinds = []
                    for index in range(1000):
                        value = (index + .5) / 1000
                        native.random = lambda: value
                        kinds.append(womb.next())
                        if mode == 1:
                            assert kinds[-1] == _ssct_pregnancy_original_next(womb)
                    actual = sum(bool(kind) for kind in kinds) / 1000
                    assert abs(actual - expected) < .001, (risk, mode, actual, expected)
                    assert womb.risk == risk
                    state.result['rolls'].append({'risk': risk, 'mode': mode, 'actual': actual})
            # The native state guard must survive guaranteed mode.
            womb.state = native.sow.bump
            persistent.ssct_pregnancy_multiplier = 'always'
            assert not womb.next()
            state.result['already_pregnant_guard'] = True
            # Both visible wheel and hidden path use Womb.next; run the real wheel.
            womb.state = native.sow.normal
            womb.risk = .2
            for mode in (0, 'always'):
                persistent.ssct_pregnancy_multiplier = mode
                game = saga.mini.womb(womb)
                game.begin()
                assert bool(game.kind) == (mode == 'always')
            state.result['native_wheel_begin'] = True
            _preg_probe_write()
        finally:
            native.random = original_random
            persistent.ssct_pregnancy_multiplier = previous

    def _preg_probe_tick(kind):
        state = sys.modules['ssct_pregnancy_probe']
        try:
            if kind in ('corp', 'gate'):
                renpy.end_interaction(None)
            elif kind == 'main_menu' and state.phase == 0:
                _preg_probe_rolls()
                persistent.pref = 'gameplay'
                persistent.ssct_pregnancy_multiplier = 1
                state.phase = 1
                renpy.run(ShowMenu('preferences'))
            elif kind == 'preferences':
                screen_name = 'my_preferences' if renpy.get_screen('my_preferences') else 'preferences'
                screen = renpy.get_screen(screen_name)
                value = renpy.get_widget(screen_name, 'ssct_pregnancy_value')
                next_button = renpy.get_widget(screen_name, 'ssct_pregnancy_next')
                prev_button = renpy.get_widget(screen_name, 'ssct_pregnancy_previous')
                assert value and next_button and prev_button, 'Missing rendered multiplier widgets'
                mode = _ssct_pregnancy_mode()
                label = _ssct_pregnancy_text(_ssct_pregnancy_names[mode])
                assert label in ''.join(value.text), (label, value.text)
                widgets = []
                screen.visit_all(widgets.append)
                value_button = next(node for node in widgets if isinstance(getattr(node, 'clicked', None), NullAction) and getattr(node, 'child', None) is value)
                assert getattr(value_button, '_tooltip', None) is None
                tip = _ssct_pregnancy_text(_ssct_pregnancy_tips[mode])
                state.result['ui'].append({'phase': state.phase, 'language': _preferences.language,
                    'mode': mode, 'label': label, 'tooltip': tip})
                if state.phase == 1:
                    assert mode == 1
                    state.phase = 2
                    renpy.run(next_button.clicked)
                elif state.phase == 2:
                    assert mode == 2
                    state.phase = 3
                    renpy.run(next_button.clicked)
                elif state.phase == 3:
                    assert mode == 'always'
                    state.phase = 4
                    renpy.run(next_button.clicked)
                elif state.phase == 4:
                    assert mode == 0
                    state.phase = 5
                    renpy.run(next_button.clicked)
                elif state.phase == 5:
                    assert mode == .5
                    state.phase = 6
                    renpy.change_language('zh_hans')
                elif state.phase == 6:
                    assert mode == .5 and '一半' in label
                    state.phase = 7
                    renpy.run(prev_button.clicked)
                elif state.phase == 7:
                    assert mode == 0 and '阻断部分任务' in tip
                    # Focus the actual button to run its hover action.
                    import renpy.display.focus as focus
                    focus.change_focus(focus.Focus(value_button, None, 0, 0, 10, 10, screen), default=False)
                    state.phase = 8
                    renpy.restart_interaction()
                elif state.phase == 8:
                    hint = renpy.get_screen('ssct_pregnancy_hint')
                    assert hint and hint.zorder == 200
                    hint_text = renpy.get_widget('ssct_pregnancy_hint', 'ssct_pregnancy_hint_text')
                    assert tip in ''.join(hint_text.text)
                    state.result['hint_above_settings'] = True
                    import renpy.display.focus as focus
                    anchor = tuple(hint.scope['anchor_rect'])
                    arrow_rect = next((item.x, item.y, item.w, item.h) for item in focus.focus_list if item.widget is next_button)
                    assert anchor == arrow_rect
                    stage = getattr(state, 'hint_focus_stage', 0)
                    if stage == 0:
                        state.hint_anchor = anchor
                    assert anchor == state.hint_anchor
                    if stage < 2:
                        state.hint_focus_stage = stage + 1
                        widget = (prev_button, next_button)[stage]
                        focus.change_focus(focus.Focus(widget, None, 0, 0, 10, 10, screen), default=False)
                        renpy.restart_interaction()
                        return
                    state.result['hint_anchor_is_right_arrow'] = True
                    state.result['hint_anchor_unchanged_across_controls'] = True
                    state.result['hint_anchor_rect'] = anchor
                    renpy.screenshot(os.path.join(config.basedir, 'pregnancy_probe_zh_0.png'))
                    state.phase = 9
                    renpy.run(value_button.unhovered)
                    renpy.run(prev_button.clicked)
                elif state.phase == 9:
                    assert mode == 'always'
                    assert not renpy.get_screen('ssct_pregnancy_hint')
                    state.result['hint_hidden_on_unhover'] = True
                    state.phase = 9.5
                    import renpy.display.focus as focus
                    focus.change_focus(focus.Focus(value_button, None, 0, 0, 10, 10, screen), default=False)
                    renpy.restart_interaction()
                elif state.phase == 9.5:
                    assert mode == 'always'
                    hint_text = renpy.get_widget('ssct_pregnancy_hint', 'ssct_pregnancy_hint_text')
                    assert tip in ''.join(hint_text.text)
                    renpy.screenshot(os.path.join(config.basedir, 'pregnancy_probe_zh_always.png'))
                    state.result['guaranteed_hint_rendered'] = True
                    state.phase = 10
                    renpy.run(value_button.unhovered)
                    renpy.run(prev_button.clicked)
                elif state.phase == 10:
                    assert mode == 2
                    state.phase = 11
                    renpy.run(prev_button.clicked)
                elif state.phase == 11:
                    assert mode == 1
                    state.phase = 12
                    renpy.run(prev_button.clicked)
                elif state.phase == 12:
                    assert mode == .5
                    state.phase = 13
                    renpy.restart_interaction()
                elif state.phase == 13:
                    renpy.screenshot(os.path.join(config.basedir, 'pregnancy_probe_zh_half.png'))
                    state.preview_index = 0
                    state.result['tooltip_previews'] = []
                    persistent.ssct_pregnancy_multiplier = _ssct_pregnancy_modes[0]
                    state.phase = 14
                    renpy.restart_interaction()
                elif state.phase == 14:
                    import renpy.display.focus as focus
                    focus.change_focus(None, default=False)
                    focus.change_focus(focus.Focus(value_button, None, 0, 0, 10, 10, screen), default=False)
                    state.phase = 15
                    renpy.restart_interaction()
                elif state.phase == 15:
                    hint = renpy.get_screen('ssct_pregnancy_hint')
                    assert hint and hint.zorder == 200
                    hint_text = renpy.get_widget('ssct_pregnancy_hint', 'ssct_pregnancy_hint_text')
                    assert tip in ''.join(hint_text.text)
                    language = 'zh' if _preferences.language == 'zh_hans' else 'en'
                    mode_name = {0: '0', .5: 'half', 1: '1', 2: '2', 'always': 'always'}[mode]
                    filename = 'pregnancy_tip_%s_%s.png' % (language, mode_name)
                    renpy.screenshot(os.path.join(config.basedir, filename))
                    state.result['tooltip_previews'].append({'language': language, 'mode': mode,
                        'tooltip': tip, 'screenshot': filename})
                    renpy.run(value_button.unhovered)
                    state.preview_index += 1
                    if state.preview_index < 10:
                        persistent.ssct_pregnancy_multiplier = _ssct_pregnancy_modes[state.preview_index % 5]
                        if state.preview_index == 5:
                            renpy.change_language(None)
                        state.phase = 14
                        renpy.restart_interaction()
                        return
                    state.result['passed'] = True
                    state.result['scope'] = 'Native deterministic conception rolls, wheel.begin, rendered preference actions and bilingual tooltips; not complete quest playthroughs or physical mouse input.'
                    _preg_probe_write()
                    renpy.quit(save=False)
        except renpy.game.QuitException:
            raise
        except Exception:
            import traceback
            state.result['error'] = traceback.format_exc()
            _preg_probe_write()
            renpy.quit(save=False)

    import renpy.display.screen as _preg_screens

    def _preg_probe_periodic():
        if renpy.get_screen('preferences') or renpy.get_screen('my_preferences'):
            _preg_probe_tick('preferences')
    config.periodic_callback = _preg_probe_periodic

label ssct_pregnancy_probe_splash:
    $ renpy.execute_default_statement(True)
    call _start_store
    $ _init_language()
    python:
        _preg_probe_rolls()
        persistent.pref = 'gameplay'
        persistent.ssct_pregnancy_multiplier = 1
        sys.modules['ssct_pregnancy_probe'].phase = 1
    call screen preferences
    $ renpy.quit(save=False)
