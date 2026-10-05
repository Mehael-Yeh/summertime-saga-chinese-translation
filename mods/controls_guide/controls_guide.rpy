# Keyboard controls guide; extends the native preferences layout.
init 998 python:
    _ssct_control_rows = (
        ('Enter / Space', 'Advance dialogue'),
        ('Arrow keys', 'Move focus between available buttons'),
        ('Enter', 'Activate the focused button'),
        ('Esc', 'Open the game menu / go back'),
        ('Hold Ctrl', 'Skip dialogue while held'),
        ('Tab', 'Toggle continuous skipping'),
        ('Page Up', 'Roll back dialogue where allowed'),
        ('Page Down', 'Go forward through rollback history'),
        ('H', 'Hide / show the dialogue interface'),
        ('F / F11 / Alt+Enter', 'Toggle fullscreen'),
        ('S', 'Take a screenshot'),
        ('Delete', 'Delete the focused save slot'),
        ('V', 'Toggle self-voicing'),
        ('Shift+A', 'Open accessibility settings'),
    )
    _ssct_minigame_rows = (
        ('Arrow keys', 'Combat: enter the displayed combo'),
        ('Left / Right', 'Milking: alternate left and right'),
        ('Number keys', 'Keypads / safe: enter matching digits'),
        ('Enter', 'Keypad: confirm input'),
        ('Left / Right', 'Diary: turn pages'),
    )

    def _ssct_controls_text(text):
        return renpy.translate_string(text + "{#ssct_controls_guide}").replace("{#ssct_controls_guide}", "")

    def _ssct_controls_nodes(node):
        yield node
        for child in getattr(node, 'children', ()):
            for item in _ssct_controls_nodes(child):
                yield item
        block = getattr(node, 'block', None)
        if block is not None:
            for item in _ssct_controls_nodes(block):
                yield item
        for condition, block in getattr(node, 'entries', ()):
            for item in _ssct_controls_nodes(block):
                yield item

    def _ssct_install_controls(screen, tab, rows):
        if getattr(screen, '_ssct_controls_installed', False):
            return True
        nodes = tuple(_ssct_controls_nodes(screen))
        tabs = [node for node in nodes if getattr(node, 'name', None) == 'hbox'
                and any("SetField(persistent, 'pref', 'display')" in str(getattr(child, 'keyword', ()))
                        for child in getattr(node, 'children', ()))]
        grids = [node for node in nodes if getattr(node, 'name', None) == 'vpgrid'
                 and any("persistent.pref == 'sound'" in str(getattr(child, 'entries', ()))
                         for child in getattr(node, 'children', ()))]
        if len(tabs) != 1 or len(grids) != 1:
            return False
        import copy
        tabs[0].children.append(copy.deepcopy(tab))
        grids[0].keyword = [(key, "1 if persistent.pref == 'ssct_controls_guide' else 2" if key == 'cols' else value) for key, value in grids[0].keyword]
        grids[0].keyword.append(('id', "'ssct_controls_view'"))
        grids[0].children.append(copy.deepcopy(rows))
        screen._ssct_controls_installed = True
        return True

init 999 python:
    import renpy.display.screen as _ssct_control_screens
    _ssct_tab_node = _ssct_control_screens.screens[('ssct_controls_tab_template', None)].function.children[0]
    _ssct_rows_node = _ssct_control_screens.screens[('ssct_controls_rows_template', None)].function.children[0]
    for (_ssct_name, _ssct_variant), _ssct_screen in tuple(_ssct_control_screens.screens.items()):
        if _ssct_name == 'preferences':
            if not _ssct_install_controls(_ssct_screen.function, _ssct_tab_node, _ssct_rows_node):
                renpy.log('Controls guide: incompatible preferences layout; no settings were replaced.')
    # Return to a native settings section at startup.
    if persistent.pref == 'ssct_controls_guide':
        persistent.pref = 'display'

screen ssct_controls_tab_template():
    use ssct_controls_tab

screen ssct_controls_rows_template():
    use ssct_controls_rows

screen ssct_controls_tab():
    button:
        id 'ssct_controls_tab_button'
        style 'pref_menu_label'
        action SetField(persistent, 'pref', 'ssct_controls_guide')
        at button
        text _ssct_controls_text('Keyboard' if renpy.variant('touch') else 'Controls') style 'pref_menu_label_text'

screen ssct_controls_rows():
    if persistent.pref == 'ssct_controls_guide':
        vbox:
            spacing 12
            hbox:
                spacing 20
                label _ssct_controls_text('Key') style 'pref_menu_group' xsize 310
                label _ssct_controls_text('Action') style 'pref_menu_group' xsize 750
            for key, description in _ssct_control_rows:
                use ssct_controls_row(key, description)
            label _ssct_controls_text('Minigames') style 'pref_menu_group'
            for key, description in _ssct_minigame_rows:
                use ssct_controls_row(key, description)
            use ssct_controls_row('Notes', 'Skipping follows the unread-text and skip-after-choices settings. Some scenes and hotspots still require a mouse. Arrow keys select buttons; they do not move the character. There are no general hotkeys for quick save, quick load or auto-play.')

