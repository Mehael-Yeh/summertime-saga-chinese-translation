translate zh_hans python:
    # 中文字体缺少原版UI符号；仅将缺字交给引擎自带字体，其余字符保持原字体。
    def _ssct_symbol_font(path, music=False):
        group = FontGroup().add(path, None, None)
        for codepoint in (0x25b8, 0x2611, 0x2718) + ((0x266a,) if music else ()):
            group.add("DejaVuSans.ttf", codepoint, codepoint)
        return group

    #游戏内对话文本字体
    gui.text_font = _ssct_symbol_font("tl/zh_hans/fonts/SourceHanSansCN-Bold.ttf")
    #游戏内人物角色名称字体
    gui.name_text_font = _ssct_symbol_font("tl/zh_hans/fonts/KNMaiyuan-Regular.ttf")
    #设置页面字体
    gui.interface_text_font = _ssct_symbol_font("tl/zh_hans/fonts/MiSans-Bold.ttf", music=True)
    #系统设置字体
    gui.button_text_font = gui.interface_text_font
    #游戏内选项文本字体
    gui.choice_button_text_font = gui.text_font
    #系统默认字体
    gui.system_font = _ssct_symbol_font("tl/zh_hans/fonts/MiSans-Regular.ttf", music=True)

    # 将 acme 字体名称映射到 MiSans-Bold，覆盖所有硬编码 font 'acme' 的样式
    # 这比逐个设置 style.X.font 更可靠，因为 config.font_name_map 必定存在
    config.font_name_map['acme'] = gui.interface_text_font
