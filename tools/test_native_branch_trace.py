import sys
import unittest
from native_tests.native_branch_trace import NativeBranchTrace, binding_snapshot, code_identity


class NativeBranchTracing(unittest.TestCase):
    def test_unconditional_native_invocation_is_recorded_without_inventing_branch(self):
        module={'__name__':'saga.logic.unconditional'}
        exec('def action():\n return 3\n',module)
        trace=NativeBranchTrace();trace.begin()
        try:self.assertEqual(module['action'](),3)
        finally:result=trace.finish()
        self.assertEqual(result['observations'],[])
        self.assertEqual(result['invocations'][0]['calls'],1)
        self.assertEqual(result['invocations'][0]['code_identity_sha256'],code_identity(module['action'].__code__))
    def test_same_bytecode_in_different_modules_is_not_collapsed(self):
        modules=[{'__name__':'saga.logic.first'}, {'__name__':'saga.logic.second'}]
        for module in modules:
            exec('def action(value):\n if value:return 1\n return 0\n', module)
        trace=NativeBranchTrace()
        trace.begin()
        try:
            for module in modules:module['action'](True)
        finally:result=trace.finish()
        self.assertEqual({row['module'] for row in result['observations']}, {'saga.logic.first','saga.logic.second'})

    def test_constant_changes_keep_distinct_code_identity(self):
        first,second={},{}
        exec('def action(value):\n if value>2:return 1\n return 0\n',first)
        exec('def action(value):\n if value>3:return 1\n return 0\n',second)
        self.assertEqual(first['action'].__code__.co_code,second['action'].__code__.co_code)
        self.assertNotEqual(code_identity(first['action'].__code__),code_identity(second['action'].__code__))

    def test_actual_jumps_keep_bindings_and_do_not_execute_extra_calls(self):
        module={'__name__':'saga.logic.test_actual', 'calls':[]}
        exec('def action(value):\n calls.append(value)\n if value>2:return "yes"\n return "no"\n',module)
        trace=NativeBranchTrace()
        trace.begin()
        try:
            self.assertEqual(module['action'](3),'yes')
            self.assertEqual(module['action'](1),'no')
        finally:
            result=trace.finish()
        self.assertEqual(module['calls'],[3,1])
        self.assertEqual({row['condition_truth'] for row in result['observations']},{True,False})
        self.assertEqual({row['bindings']['value'] for row in result['observations']},{3,1})
        self.assertIsNone(sys.gettrace())

    def test_binding_snapshot_does_not_invoke_ref_properties(self):
        class Unknown:
            @property
            def ref(self):
                raise AssertionError('Do not execute computed properties')
        self.assertIsNone(binding_snapshot({'value':Unknown()})['value']['ref'])

    def test_budget_truncation_is_not_complete_coverage(self):
        module={'__name__':'saga.logic.test_budget'}
        exec('def action(value):\n if value:return 1\n return 0\n',module)
        trace=NativeBranchTrace(limit=0)
        trace.begin()
        try:module['action'](True)
        finally:result=trace.finish()
        self.assertTrue(result['truncated'])
        self.assertEqual(result['observations'],[])


if __name__ == '__main__':
    unittest.main()
