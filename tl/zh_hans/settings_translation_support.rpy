# Translate complete tooltip strings before screen text interpolation/tokenization.
init 10 python:
    _ssct_original_get_tooltip = GetTooltip

    def _ssct_translated_tooltip(*args, **kwargs):
        value = _ssct_original_get_tooltip(*args, **kwargs)
        return renpy.translate_string(value) if isinstance(value, str) else value

    GetTooltip = _ssct_translated_tooltip

translate zh_hans strings:

    old "Open the Chinese translation project on GitHub"
    new "在GitHub上打开中文翻译项目"
