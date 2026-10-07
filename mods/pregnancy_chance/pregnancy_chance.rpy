# Scale the shared native conception roll without changing saved womb objects.
default persistent.ssct_pregnancy_multiplier = 1

init 998 python:
    _ssct_pregnancy_modes = (0, .5, 1, 2, 'always')
    _ssct_pregnancy_names = {
        0: '0x - No pregnancy', .5: '0.5x - Half chance', 1: '1x - Original chance',
        2: '2x - Double chance', 'always': u'∞x - Guaranteed pregnancy',
    }
    _ssct_pregnancy_tips = {
        0: "Your swimmers are sightseeing, not settling down. The worried can relax; the hopeful can keep hoping. Hold off on the crib shopping and the cover stories.\n\nPregnancy chance is zero. (This option may block progress in some quests. Switch to another multiplier and try again.)",
        .5: "Your swimmers have gone part-time. Hoping for a baby? It may take more tries. Hoping to avoid one? Hold the champagne. They're working less, not quitting.\n\nPregnancy chance is half the original.",
        1: "The classic 'It probably won't happen.' Someone's hoping for a miracle, someone's preparing a cover story. Your luck stays the same. So does your talent for playing innocent afterwards.\n\nUses the original pregnancy chance.",
        2: "Your swimmers are out to prove themselves. 'Let's try again' is more likely to become 'We'll need another crib.' Double the chance, not a twins meal deal.\n\nPregnancy chance is doubled, capped at 100%.",
        'always': "The town's fertility miracles are now available wholesale. Hoping for good news? Start picking names. Dreading a surprise? Start picking excuses. And you? Stop acting like nobody told you what sperm does.\n\nEvery eligible native conception attempt succeeds. Existing pregnancies and other native restrictions still apply.",
    }

    def _ssct_pregnancy_text(value):
        return renpy.translate_string(value + '{#ssct_pregnancy}').replace('{#ssct_pregnancy}', '')

    def _ssct_pregnancy_mode():
        value = persistent.ssct_pregnancy_multiplier
        return value if value in _ssct_pregnancy_modes else 1

    def _ssct_pregnancy_cycle(direction):
        index = _ssct_pregnancy_modes.index(_ssct_pregnancy_mode())
        persistent.ssct_pregnancy_multiplier = _ssct_pregnancy_modes[(index + direction) % len(_ssct_pregnancy_modes)]
        renpy.restart_interaction()

    def _ssct_pregnancy_show_hint():
        # Always anchor to the right arrow's rendered focus rectangle.
        # Hovering the label or left arrow must not move the hint.
        import renpy.display.focus as focus
        screen_name = 'my_preferences' if renpy.get_screen('my_preferences') else 'preferences'
        button = renpy.get_widget(screen_name, 'ssct_pregnancy_next')
        for item in focus.focus_list:
            if item.widget is button and item.x is not None:
                renpy.show_screen('ssct_pregnancy_hint', anchor_rect=(item.x, item.y, item.w, item.h))
                renpy.restart_interaction()
                return

    class _SSCTPregnancyRoll:
        # Only the roll reads this proxy; the native object's risk is never written.
        def __init__(self, womb, risk):
            self._womb = womb
            self.risk = risk

        def __getattr__(self, name):
            return getattr(self._womb, name)

    def _ssct_pregnancy_next(womb):
        mode = _ssct_pregnancy_mode()
        if mode == 1:
            return _ssct_pregnancy_original_next(womb)
        risk = 1.0 if mode == 'always' else min(1.0, max(0.0, womb.risk * mode))
        return _ssct_pregnancy_original_next(_SSCTPregnancyRoll(womb, risk))

    def _ssct_pregnancy_nodes(node):
        yield node
        for child in getattr(node, 'children', ()):
            for item in _ssct_pregnancy_nodes(child):
                yield item
        block = getattr(node, 'block', None)
        if block is not None:
            for item in _ssct_pregnancy_nodes(block):
                yield item
        for condition, block in getattr(node, 'entries', ()):
            for item in _ssct_pregnancy_nodes(block):
                yield item

    def _ssct_pregnancy_install(screen, rows):
        if getattr(screen, '_ssct_pregnancy_installed', False):
            return True
        matches = []
        for node in _ssct_pregnancy_nodes(screen):
            children = getattr(node, 'children', ())
            for index, child in enumerate(children):
                if (getattr(child, 'name', None) == 'text'
                        and "Reveal pregnancy" in str(getattr(child, 'positional', ()))
                        and index > 0 and getattr(children[index - 1], 'target', None) == 'cycle'):
                    matches.append((node, index))
        if len(matches) != 1:
            return False
        import copy
        node, index = matches[0]
        node.children[index:index] = copy.deepcopy(rows)
        screen._ssct_pregnancy_installed = True
        return True

