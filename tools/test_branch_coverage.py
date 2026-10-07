import unittest
from native_tests.branch_coverage import correlate


class BranchCoverage(unittest.TestCase):
    def inventory(self):
        return {'version':'native','baseline_sha256':'baseline','gates':[
            {'id':name,'analysis':{'branches':[{'module':name,'code_identity_sha256':'same','offset':12}]}}
            for name in ('saga.logic.first','saga.logic.second')]}

    def report(self):
        return {'version':'native','baseline_sha256':'baseline','tick':4,
            'status':'segment_complete','pending':[{}], 'unhandled_controls':{'unknown':{}},
            'rows':[{'native_branch_trace':{'observations':[{'module':'saga.logic.first',
                'code_identity_sha256':'same','offset':12,'condition_truth':True,'bindings':{'value':3}}]}}]}

    def test_source_modules_do_not_inherit_each_others_evidence(self):
        result=correlate(self.inventory(),[self.report()])
        self.assertEqual(result['branches'][0]['unobserved_outcomes'],['false'])
        self.assertEqual(result['branches'][1]['unobserved_outcomes'],['true','false'])
        self.assertFalse(result['all_gates_passed'])
        self.assertEqual(result['limitations'][0]['unsupported_controls'],1)

    def test_other_save_or_version_cannot_be_combined(self):
        for field in ('version','baseline_sha256'):
            report=self.report()
            report[field]='other'
            with self.assertRaisesRegex(ValueError,field):correlate(self.inventory(),[report])

    def test_failed_response_does_not_become_branch_acceptance(self):
        report=self.report()
        report['status']='failed'
        with self.assertRaises(ValueError):correlate(self.inventory(),[report])

    def test_old_trace_without_identity_is_rejected(self):
        report=self.report()
        del report['rows'][0]['native_branch_trace']['observations'][0]['code_identity_sha256']
        with self.assertRaises(ValueError):correlate(self.inventory(),[report])


if __name__=='__main__':unittest.main()
