import ast
import functools
from pathlib import Path
from types import SimpleNamespace, ModuleType
import textwrap
import unittest

class Actor:
    ref='actor'

actor=Actor()
clock=SimpleNamespace(date=1)
pool={actor:ModuleType('native_actor')}

def native_activity(verb, owner=None):
    date=clock.date
    previous=getattr(owner,verb,-1)
    setattr(owner,verb,date)
    return previous

def native_registry(verb):
    date=clock.date
    owner=next(iter(pool))
    previous=getattr(owner,verb,-1)
    setattr(owner,verb,date)
    return previous

def native_deadline(verb, owner=None):
    previous=getattr(owner,verb,-1)
    setattr(owner,verb,clock.date+3)
    return previous

class NativePartial:
    def __init__(self,fn,*args,**keywords):
        self.func,self.args,self.keywords=fn,args,keywords

def parser():
    path=Path(__file__).resolve().parents[1]/'mods/perfect_save/completion_state.rpy'
    body=path.read_text(encoding='utf8').split('init 997 python:\n',1)[1]
    module=ast.parse(textwrap.dedent(body))
    module.body=[x for x in module.body if isinstance(x,ast.FunctionDef) and x.name=='_ssct_completion_activity_dates']
    namespace={}
    exec(compile(module,str(path),'exec'),namespace)
    return namespace['_ssct_completion_activity_dates']

class ActivityDates(unittest.TestCase):
    def setUp(self):
        self.parse=parser()
        self.catalogues=dict(cast=[actor],prop=[],sets=[],flow=[])

    def test_native_partial_is_not_required_to_be_functools_partial(self):
        rows=self.parse(NativePartial(native_activity,'visit',owner=actor),self.catalogues,clock)
        self.assertEqual(rows,[(actor,'visit',-1)])
        self.assertFalse(hasattr(actor,'visit'))

    def test_runtime_actor_registry_not_character_names(self):
        rows=self.parse(functools.partial(native_registry,'activity'),self.catalogues,clock)
        self.assertEqual(rows,[(actor,'activity',-1)])

    def test_future_deadline_is_not_backdated(self):
        self.assertEqual(self.parse(functools.partial(native_deadline,'deadline',owner=actor),self.catalogues,clock),[])

    def test_engine_revertable_dict_alias_keeps_builtin_registry(self):
        class EngineDict(dict):pass
        self.parse.__globals__['dict']=EngineDict
        self.assertEqual(self.parse(functools.partial(native_registry,'activity'),self.catalogues,clock),[(actor,'activity',-1)])

if __name__=='__main__':unittest.main()
