# 8194 tel_conv screen: retain upstream two-way bubbles, media and scrolling.
# Translate the raw message before Ren'Py substitutes character references/tags.
# This screen does not change the message catalogue or saved conversations.
init -1 python:
    def _ssct_message_text(message):
        return renpy.translate_string(message)

init 1:
    screen tel_conv(what, app):
        style_prefix 'tel_conv'

        add 'art/mini/tel/misc/light.png'

        viewport as vp:
            draggable True
            mousewheel True
            scrollbars 'vertical'
            yinitial app.offset

            has window
            vbox:
                for t, mesg in what.conv(app.hdd.who):
                    if t is not None:
                        use tel_util_ago(t)

                    frame:
                        at tel_conv_mesg
                        style_prefix 'tel_conv_' + (
                            'send' if what.owner is mesg.who else 'recv')

                        if isinstance(mesg.what, str):
                            label _ssct_message_text(mesg.what)
                        else:
                            imagebutton:
                                action Emit(app='view', op='init', show=mesg)
                                at button, tel_conv_media
                                idle mesg.what

        $ vp.yadjustment.changed = app.mark
