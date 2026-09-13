# Summertime Saga 21.0.0 性爱动画速度控制
#
# 将此文件安装为 game/sex_speed_control.rpy
# 按钮标签使用 Unicode 转义，确保此文件在不同 Windows 区域设置下安全复制。
#
# 进入或离开色情菜单时，速度级别重置为 1.00 倍
# 使用游戏风格的 0.67x / 0.83x / 1.00x / 1.25x 递进

# 使用较高的 init 偏移量，确保此屏幕定义在游戏存档中的原始 screen lewd 之后注册
init offset = 999

init python:
    import saga.display.anim as _sms_anim

    # 0 = 0.67x，1 = 0.83x，2 = 1.00x，3 = 1.25x
    _sms_speed_levels = (0.67, 0.83, 1.0, 1.25)
    # 英文字符串作为后备。当存在匹配的 `translate <language> strings` 块时，
    # 当前 Ren'Py 语言会翻译它们
    _sms_speed_names = ("slow", "slightly slower", "normal", "fast")
    _sms_speed_state = {"index": 2}
    _sms_base_fps = {}

    def _sms_speed_index():
        try:
            value = int(_sms_speed_state.get("index", 2))
        except Exception:
            value = 2

        value = max(0, min(len(_sms_speed_levels) - 1, value))
        _sms_speed_state["index"] = value
        return value

    def _sms_apply_animation_speed():
        """将选中的速度应用到当前缓存中的动画。"""
        factor = _sms_speed_levels[_sms_speed_index()]
        cache = getattr(_sms_anim, "cache", None)
        if not cache:
            return

        # 在游戏入口对象之外保存原始 fps。入口类使用 slots，因此向其添加自定义属性不可靠
        for key, entry in tuple(cache.items()):
            try:
                fps = entry.fps
            except Exception:
                continue

            if not isinstance(fps, (int, float)) or fps <= 0:
                continue

            base = _sms_base_fps.get(key)
            if base is None:
                base = fps
                _sms_base_fps[key] = base

            try:
                # 原生 update() 会保持当前动画帧不变
                entry.update(base * factor)
            except Exception:
                pass

    def _sms_reset_animation_speed():
        # 将临时场景设置重置为正常的 1.00 倍速度
        _sms_speed_state["index"] = 2
        _sms_apply_animation_speed()

    def _sms_change_animation_speed(delta):
        index = _sms_speed_index()
        _sms_speed_state["index"] = max(
            0, min(len(_sms_speed_levels) - 1, index + delta))
        _sms_apply_animation_speed()
        renpy.restart_interaction()

    def _sms_speed_label():
        # 保留本地化，以防再次启用可选的状态文本
        name = _(_sms_speed_names[_sms_speed_index()])
        return _("Animation speed: ") + "{:.2f}x ({})".format(
            _sms_speed_levels[_sms_speed_index()], name)


# 重写原始 screen lewd，保留所有原始菜单操作不变
# 在现有选项窗口的两侧各添加一个速度按钮
screen lewd(items):
    style_prefix 'lewd'

    # 每个新动画场景都以正常速度开始
    on "show" action Function(_sms_reset_animation_speed)
    # 离开场景时也清除临时速度选择
    on "hide" action Function(_sms_reset_animation_speed)

    vbox:
        hbox:
            xalign .5
            spacing 12

            textbutton _("Slower"):
                action Function(_sms_change_animation_speed, -1)
                sensitive _sms_speed_index() > 0

            window:
                has grid len(items) 1

                for i in items:
                    textbutton i.caption action i.action

            textbutton _("Faster"):
                action Function(_sms_change_animation_speed, 1)
                sensitive _sms_speed_index() < len(_sms_speed_levels) - 1

        # 底部速度状态文本暂时隐藏：
        # text "[_sms_speed_label()]" style_suffix "speed_label"


# style lewd_speed_label:
#     xalign .5
#     top_margin 4
#     bottom_margin 2
#     color '#cccccc'
#     size 20

# 默认语言为英语。当玩家选择此安装的简体中文（zh_hans）时，会自动选中此翻译块
translate zh_hans strings:
    old "Slower"
    new "慢一点"

    old "Faster"
    new "快一点"

    old "slow"
    new "慢"

    old "slightly slower"
    new "\u7a0d慢"

    old "normal"
    new "标准"

    old "fast"
    new "快"

    old "Animation speed: "
    new "动画速度："