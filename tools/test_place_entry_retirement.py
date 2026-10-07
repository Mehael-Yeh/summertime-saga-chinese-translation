import ast,textwrap,unittest,sys
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

class Label:
    def __init__(self,block):self.block=block
class Scene:pass
class Say:pass
class Return:
    expression=None
class Python:pass

class EntryRetirement(unittest.TestCase):
    def setUp(self):
        self.clear=object()
        self.abort=object()
        def native_req(*args):raise AssertionError('Projection must not run native predicates')
        self.native_req=native_req
        self.place=NS(ref='room')
        self.player=NS(ref='player')
        self.other=NS(ref='npc')
        def native_call(label):raise AssertionError('Callbacks must never run during projection')
        self.native_call=native_call
        source=Path(__file__).resolve().parents[1]/'mods/perfect_save/completion_state.rpy'
        tree=ast.parse(textwrap.dedent(source.read_text(encoding='utf8').split('init 997 python:\n',1)[1]))
        function=next(node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='_ssct_completion_place_entries')
        namespace={'saga':NS(sets=[self.place],cast=NS(anon=self.player)),
            'renpy':NS(ast=NS(Label=Label,Scene=Scene,Say=Say,Return=Return),
                game=NS(script=NS(namemap={'intro':Label([Scene(),Say(),Return()])})))}
        exec(compile(ast.Module(body=[function],type_ignores=[]),str(source),'exec'),namespace)
        self.run_projection=namespace['_ssct_completion_place_entries']
        self.namespace=namespace
        callbacks={'call':native_call,'clear':self.clear}
        exec("def enter():\n call('intro')\n return clear\n",callbacks)
        self.callback=callbacks['enter']
        self.modules=patch.dict(sys.modules,{'saga.event':NS(call=native_call),'saga.util.sentinel':NS(clear=self.clear,abort=self.abort),'saga.logic.util':NS(req=native_req)})
        self.modules.start()
        self.addCleanup(self.modules.stop)

    def project(self,event):
        model={'listeners':{},'sources':[]}
        node=NS(ref='independent',pool=[(self.callback,frozenset(event.items()),None,1)])
        self.run_projection(model,[node])
        return model

    def test_native_enter_clear_retires_whole_observer(self):
        # Native catalogue entities are identity-hashable.
        self.place=type('Place',(),{'ref':'room'})()
        self.player=type('Actor',(),{'ref':'player'})()
        self.namespace['saga']=NS(sets=[self.place],cast=NS(anon=self.player))
        model=self.project({'enter':self.place,'what':self.player})
        self.assertFalse(model['listeners'][('step','independent')])
        self.assertEqual(model['place_entry_retirements'][0]['place'],'room')

    def test_script_state_effect_cannot_be_silently_retired(self):
        self.namespace['renpy'].game.script.namemap['intro'].block.append(Python())
        self.place=type('Place',(),{'ref':'room'})()
        self.player=type('Actor',(),{'ref':'player'})()
        self.namespace['saga']=NS(sets=[self.place],cast=NS(anon=self.player))
        self.assertEqual(self.project({'enter':self.place,'who':self.player})['listeners'],{})

    def test_repeat_clear_without_enter_contract_stays_active(self):
        self.assertEqual(self.project({})['listeners'],{})

    def test_presence_guarded_one_off_interaction_retires_without_running_predicate(self):
        self.place=type('Place',(),{'ref':'room'})()
        self.player=type('Actor',(),{'ref':'player'})()
        cast=NS(anon=self.player)
        sets=NS(room=self.place)
        self.namespace['saga']=NS(sets=type('Catalogue',(),{'__iter__':lambda obj:iter([self.place]),'room':self.place})(),cast=cast)
        callbacks={'call':self.native_call,'clear':self.clear,'abort':self.abort,
                   'req':self.native_req,'cast':cast,'sets':self.namespace['saga'].sets}
        exec("def once():\n ok=req(cast.anon,sets.room)\n if not ok:return\n call('intro')\n return abort,clear\n",callbacks)
        self.callback=callbacks['once']
        self.assertFalse(self.project({'interact':self.place})['listeners'][('step','independent')])

    def test_mutating_callback_cannot_be_classified_as_presentation_only(self):
        callbacks={'call':self.native_call,'clear':self.clear}
        exec("def once():\n owner.flag=True\n call('intro')\n return clear\n",callbacks)
        self.callback=callbacks['once']
        self.place=type('Place',(),{'ref':'room'})()
        self.namespace['saga'].sets=[self.place]
        self.assertEqual(self.project({'interact':self.place})['listeners'],{})

if __name__=='__main__':unittest.main()
