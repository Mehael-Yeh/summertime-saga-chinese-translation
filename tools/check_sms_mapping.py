"""Isolated regression check for extracted-string SMS loading; no game is run."""
from pathlib import Path
from types import ModuleType, SimpleNamespace
import io
import re
import sys
import textwrap
from validate_translations import iter_pairs

root = Path(__file__).resolve().parents[1]
files = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / 'tl/zh_hans/extracted').glob('*.rpy')}
loaded = []
def load(name):
    loaded.append(name)
    return io.BytesIO(files[name])
def substitute(value, **kwargs):
    return re.sub(r'\[saga\.cast\.([A-Za-z_]\w*)\]', lambda m: 'Name_' + m[1], value), False

renpy = ModuleType('renpy')
sub = ModuleType('renpy.substitutions')
sub.substitute = substitute
renpy.substitutions = sub
renpy.store = SimpleNamespace()
renpy.loader = SimpleNamespace(load=load)
renpy.list_files = lambda: list(files) + ['tl/zh_hans/unrelated.rpy', 'art/test.png']
sys.modules['renpy'] = renpy
sys.modules['renpy.substitutions'] = sub
code = (root / 'tl/zh_hans/sms_fix.rpy').read_text(encoding='utf-8-sig')
block = code.split('init -1 python:\n', 1)[1].split('\ntranslate zh_hans python:', 1)[0]
env = {'renpy': renpy}
exec(compile(textwrap.dedent(block), 'sms_fix.rpy:init', 'exec'), env)
env['_rb_rebuild_sms_map']()
assert set(loaded) == set(files), 'Did not load exactly the extracted files'
expected = {}
for content in files.values():
    for pair in iter_pairs(content.decode('utf-8-sig').splitlines()):
        source, target = map(env['_rb_unescape'], (pair.source, pair.target))
        refs = env['_rb_expr_re'].findall(source)
        if '{' in source or any(not env['_rb_cast_ref_re'].match(x) for x in refs):
            continue
        en, zh = substitute(source)[0], substitute(target)[0]
        if en and en != zh:
            expected[en] = zh
assert renpy.store._rb_sms_map == expected
messages = list(iter_pairs(files['tl/zh_hans/extracted/mesg.rpy'].decode('utf-8-sig').splitlines()))
for pair in messages:
    source, target = map(env['_rb_unescape'], (pair.source, pair.target))
    assert env['_rb_sms_replace'](substitute(source)[0]) == substitute(target)[0]
renpy.store._rb_sms_prev_replace = lambda value: 'fallback:' + value
assert env['_rb_sms_replace']('unmatched') == 'fallback:unmatched'
files['tl/zh_hans/extracted/future.rpy'] = b'translate zh_hans strings:\n    old "Future notice"\n    new "Future translated"\n'
env['_rb_rebuild_sms_map']()
assert env['_rb_sms_replace']('Future notice') == 'Future translated'
assert len(renpy.store._rb_sms_map) == len(expected) + 1
print(f'OK: {len(messages)} SMS translations; {len(expected)} mappings; archive-like reads, future category, fallback verified.')
