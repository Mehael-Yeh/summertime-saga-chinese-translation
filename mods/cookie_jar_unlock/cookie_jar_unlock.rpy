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

    def _ssct_cookie_jar_unlocked():
        return getattr(persistent, 'cookies', None) is True

    def _ssct_cookie_jar_button_label():
        if _ssct_cookie_jar_unlocked():
            return renpy.translate_string(_("Restore normal Cookie Jar unlocks"))
        return renpy.translate_string(_("Unlock all Cookie Jar entries"))

    def _ssct_toggle_cookie_jar():
        if not _ssct_cookie_jar_supported():
            renpy.notify(renpy.translate_string(_("This game version's Cookie Jar interface is incompatible. Unlock data was not changed.")))
            return
        # Only toggle the native override. Earned scene records stay untouched.
        persistent.cookies = not persistent.cookies
        renpy.save_persistent()
        renpy.restart_interaction()
        if persistent.cookies:
            renpy.notify(renpy.translate_string(_("All Cookie Jar entries unlocked!")))
        else:
            renpy.notify(renpy.translate_string(_("Normal Cookie Jar unlocks restored.")))

    def _ssct_attach_cookie_jar_button(original):
        def with_unlock_button(*args, **kwargs):
            original(*args, **kwargs)
            renpy.use_screen(
                'ssct_cookie_jar_unlock_button',
                _scope=kwargs.get('_scope', {}),
                # Root screens use an integer name; nested screens may use
                # tuples. Preserve either as one component of our child ID.
                _name=(kwargs.get('_name', ()), 'ssct_unlock'))
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
    textbutton ("\U0001f512" if _ssct_cookie_jar_unlocked() else "\U0001f513"):
        align (.97, .03)
        xysize (80, 80)
        padding (8, 8)
        background Solid('#0007')
        hover_background Solid('#40566ecc')
        text_font 'TwemojiCOLRv0.ttf'
        text_size 48
        text_align (.5, .5)
        alt _ssct_cookie_jar_button_label()
        tooltip _ssct_cookie_jar_button_label()
        action Function(_ssct_toggle_cookie_jar)


translate zh_hans strings:
    old "All Cookie Jar entries unlocked!"
    new "角色图鉴已全部解锁"

    old "This game version's Cookie Jar interface is incompatible. Unlock data was not changed."
    new "当前游戏版本的图鉴接口不兼容，未修改解锁数据"

    old "Unlock all Cookie Jar entries"
    new "一键解锁所有角色图鉴"

    old "Restore normal Cookie Jar unlocks"
    new "恢复角色图鉴的正常解锁状态"

    old "Normal Cookie Jar unlocks restored."
    new "角色图鉴已恢复正常解锁状态"