screen ssct_controls_row(key, description):
    hbox:
        spacing 20
        use ssct_controls_cell(key, 310)
        use ssct_controls_cell(description, 750)

screen ssct_controls_cell(value, width):
    frame:
        background Solid('#ffffff0b')
        padding (12, 10)
        xsize width
        text _ssct_controls_text(value):
            style 'pref_menu_text'
            size 28
            xmaximum width - 24


translate zh_hans strings:
    old "Controls{#ssct_controls_guide}"
    new "控制{#ssct_controls_guide}"

    old "Keyboard{#ssct_controls_guide}"
    new "键盘{#ssct_controls_guide}"

    old "Key{#ssct_controls_guide}"
    new "按键{#ssct_controls_guide}"

    old "Action{#ssct_controls_guide}"
    new "功能{#ssct_controls_guide}"

    old "Minigames{#ssct_controls_guide}"
    new "小游戏{#ssct_controls_guide}"

    old "Notes{#ssct_controls_guide}"
    new "说明{#ssct_controls_guide}"

    old "Enter / Space{#ssct_controls_guide}"
    new "Enter / 空格{#ssct_controls_guide}"

    old "Arrow keys{#ssct_controls_guide}"
    new "方向键{#ssct_controls_guide}"

    old "Hold Ctrl{#ssct_controls_guide}"
    new "按住Ctrl{#ssct_controls_guide}"

    old "Left / Right{#ssct_controls_guide}"
    new "左 / 右方向键{#ssct_controls_guide}"

    old "Number keys{#ssct_controls_guide}"
    new "数字键{#ssct_controls_guide}"

    old "Advance dialogue{#ssct_controls_guide}"
    new "推进对白{#ssct_controls_guide}"

    old "Move focus between available buttons{#ssct_controls_guide}"
    new "在可选按钮之间移动焦点{#ssct_controls_guide}"

    old "Activate the focused button{#ssct_controls_guide}"
    new "确认当前选中的按钮{#ssct_controls_guide}"

    old "Open the game menu / go back{#ssct_controls_guide}"
    new "打开游戏菜单／返回{#ssct_controls_guide}"

    old "Skip dialogue while held{#ssct_controls_guide}"
    new "按住时快进对白，松开停止{#ssct_controls_guide}"

    old "Toggle continuous skipping{#ssct_controls_guide}"
    new "开启／关闭持续快进{#ssct_controls_guide}"

    old "Roll back dialogue where allowed{#ssct_controls_guide}"
    new "回退对白（受场景限制）{#ssct_controls_guide}"

    old "Go forward through rollback history{#ssct_controls_guide}"
    new "沿回退记录向前恢复{#ssct_controls_guide}"

    old "Hide / show the dialogue interface{#ssct_controls_guide}"
    new "隐藏／恢复对白界面{#ssct_controls_guide}"

    old "Toggle fullscreen{#ssct_controls_guide}"
    new "切换全屏／窗口{#ssct_controls_guide}"

    old "Take a screenshot{#ssct_controls_guide}"
    new "截图{#ssct_controls_guide}"

    old "Delete the focused save slot{#ssct_controls_guide}"
    new "删除当前聚焦的存档{#ssct_controls_guide}"

    old "Toggle self-voicing{#ssct_controls_guide}"
    new "开启／关闭文字朗读{#ssct_controls_guide}"

    old "Open accessibility settings{#ssct_controls_guide}"
    new "打开辅助功能设置{#ssct_controls_guide}"

    old "Combat: enter the displayed combo{#ssct_controls_guide}"
    new "战斗QTE：输入画面要求的方向组合{#ssct_controls_guide}"

    old "Milking: alternate left and right{#ssct_controls_guide}"
    new "挤奶：交替按左右方向键{#ssct_controls_guide}"

    old "Keypads / safe: enter matching digits{#ssct_controls_guide}"
    new "密码键盘／保险箱：输入对应数字{#ssct_controls_guide}"

    old "Keypad: confirm input{#ssct_controls_guide}"
    new "密码键盘：确认输入{#ssct_controls_guide}"

    old "Diary: turn pages{#ssct_controls_guide}"
    new "日记：翻页{#ssct_controls_guide}"

    old "Skipping follows the unread-text and skip-after-choices settings. Some scenes and hotspots still require a mouse. Arrow keys select buttons; they do not move the character. There are no general hotkeys for quick save, quick load or auto-play.{#ssct_controls_guide}"
    new "快进受“跳过未读文本”和“选项后继续快进”设置影响。部分场景和热点仍需鼠标。方向键用于选择按钮，不用于移动人物。快速保存、快速读取和自动播放没有通用快捷键。{#ssct_controls_guide}"
