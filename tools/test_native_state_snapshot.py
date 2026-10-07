import unittest
import functools
from enum import IntEnum
from native_tests.native_state_snapshot import NativeStateSnapshot


class Native:
    __module__='saga.test'


class SnapshotTests(unittest.TestCase):
    def test_nested_native_state_changes_are_observed_without_reference_change(self):
        actor=Native();actor.ref='person';actor.womb=Native();actor.womb.count=1
        catalogues={'cast':[actor]}
        reader=NativeStateSnapshot(catalogues)
        before=reader.capture(catalogues)
        actor.womb.count=2
        after=reader.capture(catalogues)
        self.assertEqual(before['facts']['cast']['person']['womb']['fields']['count'],1)
        self.assertEqual(after['facts']['cast']['person']['womb']['fields']['count'],2)

    def test_slots_are_read_but_computed_properties_never_execute(self):
        class Auxiliary:
            __module__='saga.test'
            __slots__=('stored',)
            @property
            def computed(self):raise AssertionError('No property execution')
        actor=Native();actor.ref='person';actor.data=Auxiliary();actor.data.stored=7
        result=NativeStateSnapshot({'cast':[actor]}).capture({'cast':[actor]})
        self.assertEqual(result['facts']['cast']['person']['data']['fields'],{'stored':7})

    def test_cycles_and_snapshot_budget_fail_explicitly(self):
        actor=Native();actor.ref='person';actor.data=Native();actor.data.again=actor.data
        result=NativeStateSnapshot({'cast':[actor]}).capture({'cast':[actor]})
        self.assertIn('cycle',result['facts']['cast']['person']['data']['fields']['again'])
        result=NativeStateSnapshot({'cast':[actor]},max_values=1).capture({'cast':[actor]})
        self.assertIn('snapshot_budget',result['unknown'])

    def test_enum_and_reference_mapping_keys_preserve_nested_values(self):
        class Child(IntEnum):girl=1
        actor=Native();actor.ref='person';actor.children={Child.girl:2,actor:3}
        result=NativeStateSnapshot({'cast':[actor]}).capture({'cast':[actor]})
        rows=result['facts']['cast']['person']['children']['mapping']
        self.assertEqual({row['value'] for row in rows},{2,3})
        self.assertTrue(any(row['key'].get('member')=='girl' for row in rows))
        self.assertTrue(any(row['key'].get('reference')==['cast','person'] for row in rows))
        self.assertEqual(result['unknown'],[])

    def test_partial_bindings_are_snapshotted_without_invoking_callback(self):
        actor=Native();actor.ref='person'
        def forbidden(*args,**kwargs):raise AssertionError('Snapshot cannot call this')
        actor.callback=functools.partial(forbidden,actor,flag=True)
        result=NativeStateSnapshot({'cast':[actor]}).capture({'cast':[actor]})
        partial=result['facts']['cast']['person']['callback']
        self.assertEqual(partial['args'],[{'reference':['cast','person']}])
        self.assertEqual(partial['keywords'],{'flag':True})
        self.assertEqual(result['unknown'],[])

    def test_unordered_auxiliary_values_are_canonically_sorted(self):
        first=Native();first.amount=2
        second=Native();second.amount=1
        actor=Native();actor.ref='person';actor.values={first,second}
        reader=NativeStateSnapshot({'cast':[actor]})
        result=reader.capture({'cast':[actor]})
        self.assertEqual([row['fields']['amount'] for row in result['facts']['cast']['person']['values']],[1,2])


if __name__=='__main__':unittest.main()