init 999 python:
    import saga.obgyn as _ssct_pregnancy_native
    import renpy.display.screen as _ssct_pregnancy_screens
    _ssct_pregnancy_original_next = _ssct_pregnancy_native.Womb.next
    _ssct_pregnancy_native.Womb.next = _ssct_pregnancy_next
    _ssct_pregnancy_rows = _ssct_pregnancy_screens.screens[('ssct_pregnancy_template', None)].function.children
    for (_ssct_pregnancy_name, _ssct_pregnancy_variant), _ssct_pregnancy_screen in tuple(_ssct_pregnancy_screens.screens.items()):
        if _ssct_pregnancy_name == 'preferences':
            if not _ssct_pregnancy_install(_ssct_pregnancy_screen.function, _ssct_pregnancy_rows):
                renpy.log('Pregnancy chance: incompatible preferences layout; multiplier control could not be inserted.')

screen ssct_pregnancy_template():
    text _ssct_pregnancy_text('Pregnancy chance')
    use ssct_pregnancy_control

screen ssct_pregnancy_control():
    $ ssct_mode = _ssct_pregnancy_mode()
    $ ssct_tip = _ssct_pregnancy_text(_ssct_pregnancy_tips[ssct_mode])
    side 'l c r':
        style_prefix 'pref_menu'
        style_suffix 'cycle'
        imagebutton:
            id 'ssct_pregnancy_previous'
            idle gui.left
            action Function(_ssct_pregnancy_cycle, -1)
            at button
            hovered Function(_ssct_pregnancy_show_hint)
            unhovered Hide('ssct_pregnancy_hint')
            alt _ssct_pregnancy_text('Previous pregnancy multiplier')
        textbutton _ssct_pregnancy_text(_ssct_pregnancy_names[ssct_mode]):
            id 'ssct_pregnancy_value'
            text_style 'pref_menu_text'
            action NullAction()
            selected False
            xalign .5
            hovered Function(_ssct_pregnancy_show_hint)
            unhovered Hide('ssct_pregnancy_hint')
            alt _ssct_pregnancy_text(_ssct_pregnancy_names[ssct_mode]) + '. ' + ssct_tip
        imagebutton:
            id 'ssct_pregnancy_next'
            idle gui.right
            action Function(_ssct_pregnancy_cycle, 1)
            at button
            hovered Function(_ssct_pregnancy_show_hint)
            unhovered Hide('ssct_pregnancy_hint')
            alt _ssct_pregnancy_text('Next pregnancy multiplier')

screen ssct_pregnancy_hint(anchor_rect):
    zorder 200
    if renpy.get_screen('preferences') or renpy.get_screen('my_preferences'):
        nearrect:
            rect anchor_rect
            frame:
                id 'ssct_pregnancy_hint_panel'
                style 'pref_menu_tooltip'
                background Solid('#101722')
                foreground gui.frame
                text _ssct_pregnancy_text(_ssct_pregnancy_tips[_ssct_pregnancy_mode()]):
                    id 'ssct_pregnancy_hint_text'
                    style 'pref_menu_tip'
                    color '#ffffff'
    else:
        timer .01 action Hide('ssct_pregnancy_hint')

