import unittest
from types import SimpleNamespace as NS
from native_tests.native_script_continuation import (ScriptContinuation,expand_menu_plans,plan_identity,
    stored_boolean_parameters,apply_script_parameters)


class Node:
    filename='native.rpy'
    linenumber=1
    next=None


class Say(Node):
    def execute(self):raise AssertionError('presentation must not run')


class TranslateSay(Say):
    def execute(self):
        self.effect()
        Say.execute(self)


class Python(Node):
    def execute(self):self.effect()


class Menu(Node):
    def execute(self):self.selected=self.api.exports.menu(self.choices)


class UserStatement(Node):
    def execute(self):raise AssertionError('unknown control must not run')


class If(Node):
    def execute(self):
        self.api.ast.next_node(self.next)
        for expression,block in self.entries:
            if self.api.python.py_eval(expression):
                self.api.ast.next_node(block[0] if block else None)
                break


class ScriptTests(unittest.TestCase):
    def test_native_if_evaluation_is_recorded_once_and_adapter_restored(self):
        node=If();node.entries=[('False',[]),('True',[])]
        api=self.api([node]);api.ast.If=If;node.api=api
        calls=[]
        def evaluate(expr):calls.append(expr);return expr=='True'
        api.python.py_eval=evaluate
        result=ScriptContinuation(api).run('native')
        records=result['statements'][0]['native_evaluated_conditions']
        self.assertEqual(calls,['False','True'])
        self.assertEqual([row['truth'] for row in records],[False,True])
        self.assertIs(api.python.py_eval,evaluate)

    def test_custom_truth_is_not_evaluated_twice(self):
        calls=[]
        class Truth:
            def __bool__(self):calls.append(True);return True
        node=If();node.entries=[('special',[])]
        api=self.api([node]);api.ast.If=If;node.api=api
        api.python.py_eval=lambda expr:Truth()
        result=ScriptContinuation(api).run('native')
        self.assertEqual(calls,[True])
        record=result['statements'][0]['native_evaluated_conditions'][0]
        self.assertIsNone(record['truth'])
        self.assertIn('unresolved_truth_type',record)

    def test_native_if_eval_failure_restores_original_function(self):
        node=If();node.entries=[('broken',[])]
        api=self.api([node]);api.ast.If=If;node.api=api
        def evaluate(expr):raise ValueError('failed')
        api.python.py_eval=evaluate
        result=ScriptContinuation(api).run('native')
        self.assertEqual(result['reason'],'native_script_execution_error')
        self.assertIs(api.python.py_eval,evaluate)

    def test_custom_truth_is_captured_from_real_control_transfer(self):
        calls=[]
        class Truth:
            def __bool__(self):calls.append(True);return True
        child=Python();node=If();node.entries=[('special',[child])]
        api=self.api([node]);api.ast.If=If;node.api=api
        api.python.py_eval=lambda expr:Truth()
        original=api.ast.next_node
        result=ScriptContinuation(api).run('native')
        record=result['statements'][0]['native_evaluated_conditions'][0]
        self.assertEqual(calls,[True])
        self.assertTrue(record['truth'])
        self.assertEqual(record['native_truth_source'],'native_control_transfer')
        self.assertIs(api.ast.next_node,original)
    def test_native_simple_mode_is_solved_from_literal_condition_not_screen_name(self):
        from native_tests.native_script_continuation import script_parameter_candidates
        api=NS(store=NS(persistent=NS(mode='normal')))
        domains=script_parameter_candidates(api,["persistent.mode == 'easy'"])
        self.assertEqual(domains,{'persistent.mode':['easy']})
        apply_script_parameters(api,{'persistent.mode':'easy'})
        self.assertEqual(api.store.persistent.mode,'easy')

    def test_script_parameter_plan_rejects_absent_fields_and_is_atomic(self):
        api=NS(store=NS(persistent=NS(option=True,count=1)))
        with self.assertRaises(ValueError):apply_script_parameters(api,{'persistent.option':False,'persistent.absent':None})
        self.assertTrue(api.store.persistent.option)
        with self.assertRaises(ValueError):apply_script_parameters(api,{'persistent.count':False})

    def test_script_parameters_cannot_replace_independent_native_clock_scenario(self):
        from native_tests.native_script_continuation import script_parameter_candidates
        api=NS(store=NS(saga=NS(time=NS(now=4))))
        self.assertEqual(script_parameter_candidates(api,['saga.time.now>=20']),{})
        with self.assertRaises(ValueError):apply_script_parameters(api,{'saga.time.now':20})
    def test_imported_persistent_aliases_use_case_object_and_restore(self):
        from native_tests.native_script_continuation import replace_persistent_aliases,restore_persistent_aliases
        original=NS(flag=False);replacement=NS(flag=False)
        native={'persistent':original,'unrelated':True}
        bindings=replace_persistent_aliases([native,native],original,replacement)
        native['persistent'].flag=True
        self.assertFalse(original.flag)
        self.assertEqual(len(bindings),1)
        restore_persistent_aliases(bindings)
        self.assertIs(native['persistent'],original)
    def test_script_boolean_candidates_come_from_existing_native_fields_only(self):
        api=NS(store=NS(persistent=NS(option=True,count=1,_private=False)))
        result=stored_boolean_parameters(api,['not persistent.option','persistent.count>0','persistent._private'])
        self.assertEqual(result,{'persistent.option':True})
        apply_script_parameters(api,{'persistent.option':False})
        self.assertFalse(api.store.persistent.option)
        with self.assertRaises(ValueError):apply_script_parameters(api,{'persistent.count':False})

    def test_blocked_screen_branches_by_native_condition_parameters_not_fake_result(self):
        receipts=[{'status':'native_script_blocked','reason':'native_statement_requires_adapter',
            'statements':[{'stored_boolean_parameters':{'persistent.option':True}}]}]
        plans=expand_menu_plans({'native.rpy:1':7},receipts)
        self.assertEqual(plans,[{'native.rpy:1':7,'__parameters__':{'persistent.option':False}}])
        self.assertEqual(expand_menu_plans(plans[0],receipts),[])
    def test_native_translation_bookkeeping_runs_but_say_presentation_does_not(self):
        effects=[]
        node=TranslateSay();node.effect=lambda:effects.append('native-seen')
        api=self.api([node]);api.ast.TranslateSay=TranslateSay
        result=ScriptContinuation(api).run('native')
        self.assertEqual(result['status'],'native_script_returned')
        self.assertEqual(effects,['native-seen'])

    def test_menu_plans_branch_only_on_observed_enabled_payloads(self):
        receipts=[{'reason':'native_menu_input_required','details':{
            'source':'native.rpy:9','available':[{'value':3},{'value':7}]}}]
        original={'native.rpy:1':2}
        plans=expand_menu_plans(original,receipts)
        self.assertEqual(plans,[{'native.rpy:1':2,'native.rpy:9':3},{'native.rpy:1':2,'native.rpy:9':7}])
        self.assertEqual(original,{'native.rpy:1':2})
        self.assertEqual(expand_menu_plans(plans[0],receipts),[])
        self.assertEqual(plan_identity(plans[0]),plan_identity(dict(reversed(list(plans[0].items())))))
    def api(self,nodes,value=23):
        next_nodes=[]
        api=NS(ast=NS(Node=Node,Say=Say,Python=Python,Menu=Menu,UserStatement=UserStatement,
                      next_node=next_nodes.append),exports=NS(menu=lambda *args:None),
               python=NS(py_eval=lambda expr:expr=='True'))
        def run(label,*args,**kwargs):
            for node in nodes:node.execute()
            return value
        api.call_in_new_context=run
        return api

    def test_native_state_effect_and_return_are_preserved_without_dialogue(self):
        effects=[]
        node=Python();node.effect=lambda:effects.append('native-effect')
        original=Say.execute
        result=ScriptContinuation(self.api([Say(),node])).run('native_label')
        self.assertEqual(effects,['native-effect'])
        self.assertEqual(result['value'],23)
        self.assertEqual(result['status'],'native_script_returned')
        self.assertIs(Say.execute,original)

    def test_menu_input_must_be_enabled_and_is_the_actual_payload(self):
        menu=Menu();menu.choices=[('blocked','False',0),('enabled','True',1),('other','True',2)]
        api=self.api([menu]);menu.api=api
        result=ScriptContinuation(api,{'native.rpy:1':1}).run('native')
        self.assertEqual(result['status'],'native_script_returned')
        self.assertEqual(menu.selected,1)
        result=ScriptContinuation(api,{'native.rpy:1':0}).run('native')
        self.assertEqual(result['reason'],'native_menu_input_not_enabled')

    def test_multiple_menu_choices_require_an_explicit_input_plan(self):
        menu=Menu();menu.choices=[('one','True',1),('two','True',2)]
        api=self.api([menu]);menu.api=api
        original=api.exports.menu
        result=ScriptContinuation(api).run('native')
        self.assertEqual(result['reason'],'native_menu_input_required')
        self.assertEqual([row['value'] for row in result['details']['available']],[1,2])
        self.assertIs(api.exports.menu,original)

    def test_unknown_screen_input_never_produces_a_success_result(self):
        node=UserStatement();node.line='call screen arbitrary_game()'
        original=UserStatement.execute
        result=ScriptContinuation(self.api([node])).run('native')
        self.assertEqual(result['reason'],'native_statement_requires_adapter')
        self.assertNotIn('value',result)
        self.assertIs(UserStatement.execute,original)

    def test_native_python_error_is_reported_without_entering_error_ui(self):
        node=Python();node.effect=lambda:1/0
        result=ScriptContinuation(self.api([node])).run('native')
        self.assertEqual(result['reason'],'native_script_execution_error')
        self.assertEqual(result['details']['type'],'ZeroDivisionError')


if __name__=='__main__':unittest.main()
