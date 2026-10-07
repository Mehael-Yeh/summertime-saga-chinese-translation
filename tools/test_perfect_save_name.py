import ast
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace


def helpers(api):
    path=Path(__file__).resolve().parents[1]/'mods/perfect_save/perfect_save.rpy'
    body=path.read_text(encoding='utf8').split('init 998 python:\n',1)[-1]
    # Extract just the name helpers from the actual production init block.
    start=body.index('    def _ssct_perfect_name_json')
    end=body.index('    def _ssct_perfect_construct',start)
    namespace={'renpy':api,'saga':SimpleNamespace(cast=SimpleNamespace(anon=SimpleNamespace(name='LiveName')))}
    exec(compile(ast.parse(textwrap.dedent(body[start:end])),str(path),'exec'),namespace)
    return namespace


class SavedNameTests(unittest.TestCase):
    def api(self,slots):
        reads=[]
        def load(slot):
            reads.append(slot)
            row=slots[slot]
            if row.get('corrupt'):raise ValueError('corrupt')
            return row.get('roots',{}),row.get('trusted',True)
        api=SimpleNamespace(list_saved_games=lambda fast:list(slots),
            slot_mtime=lambda slot:slots[slot]['time'],slot_json=lambda slot:slots[slot].get('metadata',{}),
            loadsave=SimpleNamespace(location=SimpleNamespace(load=load),loads=lambda data:(data,None)),
            savetoken=SimpleNamespace(verify_data=lambda data,signatures:signatures),log=lambda message:None)
        return api,reads

    def test_newest_slot_wins_across_pages_auto_and_quick(self):
        api,reads=self.api({'1-1':{'time':20,'metadata':{'ssct_protagonist_name':'Older'}},
            'auto-1':{'time':40,'metadata':{'ssct_protagonist_name':'玩家甲'}},
            'quick-6':{'time':30,'metadata':{'ssct_protagonist_name':'Other'}}})
        self.assertEqual(helpers(api)['_ssct_perfect_latest_name'](),'玩家甲')
        self.assertEqual(reads,[])

    def test_existing_native_save_without_metadata(self):
        api,reads=self.api({'2-4':{'time':30,'roots':{'#saga.cast.anon.name':'Legacy'}}})
        self.assertEqual(helpers(api)['_ssct_perfect_latest_name'](),'Legacy')
        self.assertEqual(reads,['2-4'])

    def test_no_saves_defaults_to_anon_not_current_game(self):
        api,_=self.api({})
        self.assertEqual(helpers(api)['_ssct_perfect_latest_name'](),'Anon')

    def test_corrupt_or_empty_newer_slot_uses_latest_readable_name(self):
        api,_=self.api({'quick-1':{'time':40,'corrupt':True},
            '1-2':{'time':30,'roots':{'#saga.cast.anon.name':'  '}},
            '1-3':{'time':20,'metadata':{'ssct_protagonist_name':'Usable'}}})
        self.assertEqual(helpers(api)['_ssct_perfect_latest_name'](),'Usable')

    def test_unknown_signer_is_not_deserialized(self):
        api,_=self.api({'1-1':{'time':10,'trusted':False}})
        api.loadsave.loads=lambda _:self.fail('Do not deserialize untrusted save')
        self.assertEqual(helpers(api)['_ssct_perfect_latest_name'](),'Anon')

    def test_save_callback_records_live_name(self):
        api,_=self.api({});namespace=helpers(api);data={}
        namespace['_ssct_perfect_name_json'](data)
        self.assertEqual(data,{'ssct_protagonist_name':'LiveName'})


if __name__=='__main__':unittest.main()
