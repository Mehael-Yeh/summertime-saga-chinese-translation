import unittest
from types import SimpleNamespace
from native_tests.gate_catalogue import branch_inventory
from native_tests.gate_runtime import observe_chain,native_predicate,verify_scalar_witness
from native_tests.gate_runtime import execute_parameter_case
from native_tests.gate_runtime import solve_parameter_prerequisites


class NativePredicateTests(unittest.TestCase):
    def test_current_random_input_is_resolved_again_without_integer_literal(self):
        import random
        seed={'kind':'call','function':{'kind':'callable','name':'random.Random'},
            'args':[{'kind':'path','parts':['cast','actor','value']}],'keywords':[]}
        expression={'kind':'operation','operator':'<',
            'left':{'kind':'call','function':{'kind':'attribute','owner':seed,'name':'random'},'args':[],'keywords':[]},
            'right':{'kind':'literal','value':.15}}
        actor=SimpleNamespace(value=1)
        roots={'cast':SimpleNamespace(actor=actor)}
        old=solve_parameter_prerequisites({'expression':expression},roots,{'random.Random':random.Random},True)
        self.assertEqual(old['changes'],{})
        actor.value=0
        self.assertEqual(observe_chain({'expression':expression},roots,{'random.Random':random.Random})['truth'],False)
        new=solve_parameter_prerequisites({'expression':expression},roots,{'random.Random':random.Random},True)
        self.assertEqual(new['status'],'parameter_witness')
        self.assertNotEqual(new['changes'],{})
        self.assertEqual(new['seeded_random_domain_limit'],64)
        self.assertEqual(actor.value,0)

    def test_numeric_gate_threshold_arithmetic(self):
        for operation,left,right,expected in (('*',75,.001,.075),('/',3,2,1.5),('//',7,3,2),('%',7,3,1)):
            expression={'kind':'operation','operator':operation,
                'left':{'kind':'literal','value':left},'right':{'kind':'literal','value':right}}
            self.assertEqual(native_predicate(expression,{},{}),expected)

    def test_invalid_or_overloaded_arithmetic_stays_unknown(self):
        from native_tests.gate_catalogue import UNRESOLVED
        class Operand:
            def __mul__(self,other):raise AssertionError('Entity operator must not run')
        for operation,left,right in (('/',1,0),('*',float('inf'),2),('*',Operand(),2)):
            expression={'kind':'operation','operator':operation,
                'left':{'kind':'literal','value':left},'right':{'kind':'literal','value':right}}
            self.assertIs(native_predicate(expression,{},{}),UNRESOLVED)

    def test_native_clock_enum_comparison_is_a_fixed_read(self):
        from enum import IntEnum
        class Period(IntEnum):
            dawn=0
            dusk=2
        branch={'expression':{'kind':'operation','operator':'<',
            'left':{'kind':'path','parts':['time','tod']},'right':{'kind':'literal','value':Period.dusk}}}
        clock=SimpleNamespace(tod=Period.dawn)
        result=solve_parameter_prerequisites(branch,{'time':clock}, {},True)
        self.assertEqual(result['status'],'parameter_witness')
        self.assertEqual(result['changes'],{})
        self.assertEqual(clock.tod,Period.dawn)

    def test_original_native_item_ownership_protocol_is_read_and_not_mutated(self):
        namespace={'__name__':'saga.test_container'}
        exec('class Container:\n def __contains__(self,entity):\n  return getattr(entity,"where",None) is self\n',namespace)
        owner=namespace['Container']()
        item=SimpleNamespace(where=owner)
        expression={'kind':'operation','operator':'in','left':{'kind':'path','parts':['prop','item']},
            'right':{'kind':'path','parts':['cast','owner']}}
        self.assertTrue(native_predicate(expression,{'cast':SimpleNamespace(owner=owner),'prop':SimpleNamespace(item=item)},{}))
        item.where=None
        self.assertFalse(native_predicate(expression,{'cast':SimpleNamespace(owner=owner),'prop':SimpleNamespace(item=item)},{}))

    def test_mutating_contains_protocol_is_never_executed(self):
        namespace={'__name__':'saga.test_container'}
        exec('class Container:\n def __contains__(self,entity):\n  self.changed=True\n  return True\n',namespace)
        owner=namespace['Container']()
        expression={'kind':'operation','operator':'in','left':{'kind':'literal','value':'item'},
            'right':{'kind':'path','parts':['cast','owner']}}
        from native_tests.gate_catalogue import UNRESOLVED
        self.assertIs(native_predicate(expression,{'cast':SimpleNamespace(owner=owner)},{}),UNRESOLVED)
        self.assertFalse(hasattr(owner,'changed'))

    def test_native_memory_comparison_reads_actual_encounter_set(self):
        namespace={'__name__':'saga.test_actor'}
        exec('class Actor:\n def __lt__(self,other):\n  return other not in self.memo\n',namespace)
        actor=namespace['Actor']()
        actor.memo={'introduced'}
        expression={'kind':'operation','operator':'<','left':{'kind':'path','parts':['cast','person']},
            'right':{'kind':'literal','value':'introduced'}}
        self.assertFalse(native_predicate(expression,{'cast':SimpleNamespace(person=actor)},{}))
        expression['right']['value']='new'
        self.assertTrue(native_predicate(expression,{'cast':SimpleNamespace(person=actor)},{}))
        self.assertEqual(actor.memo,{'introduced'})

    def test_dynamic_getattr_threshold_is_solved_with_native_reads(self):
        actor=SimpleNamespace(ref='person',babies=0)
        cast=SimpleNamespace(person=actor)
        def check():
            if getattr(cast.person,'babies',0)>=2:return True
        branch=branch_inventory(check,{'cast':cast},None)['branches'][0]
        result=solve_parameter_prerequisites(branch,{'cast':cast},{'builtins.getattr':getattr},True)
        self.assertEqual(result['status'],'parameter_witness')
        self.assertEqual(result['changes'],{'cast.person.babies':2})
        self.assertEqual(actor.babies,0)

    def test_fixed_reference_and_clock_predecessors_are_not_scalar_parameters(self):
        stage=object()
        actor=SimpleNamespace(step=stage,ready=False)
        clock=SimpleNamespace(dusk=True)
        def check():
            if clock.dusk and actor.step is stage and actor.ready:return True
        branch=branch_inventory(check,{'cast':SimpleNamespace(person=actor)},clock)['branches'][-1]
        # Explicit native reference operands cannot be guessed from arbitrary
        # objects; use catalogue paths for the supported identity protocol.
        branch['prerequisites']=[{'expression':{'kind':'path','parts':['time','dusk']},'truth':True},
            {'expression':{'kind':'operation','operator':'is','left':{'kind':'path','parts':['cast','person','step']},
             'right':{'kind':'path','parts':['step','terminal']}},'truth':True}]
        branch['expression']={'kind':'path','parts':['cast','person','ready']}
        roots={'cast':SimpleNamespace(person=actor),'time':clock,'step':SimpleNamespace(terminal=stage)}
        result=solve_parameter_prerequisites(branch,roots,{},True)
        self.assertEqual(result['changes'],{'cast.person.ready':True})
        self.assertIs(actor.step,stage)
        self.assertFalse(actor.ready)

    def test_unknown_dynamic_read_never_runs_during_search(self):
        calls=[]
        branch={'expression':{'kind':'call','function':{'kind':'callable','name':'unknown'},'args':[],'keywords':[]}}
        result=solve_parameter_prerequisites(branch,{}, {},True)
        self.assertEqual(result['status'],'unresolved')
        self.assertEqual(calls,[])

    def test_nested_scalar_parameters_restore_the_native_owner(self):
        actor=SimpleNamespace(womb=SimpleNamespace(count=0))
        branch={'expression':{'kind':'operation','operator':'>','left':{'kind':'path','parts':['cast','person','womb','count']},
            'right':{'kind':'literal','value':0}}}
        result=solve_parameter_prerequisites(branch,{'cast':SimpleNamespace(person=actor)}, {},True)
        self.assertEqual(result['changes'],{'cast.person.womb.count':1})
        self.assertEqual(actor.womb.count,0)

    def test_parameter_dispatch_uses_solved_native_fields_and_restores_them(self):
        actor=SimpleNamespace(babies=0,reward=0)
        branch={'module':'native','code_identity_sha256':'identity','offset':10,
            'expression':{'kind':'operation','operator':'>=',
            'left':{'kind':'path','parts':['cast','person','babies']},
            'right':{'kind':'literal','value':1}}}
        trace=SimpleNamespace(begin=lambda:None,finish=lambda:{'observations':[
            dict(module='native',code_identity_sha256='identity',offset=10,condition_truth=True)]})
        def invoke():
            self.assertEqual(actor.babies,1)
            actor.reward=5
        result=execute_parameter_case(branch,{'changes':{'cast.person.babies':1}},True,
            {'cast':SimpleNamespace(person=actor)}, {},invoke,trace,lambda:actor.reward)
        self.assertEqual(result['status'],'native_dispatch_observed')
        self.assertEqual((result['before'],result['after']),(0,5))
        self.assertEqual(actor.babies,0)
        self.assertFalse(result['native_response_validated'])

    def test_state_delta_preserves_added_removed_and_changed_native_facts(self):
        from native_tests.gate_runtime import state_delta
        before={'cast':{'actor':{'ready':False,'gone':1}}}
        after={'cast':{'actor':{'ready':True,'new':None}}}
        result=state_delta(before,after)
        self.assertNotEqual(result['before_sha256'],result['after_sha256'])
        self.assertEqual(len(result['changes']),3)
        removed=next(row for row in result['changes'] if row['path'][-1]=='gone')
        self.assertFalse(removed['after_present'])
        added=next(row for row in result['changes'] if row['path'][-1]=='new')
        self.assertFalse(added['before_present'])
        self.assertTrue(added['after_present'])

    def test_seeded_native_random_expression_does_not_change_global_rng(self):
        import random
        seed={'kind':'call','function':{'kind':'callable','name':'random.Random'},
            'args':[{'kind':'literal','value':17}],'keywords':[]}
        expression={'kind':'call','function':{'kind':'attribute','owner':seed,'name':'random'},
            'args':[],'keywords':[]}
        before=random.getstate()
        values=[native_predicate(expression,{}, {'random.Random':random.Random}) for _ in range(2)]
        self.assertEqual(values,[random.Random(17).random()]*2)
        self.assertEqual(random.getstate(),before)
        from native_tests.gate_catalogue import UNRESOLVED
        seed['args']=[]
        self.assertIs(native_predicate(expression,{}, {'random.Random':random.Random}),UNRESOLVED)

    def test_unconditional_entry_requires_actual_matching_native_invocation(self):
        branch={'entry_only':True,'module':'saga.logic.entry','code_identity_sha256':'native-id',
            'expression':{'kind':'literal','value':True}}
        trace=SimpleNamespace(begin=lambda:None,finish=lambda:{'observations':[],
            'invocations':[{'module':'saga.logic.entry','code_identity_sha256':'native-id'}]})
        result=execute_parameter_case(branch,{'changes':{}},True,{}, {},lambda:None,trace,lambda:0)
        self.assertTrue(result['target_entry_observed'])
        self.assertIsNone(result['target_branch_observed'])
        self.assertFalse(result['native_response_validated'])

    def test_enum_literal_survives_json_without_becoming_current_time(self):
        from enum import IntEnum
        import json
        from native_tests.gate_catalogue import literal
        class tod(IntEnum):dawn=0;dusk=2
        expression=json.loads(json.dumps(literal(tod.dusk)))
        clock=SimpleNamespace(tod=tod.dawn)
        self.assertIs(native_predicate(expression,{'time':clock},{}),tod.dusk)

    def test_unsatisfied_prerequisite_never_dispatches_native_event(self):
        calls=[]
        result=execute_parameter_case({'expression':{'kind':'literal','value':False}},
            {'changes':{}},True,{}, {},lambda:calls.append(1),None,None)
        self.assertEqual(result['status'],'prerequisite_not_satisfied')
        self.assertEqual(calls,[])

    def test_script_transfer_is_not_counted_as_completed_native_response(self):
        actor=SimpleNamespace(babies=0)
        def transfer():raise RuntimeError('native script continuation required')
        trace=SimpleNamespace(begin=lambda:None,finish=lambda:{'observations':[]})
        result=execute_parameter_case({'expression':{'kind':'literal','value':True}},
            {'changes':{'cast.person.babies':1}},True,{'cast':SimpleNamespace(person=actor)},
            {},transfer,trace,lambda:actor.babies)
        self.assertEqual(result['status'],'native_response_incomplete')
        self.assertEqual(actor.babies,0)
        self.assertFalse(result['native_response_validated'])

    def test_native_witness_restores_original_scalar(self):
        actor=SimpleNamespace(babies=0)
        branch={'expression':{'kind':'operation','operator':'>=',
            'left':{'kind':'path','parts':['cast','anon','babies']},
            'right':{'kind':'literal','value':1}}}
        result=verify_scalar_witness(branch,{'changes':{'cast.anon.babies':1}},True,
            {'cast':SimpleNamespace(anon=actor)}, {})
        self.assertTrue(result['witness_matches_native'])
        self.assertEqual(actor.babies,0)

    def test_invalid_later_write_still_restores_earlier_field(self):
        actor=SimpleNamespace(babies=0)
        witness={'changes':{'cast.anon.babies':1,'cast.anon.missing':1}}
        result=verify_scalar_witness({},witness,True,{'cast':SimpleNamespace(anon=actor)}, {})
        self.assertEqual(result['status'],'unresolved')
        self.assertEqual(actor.babies,0)
        self.assertFalse(hasattr(actor,'missing'))

    def test_admitted_getattr_is_called_on_real_owner(self):
        actor=SimpleNamespace(ref='anon',babies=2)
        cast=SimpleNamespace(anon=actor)
        clock=SimpleNamespace(date=1)
        def check():
            if getattr(cast.anon,'babies',0)>0:return True
        branch=branch_inventory(check,{'cast':cast},clock)['branches'][0]
        result=observe_chain(branch,{'cast':cast,'time':clock},{'builtins.getattr':getattr})
        self.assertEqual(result['status'],'native_predicate_observed')
        self.assertTrue(result['truth'])
        self.assertFalse(result['native_response_validated'])

    def test_unknown_call_is_not_executed(self):
        calls=[]
        def dangerous():calls.append(True)
        expression={'kind':'call','function':{'kind':'callable','name':'dangerous'},'args':[],'keywords':[]}
        from native_tests.gate_catalogue import UNRESOLVED
        self.assertIs(native_predicate(expression,{},{}),UNRESOLVED)
        self.assertEqual(calls,[])

    def test_blocked_predecessor_prevents_later_call(self):
        calls=[]
        branch={'prerequisites':[{'expression':{'kind':'literal','value':False},'truth':True}],
            'expression':{'kind':'call','function':{'kind':'callable','name':'probe'},'args':[],'keywords':[]}}
        result=observe_chain(branch,{}, {'probe':lambda:calls.append(True)})
        self.assertEqual(result['status'],'predecessor_blocked')
        self.assertEqual(calls,[])

    def test_side_effect_branch_is_rejected(self):
        branch={'prior_effects':[{'operation':'STORE_ATTR'}],'expression':{'kind':'literal','value':True}}
        self.assertEqual(observe_chain(branch,{}, {})['status'],'unresolved')

    def test_native_dispatch_membership_reads_singleton_and_uses_identity(self):
        class Observer:
            __module__='saga.test'
        class Event:
            __module__='saga.event'
            ref='event'
        observer=Observer();event=Event();event.crowd={observer}
        expression={'kind':'operation','operator':'in',
            'left':{'kind':'path','parts':['step','observer']},
            'right':{'kind':'attribute','owner':{'kind':'reference','module':'saga.event','ref':'event'},'name':'crowd'}}
        roots={'step':SimpleNamespace(observer=observer),'event':event}
        self.assertTrue(native_predicate(expression,roots,{}))
        event.crowd=set()
        self.assertFalse(native_predicate(expression,roots,{}))

    def test_membership_does_not_execute_subclass_iterator_or_equality(self):
        class Observer:
            __module__='saga.test'
        class Crowd(set):
            def __iter__(self):raise AssertionError('Do not run custom iteration')
        observer=Observer()
        roots={'step':SimpleNamespace(observer=observer),'crowd':Crowd([observer])}
        expr={'kind':'operation','operator':'in','left':{'kind':'path','parts':['step','observer']},
            'right':{'kind':'path','parts':['crowd']}}
        self.assertTrue(native_predicate(expr,roots,{}))

    def test_reference_attribute_property_is_unknown_without_execution(self):
        class Event:
            __module__='saga.event'
            ref='event'
            @property
            def crowd(self):raise AssertionError('Do not evaluate property')
        expr={'kind':'attribute','owner':{'kind':'reference','module':'saga.event','ref':'event'},'name':'crowd'}
        from native_tests.gate_catalogue import UNRESOLVED
        self.assertIs(native_predicate(expr,{'event':Event()},{}),UNRESOLVED)

if __name__=='__main__':unittest.main()
