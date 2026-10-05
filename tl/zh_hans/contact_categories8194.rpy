# 8194 tel_cast screen: retain upstream cards, names, actions and scrolling.
# Translate display categories only; keep who.type and asset/style keys unchanged.
init -1 python:
    def _ssct_contact_category(category):
        source = category.capitalize()
        if category not in ('home', 'student', 'teacher', 'town', 'monster', 'villain'):
            return source
        return renpy.translate_string(source + '{#ssct_contact_type}').split('{#', 1)[0]

init 1:
    screen tel_cast(what, app):
        style_prefix 'tel_cast'

        default data = what.cast

        add 'art/mini/tel/misc/dark.png'

        vpgrid as vp:
            cols 2
            draggable True
            mousewheel bool(data)
            scrollbars ('vertical' if data else None)
            yinitial app.offset

            for who in data:
                button:
                    action Emit(app='info', op='init', who=who)
                    at button

                    has fixed

                    add f'art/mini/tel/cast/{who.type}.png'
                    add f'menu_cast_{who.ref}_face' pos (20, 15) zoom .52536

                    text '[who]' style_suffix f'name_{who.type}'
                    text _ssct_contact_category(who.type) style_suffix f'type_{who.type}'

        $ vp.yadjustment.changed = app.mark

translate zh_hans strings:

    # game/src/gui/tel.rpy:87 (dynamic contact category)
    old "Home{#ssct_contact_type}"
    new "家人{#ssct_contact_type}"

    # game/src/gui/tel.rpy:87 (dynamic contact category)
    old "Student{#ssct_contact_type}"
    new "学生{#ssct_contact_type}"

    # game/src/gui/tel.rpy:87 (dynamic contact category)
    old "Teacher{#ssct_contact_type}"
    new "教师{#ssct_contact_type}"

    # game/src/gui/tel.rpy:87 (dynamic contact category)
    old "Town{#ssct_contact_type}"
    new "镇民{#ssct_contact_type}"

    # game/src/gui/tel.rpy:87 (dynamic contact category)
    old "Monster{#ssct_contact_type}"
    new "怪物{#ssct_contact_type}"

    # game/src/gui/tel.rpy:87 (dynamic contact category)
    old "Villain{#ssct_contact_type}"
    new "反派{#ssct_contact_type}"
