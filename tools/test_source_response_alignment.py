import unittest
from native_tests.source_response_alignment import align


class AlignmentTests(unittest.TestCase):
    def source(self,rows):return {'engine_version':'test','graph':{'statements':rows}}
    def responses(self,truth=True):
        return {'version':'test','native_cases':[{'gate':'registered','status':'native_dispatch_observed',
            'native_queue_drained':True,'native_script_continuations':[{'statements':[{'kind':'If',
                'source':'game/src/test.rpy:8','native_evaluated_conditions':[{'expression':'(flag)','truth':truth}]}]}]}]}
    def row(self,id='1',line=8):return {'node':'If','file':'/isolated/src/test.rpy','line':line,'id':id,'conditions':['flag']}

    def test_actual_evaluation_matches_source_without_claiming_all_gates(self):
        result=align(self.source([self.row()]),self.responses())
        self.assertEqual(result['statuses'],{'source_condition_observed':1})
        self.assertEqual(result['observed_source_if_nodes'],1)
        self.assertFalse(result['all_gates_passed'])
        self.assertEqual(result['validation_mode'],'gate_only')
        self.assertFalse(result['route_endpoint_validation_required'])

    def test_ambiguous_source_is_not_marked_covered(self):
        result=align(self.source([self.row('1'),self.row('2')]),self.responses())
        self.assertEqual(result['statuses'],{'source_ambiguous':1})
        self.assertEqual(result['observed_source_if_nodes'],0)

    def test_unknown_truth_and_unvisited_source_remain_unverified(self):
        result=align(self.source([self.row()]),self.responses(None))
        self.assertEqual(result['statuses'],{'unknown_native_truth':1})
        self.assertEqual(result['unobserved_source_if_nodes'],['1'])

    def test_different_engine_versions_are_rejected(self):
        source=self.source([self.row()]);source['engine_version']='other'
        with self.assertRaises(ValueError):align(source,self.responses())


if __name__=='__main__':unittest.main()
