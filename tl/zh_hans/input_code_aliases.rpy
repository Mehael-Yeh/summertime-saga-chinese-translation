# 游戏谜题输入别名；不是显示文本的全局替换。
# 维护规则：translation_context/input_codes.md
init 10 python:
    import saga.tech.computer as _zh_codes_computer

    # 按设备、原始校验键配置；不改写游戏密码或存档。
    _zh_input_code_aliases = {
        ('jenny_laptop', 'BADMONSTER'): {
            'BAD MONSTER': 'BADMONSTER',
            '坏怪物': 'BADMONSTER',
        },
    }

    class _ZhComputerAuthValue(_zh_codes_computer.UpperAuthValue):
        __slots__ = ()

        def enter(self):
            original_text = self.text
            aliases = _zh_input_code_aliases.get(('jenny_laptop', self.key), {})
            self.text = aliases.get(original_text, original_text)
            try:
                return super(_ZhComputerAuthValue, self).enter()
            finally:
                self.text = original_text

    _zh_original_computer_auth = _zh_codes_computer.Computer.auth

    def _zh_computer_auth_with_aliases(device):
        app = _zh_original_computer_auth.fget(device)
        if (device.ref, app.key) not in _zh_input_code_aliases:
            return app
        # 与7944原属性一致：自动登录/触屏不默认获取输入焦点。
        return _ZhComputerAuthValue(
            app.key, app.rv,
            default=not device.auto and not renpy.variant('touch'))

    _zh_codes_computer.Computer.auth = property(_zh_computer_auth_with_aliases)
