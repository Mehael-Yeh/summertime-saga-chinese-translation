# Cookie Jar unlock mod. No character lists or original screens are copied.
init offset = 0

init 998 python:
    def _ssct_cookie_jar_supported():
        # Reject a removed/changed API instead of creating an unused attribute.
        try:
            return (isinstance(persistent.cookies, bool)
                    and callable(saga.menu.cast)
                    and bool(saga.lewd.intf))
        except AttributeError:
            return False

    def _ssct_unlock_cookie_jar():
        if not _ssct_cookie_jar_supported():
            renpy.notify("当前游戏版本的图鉴接口不兼容，未修改解锁数据")
            return
        persistent.cookies = True
        renpy.save_persistent()
        renpy.restart_interaction()
        renpy.notify("角色图鉴已全部解锁")

    def _ssct_attach_cookie_jar_button(original):
        def with_unlock_button(*args, **kwargs):
            original(*args, **kwargs)
            renpy.use_screen(
                'ssct_cookie_jar_unlock_button',
                _scope=kwargs.get('_scope', {}),
                _name=tuple(kwargs.get('_name', ())) + ('ssct_unlock',))
        return with_unlock_button

# Attach after normal screen registration, preserving each native variant's
# function, parameters, tag, modality and layout. Future character/scene lists
# are still supplied entirely by the game.
init 999 python:
    import renpy.display.screen as _ssct_screens
    for (_ssct_name, _ssct_variant), _ssct_screen in tuple(_ssct_screens.screens.items()):
        if _ssct_name in ('cast', 'lewd_menu'):
            _ssct_screen.function = _ssct_attach_cookie_jar_button(_ssct_screen.function)

screen ssct_cookie_jar_unlock_button():
    textbutton "\U0001f513":
        align (.97, .03)
        xysize (80, 80)
        padding (8, 8)
        background Solid('#0007')
        hover_background Solid('#40566ecc')
        text_font 'TwemojiCOLRv0.ttf'
        text_size 48
        text_align (.5, .5)
        alt "一键解锁所有角色图鉴"
        tooltip "一键解锁所有角色图鉴"
        action Function(_ssct_unlock_cookie_jar)
