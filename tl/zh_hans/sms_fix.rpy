# 短信/UI插值后的整串翻译补丁。
# 从tl/zh_hans/extracted/下发现全部rpy，兼容松散文件和Ren’Py归档。
# 按原有安全规则跳过标签及非角色动态表达式；不执行提取文件中的代码。
# 新增分类文件无需修改加载清单；维护规则见translation_context/style_guide.md。

init -1 python:
    import re as _rb_re
    import renpy.substitutions as _rb_sub

    _rb_escape_re = _rb_re.compile(r'\\(.)')
    _rb_old_re = _rb_re.compile(r'^\s*old\s+"((?:\\.|[^"\\])*)"\s*$')
    _rb_new_re = _rb_re.compile(r'^\s*new\s+"((?:\\.|[^"\\])*)"\s*$')
    _rb_expr_re = _rb_re.compile(r'\[[^\]]*\]')
    _rb_cast_ref_re = _rb_re.compile(r'^\[saga\.cast\.[A-Za-z_][A-Za-z0-9_]*\]$')
    _rb_escape_map = {'n': '\n', 't': '\t', '\\': '\\', '"': '"'}

    def _rb_unescape(s):
        return _rb_escape_re.sub(
            lambda m: _rb_escape_map.get(m.group(1), m.group(1)), s
        )

    def _rb_sms_replace(s):
        if not isinstance(s, str):
            return s
        _rb_map = renpy.store.__dict__.get('_rb_sms_map') or {}
        if s in _rb_map:
            return _rb_map[s]
        _rb_prev = renpy.store.__dict__.get('_rb_sms_prev_replace')
        if _rb_prev is not None:
            return _rb_prev(s)
        return s

    def _rb_rebuild_sms_map():
        renpy.store._rb_sms_map = {}
        try:
            _rb_sources = []
            for _rb_path in sorted(renpy.list_files()):
                if not (_rb_path.startswith('tl/zh_hans/extracted/')
                        and _rb_path.endswith('.rpy')):
                    continue
                _rb_f = renpy.loader.load(_rb_path)
                try:
                    _rb_text = _rb_f.read()
                finally:
                    _rb_f.close()
                if isinstance(_rb_text, bytes):
                    _rb_text = _rb_text.decode('utf-8-sig', 'replace')
                _rb_sources.append(_rb_text)
            _rb_raw = '\n'.join(_rb_sources)

            _rb_pairs = []
            _rb_old = None
            for _rb_line in _rb_raw.splitlines():
                _rb_m = _rb_old_re.match(_rb_line)
                if _rb_m:
                    _rb_old = _rb_unescape(_rb_m.group(1))
                    continue
                _rb_m = _rb_new_re.match(_rb_line)
                if _rb_m and _rb_old is not None:
                    _rb_pairs.append((_rb_old, _rb_unescape(_rb_m.group(1))))
                    _rb_old = None

            for _rb_old_s, _rb_new_s in _rb_pairs:
                # 短信正文经 `text '[mesg.what!i]'` 渲染时从不走
                # translate_string，所以无论有没有 [saga.cast.X] 占位符，
                # 都要进 replace_text 映射。仅排除两类：
                # - 含 {tag} 的条目：tokenize 时被拆开，replace_text 收到
                #   的是去标签的片段，整串匹配不可靠；
                # - 含其它动态表达式（如 [renpy.random...]）的条目：
                #   提前求值有副作用，跳过。
                if '{' in _rb_old_s:
                    continue
                _rb_exprs = _rb_expr_re.findall(_rb_old_s)
                if _rb_exprs and any(
                    not _rb_cast_ref_re.match(_rb_e) for _rb_e in _rb_exprs
                ):
                    continue
                try:
                    _rb_en, _ = _rb_sub.substitute(
                        _rb_old_s, scope=None, translate=False
                    )
                    _rb_zh, _ = _rb_sub.substitute(
                        _rb_new_s, scope=None, translate=False
                    )
                except Exception:
                    continue
                if isinstance(_rb_en, str) and _rb_en and _rb_en != _rb_zh:
                    renpy.store._rb_sms_map[_rb_en] = _rb_zh
        except Exception:
            renpy.store._rb_sms_map = {}

    renpy.store._rb_sms_map = {}
    renpy.store._rb_sms_prev_replace = None


translate zh_hans python:
    # 语言激活时注册/重建（重复激活不会无限叠加包装器）
    try:
        if renpy.config.replace_text is not _rb_sms_replace:
            _rb_sms_prev_replace = renpy.config.replace_text
            renpy.config.replace_text = _rb_sms_replace
        _rb_rebuild_sms_map()
    except Exception:
        pass
