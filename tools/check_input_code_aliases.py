"""Isolated alias regression; optional --game-lib uses original 7944 AuthValue bytecode."""
import argparse, marshal, types, textwrap
from pathlib import Path

class IgnoreEvent(Exception):
    pass

class AuthValue:
    def __init__(self, key, rv, **kwargs):
        self.key, self.rv, self.text, self.error = key, rv, '', False
        self.default = kwargs.get('default')
    def get_text(self):
        return self.text
    def set_text(self, s):
        self.text = s.strip()
    def enter(self):
        if self.get_text() == self.key:
            return self.rv
        self.error = True
        raise IgnoreEvent()

parser = argparse.ArgumentParser()
parser.add_argument('--game-lib', type=Path)
args = parser.parse_args()
if args.game_lib:
    code = marshal.loads((args.game_lib / 'saga/store.pyc').read_bytes()[16:])
    cls = next(c for c in code.co_consts if isinstance(c, types.CodeType) and c.co_name == 'AuthValue')
    for name in ('enter', 'get_text', 'set_text'):
        c = next(c for c in cls.co_consts if isinstance(c, types.CodeType) and c.co_name == name)
        setattr(AuthValue, name, types.FunctionType(c, {'IgnoreEvent': IgnoreEvent, 'restart_interaction': lambda: None}))

class UpperAuthValue(AuthValue):
    def __init__(self, key, rv, **kwargs):
        super().__init__(key.upper(), rv, **kwargs)
    def set_text(self, s):
        super().set_text(s.upper())

class Computer:
    def __init__(self, ref, key='badmonster', auto=False):
        self.ref, self.password, self.auto = ref, key, auto
    @property
    def auth(self):
        return UpperAuthValue(self.password, {'app': 'sys', 'op': 'auth'}, default=not self.auto)

module = types.SimpleNamespace(Computer=Computer, UpperAuthValue=UpperAuthValue)
source = Path('tl/zh_hans/input_code_aliases.rpy').read_text(encoding='utf-8-sig').split('init 10 python:\n', 1)[1]
source = textwrap.dedent(source).replace('import saga.tech.computer as _zh_codes_computer', '')
ns = {'_zh_codes_computer': module, 'renpy': types.SimpleNamespace(variant=lambda _: False)}
exec(compile(source, 'input_code_aliases.rpy', 'exec'), ns)
cases = 0
for device, text, valid in [
    ('jenny_laptop', 'BADMONSTER', True), ('jenny_laptop', 'badmonster', True),
    ('jenny_laptop', 'BAD MONSTER', True), ('jenny_laptop', 'Bad Monster', True),
    ('jenny_laptop', '坏怪物', True), ('jenny_laptop', '  坏怪物  ', True),
    ('jenny_laptop', 'wrong', False), ('jenny_laptop', '', False),
    ('jenny_laptop', '坏怪', False), ('anon_pc', '坏怪物', False),
    ('anon_pc', 'BAD MONSTER', False), ('anon_pc', 'badmonster', True),
]:
    app = Computer(device).auth
    app.set_text(text)
    before = app.text
    try:
        result = app.enter()
        assert valid and result == {'app': 'sys', 'op': 'auth'}
    except IgnoreEvent:
        assert not valid and app.error
    assert app.text == before
    cases += 1
assert type(Computer('jenny_laptop', 'changed').auth) is UpperAuthValue
assert Computer('jenny_laptop', auto=True).auth.default is False
ns['renpy'].variant = lambda _: True
assert Computer('jenny_laptop').auth.default is False
for key, text, valid in [('L6bv12R', 'L6bv12R', True), ('L6bv12R', 'l6bv12r', False), ('12345', '12345', True), ('12345', '1234', False)]:
    app = AuthValue(key, 'ok'); app.set_text(text)
    try:
        assert app.enter() == 'ok' and valid
    except IgnoreEvent:
        assert not valid
    cases += 1
print('PASS:', cases, 'input cases; device/key scope, focus defaults and input restoration checked.', 'Original AuthValue bytecode used.' if args.game_lib else 'Stub base used.')
