import unittest
from native_tests.gate_sequence import run_sequence,compare_effects
from native_tests.gate_runtime import parameter_fields
from types import SimpleNamespace


class SequenceTests(unittest.TestCase):
    def run_chain(self,generated=None,loop=False,incomplete=False,validated=True):
        state={'facts':{'flag':False,'reward':0},'unknown':[]}
        executed=[]
        solved=[]
        def select():
            if len(executed)==2 and not loop:
                return {'status':'native_final_gate_completed','source':'native.test.final',
                    'native_completion_evidence':{'return':'null'}}
            return {'status':'native_gate','source':'native.test','gate':'gate'+str(len(executed)) if not loop else 'reminder'}
        def solve(gate):
            solved.append(dict(state['facts']))
            return {'status':'parameter_witness','changes':{'flag':len(executed)==0}}
        def execute(gate,witness):
            if not loop:
                state['facts']['flag']=witness['changes']['flag']
                state['facts']['reward']+=1
            executed.append(gate['gate'])
            return {'status':'native_dispatch_observed','target_branch_observed':True,
                'native_queue_drained':not incomplete,'native_task_completed':True,'native_branch_trace':{'truncated':False},
                'native_postconditions_validated':validated,
                'state_delta':{'changes':[{'path':['facts','reward']}]}}
        result=run_sequence(select,solve,execute,lambda:state,
            lambda:generated or {'facts':{'flag':False,'reward':2},'unknown':[]},max_steps=5)
        return result,solved

    def test_later_prerequisite_replaces_old_but_native_effects_survive(self):
        result,solved=self.run_chain()
        self.assertEqual(solved,[{'flag':False,'reward':0},{'flag':True,'reward':1}])
        self.assertEqual(result['status'],'sequence_verified')
        self.assertTrue(result['all_gates_passed'])

    def test_generated_mismatch_reports_field_instead_of_patching_it(self):
        result,_=self.run_chain({'facts':{'reward':0},'unknown':[]})
        self.assertFalse(result['all_gates_passed'])
        difference=result['comparison']['differences'][0]
        self.assertEqual(difference['path'],['facts','reward'])
        self.assertEqual((difference['expected'],difference['actual']),(2,0))

    def test_repeated_reminder_without_state_change_stops(self):
        result,_=self.run_chain(loop=True)
        self.assertEqual(result['status'],'no_progress_cycle')
        self.assertFalse(result['all_gates_passed'])

    def test_pending_native_queue_cannot_advance(self):
        result,solved=self.run_chain(incomplete=True)
        self.assertEqual(result['status'],'native_gate_incomplete')
        self.assertEqual(len(solved),1)

    def test_observations_without_semantic_postconditions_are_not_acceptance(self):
        result,_=self.run_chain(validated=False)
        self.assertEqual(result['status'],'sequence_not_accepted')
        self.assertFalse(result['all_gates_passed'])

    def test_no_witness_or_empty_candidate_is_not_final_completion(self):
        result=run_sequence(lambda:{'status':'empty'},lambda _:None,lambda *_:None,
            lambda:{},lambda:{})
        self.assertEqual(result['status'],'next_gate_unresolved')
        result=run_sequence(lambda:{'status':'native_gate','source':'native.test','gate':'one'},
            lambda _:{'status':'unresolved'},lambda *_:self.fail('must not execute'),lambda:{},lambda:{})
        self.assertEqual(result['status'],'prerequisite_unresolved')

    def test_unknown_snapshots_and_missing_facts_are_not_equal(self):
        self.assertEqual(compare_effects({'unknown':['unsupported']},{},[])['status'],'unknown_snapshot')
        result=compare_effects({'facts':{'reward':1}},{'facts':{}},[{'path':['facts','reward']}])
        self.assertEqual(result['status'],'state_mismatch')
        self.assertFalse(result['differences'][0]['generated_present'])

    def test_same_deleted_field_and_latest_effect_value_match(self):
        effects=[{'path':['facts','reward']},{'path':['facts','reward']},{'path':['facts','retired']}]
        result=compare_effects({'facts':{'reward':2}},{'facts':{'reward':2}},effects)
        self.assertEqual(result['status'],'observed_effects_match')
        self.assertEqual(result['compared_paths'],2)

    def test_parameters_can_persist_only_for_disposable_sequence_caller(self):
        actor=SimpleNamespace(flag=False)
        roots={'cast':SimpleNamespace(actor=actor)}
        witness={'changes':{'cast.actor.flag':True}}
        with parameter_fields(witness,roots):self.assertTrue(actor.flag)
        self.assertFalse(actor.flag)
        with parameter_fields(witness,roots,retain=True):self.assertTrue(actor.flag)
        self.assertTrue(actor.flag)


if __name__=='__main__':unittest.main()