translate zh_hans strings:
    old "Pregnancy chance{#ssct_pregnancy}"
    new "怀孕概率{#ssct_pregnancy}"

    old "0x - No pregnancy{#ssct_pregnancy}"
    new "0x - 内射不怀孕{#ssct_pregnancy}"

    old "1x - Original chance{#ssct_pregnancy}"
    new "1x - 原始怀孕概率{#ssct_pregnancy}"

    old "0.5x - Half chance{#ssct_pregnancy}"
    new "0.5x - 一半怀孕概率{#ssct_pregnancy}"

    old "Your swimmers have gone part-time. Hoping for a baby? It may take more tries. Hoping to avoid one? Hold the champagne. They're working less, not quitting.\n\nPregnancy chance is half the original.{#ssct_pregnancy}"
    new "小蝌蚪改上半天班。盼孩子的可能得多试几次，怕意外的可别先开香槟——它们只是少干活，还没辞职。\n\n怀孕概率为原版的一半。{#ssct_pregnancy}"

    old "2x - Double chance{#ssct_pregnancy}"
    new "2x - 双倍怀孕概率{#ssct_pregnancy}"

    old "∞x - Guaranteed pregnancy{#ssct_pregnancy}"
    new "∞x - 必定怀孕{#ssct_pregnancy}"

    old "Your swimmers are sightseeing, not settling down. The worried can relax; the hopeful can keep hoping. Hold off on the crib shopping and the cover stories.\n\nPregnancy chance is zero. (This option may block progress in some quests. Switch to another multiplier and try again.){#ssct_pregnancy}"
    new "小蝌蚪只参观，不落户。该松口气的松口气，该等好消息的继续等——婴儿床先别买，借口也先别编。\n\n怀孕概率为0。（该选项可能会阻断部分任务进行，切换至其他倍率后重新尝试。）{#ssct_pregnancy}"

    old "The classic 'It probably won't happen.' Someone's hoping for a miracle, someone's preparing a cover story. Your luck stays the same. So does your talent for playing innocent afterwards.\n\nUses the original pregnancy chance.{#ssct_pregnancy}"
    new "原汁原味的“应该不会吧”。有人盼着奇迹，有人备着借口。你的运气照旧，事后装傻的功夫也照旧。\n\n使用原版怀孕概率。{#ssct_pregnancy}"

    old "Your swimmers are out to prove themselves. 'Let's try again' is more likely to become 'We'll need another crib.' Double the chance, not a twins meal deal.\n\nPregnancy chance is doubled, capped at 100%.{#ssct_pregnancy}"
    new "小蝌蚪开始抢着立功了。“再试一次”更容易变成“再买张婴儿床”。先说清楚：双倍概率，不是双胞胎套餐。\n\n原版怀孕概率翻倍，最高100%。{#ssct_pregnancy}"

    old "The town's fertility miracles are now available wholesale. Hoping for good news? Start picking names. Dreading a surprise? Start picking excuses. And you? Stop acting like nobody told you what sperm does.\n\nEvery eligible native conception attempt succeeds. Existing pregnancies and other native restrictions still apply.{#ssct_pregnancy}"
    new "本镇的生育奇迹，现在归你批发。等好消息的可以开始想名字了，怕出意外的可以开始想借口了——至于你，别再装作第一次听说精子是干什么的。\n\n原版允许受孕时必定成功；已有孕期等限制照常生效。{#ssct_pregnancy}"

    old "Previous pregnancy multiplier{#ssct_pregnancy}"
    new "上一档怀孕倍率{#ssct_pregnancy}"

    old "Next pregnancy multiplier{#ssct_pregnancy}"
    new "下一档怀孕倍率{#ssct_pregnancy}"
