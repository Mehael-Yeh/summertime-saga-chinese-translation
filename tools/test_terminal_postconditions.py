import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('terminal_postconditions',Path(__file__).parent/'native_tests/compare_terminal_postconditions.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TerminalEvidenceTests(unittest.TestCase):
    def reference(self):
        return {'version':'build','constructed_mod_save':False,'fabricated_quest_steps':False,
            'terminal_observations':{'route':{'postconditions':{'cast.actor':[['memo',['met']]]}}}}

    def generated(self):
        return {'version':'build','routes':[['route','null',5]],
            'native_postconditions':{'cast.actor':[['memo',['met','relationship']]]}}

    def test_later_memories_can_extend_native_endpoint(self):
        result=module.compare(self.reference(),self.generated())
        self.assertTrue(result['frontier_comparison_complete'])
        self.assertFalse(result['all_routes_verified'])
        self.assertFalse(result['full_dialogue_or_device_acceptance'])

    def test_missing_route_endpoint_cannot_pass(self):
        generated=self.generated()
        generated['routes'].append(['another','null',9])
        result=module.compare(self.reference(),generated)
        self.assertEqual(result['missing_native_frontiers'],['another'])
        self.assertFalse(result['frontier_comparison_complete'])

    def test_missing_required_memory_is_a_difference(self):
        generated=self.generated()
        generated['native_postconditions']['cast.actor']=[['memo',[]]]
        result=module.compare(self.reference(),generated)
        self.assertEqual(len(result['differences_requiring_review']),1)
        self.assertFalse(result['frontier_comparison_complete'])

    def test_projected_or_different_version_reference_is_rejected(self):
        reference=self.reference()
        reference['constructed_mod_save']=True
        reference['version']='other'
        result=module.compare(reference,self.generated())
        self.assertEqual(len(result['errors']),2)
        self.assertFalse(result['frontier_comparison_complete'])


if __name__=='__main__':unittest.main()
