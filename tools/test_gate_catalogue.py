import unittest
from types import SimpleNamespace
from native_tests.gate_catalogue import branch_inventory, temporal_scenarios, render_inventory, branch_witnesses, solve_prerequisites

clock=SimpleNamespace(date=1,tod='dawn')
cast=SimpleNamespace(anon=SimpleNamespace(ref='anon',babies=0))

def gate():
    if clock.date < 5:return None
    if cast.anon.babies >= 1:return 'ready'
    return None

def dynamic_gate(actor):
    if actor.plan[0]:return None
    return 'ready'

class GateInventory(unittest.TestCase):
    def test_native_integer_context_marker_binds_observer(self):
        def check(ctx):
            if ctx.ready:return True
        check._ctx=1
        observer=SimpleNamespace(ref='route',ready=True)
        branch=branch_inventory(check,{'flow':SimpleNamespace(route=observer)},clock,
            observer_context=observer)['branches'][0]
        self.assertEqual(branch['expression'],{'kind':'path','parts':['flow','route','ready']})

    def test_calendar_input_uses_actual_clock_enum_and_keeps_dynamic_clock_path(self):
        from enum import IntEnum
        from native_tests.gate_catalogue import concrete_event_defaults
        class tod(IntEnum):dawn=0;dusk=2
        native_clock=SimpleNamespace(tod=tod.dusk)
        def check(*,tod=None):
            if tod==tod.dusk:return True
        check._req={'tod'}
        event,provenance,missing=concrete_event_defaults(check,(),native_clock)
        self.assertIs(event['tod'],tod.dusk)
        self.assertEqual(provenance['tod'],'explicit_test_input_from_native_clock')
        branch=branch_inventory(check,{},native_clock,event,clock_bindings=('tod',))['branches'][0]
        self.assertEqual(branch['expression']['left'],{'kind':'path','parts':['time','tod']})
        self.assertEqual(branch['expression']['right'],{'kind':'path','parts':['time','tod','dusk']})

    def test_registered_enum_literal_is_not_replaced_by_dynamic_clock(self):
        from enum import IntEnum
        class tod(IntEnum):dawn=0;dusk=2
        native_clock=SimpleNamespace(tod=tod.dawn)
        def check(*,tod=None):
            if tod==tod.dusk:return True
        branch=branch_inventory(check,{},native_clock,{'tod':tod.dusk})['branches'][0]
        self.assertEqual(branch['expression']['left']['kind'],'enum')
        self.assertEqual(branch['expression']['left']['name'],'dusk')
    def test_seeded_local_random_read_is_not_a_global_side_effect_barrier(self):
        import random
        namespace={'Random':random.Random}
        exec('def check():\n r=Random(17)\n if r.random()<.5:return True\n return False\n',namespace)
        branch=branch_inventory(namespace['check'],{},clock)['branches'][0]
        self.assertEqual(branch['prior_effects'],[])
    def test_registered_none_is_an_explicit_literal_not_a_missing_input(self):
        from native_tests.gate_catalogue import concrete_event_defaults
        def callback(*,who):return who
        callback._req={'who'}
        event,provenance,missing=concrete_event_defaults(callback,(('who',None),))
        self.assertEqual(event,{'who':None})
        self.assertEqual(provenance,{'who':'registered_literal'})
        self.assertEqual(missing,[])
    def test_declared_default_is_an_explicit_dispatch_input_not_an_observed_event(self):
        from native_tests.gate_catalogue import concrete_event_defaults
        def callback(*,clock=None):return clock
        callback._req={'clock'}
        event,provenance,missing=concrete_event_defaults(callback,())
        self.assertEqual(event,{'clock':None})
        self.assertEqual(provenance,{'clock':'explicit_test_input_from_native_default'})
        self.assertEqual(missing,[])
        def required(*,who):return who
        required._req={'who'}
        self.assertEqual(concrete_event_defaults(required,())[2],['who'])

    def test_bare_boolean_gate_can_be_solved_in_both_directions(self):
        branch={'expression':{'kind':'path','parts':['prop','device','lock']}}
        witness=solve_prerequisites(branch,{'prop.device.lock':False},True)
        self.assertEqual(witness['status'],'scalar_witness')
        self.assertEqual(witness['changes'],{'prop.device.lock':True})
        witness=solve_prerequisites(branch,{'prop.device.lock':True},False)
        self.assertEqual(witness['changes'],{'prop.device.lock':False})

    def test_native_context_flag_does_not_use_default_none_as_actual_observer(self):
        namespace={}
        exec('def callback(ctx=None):\n if ctx.ready:return True\n return False\n',namespace)
        callback=namespace['callback']
        callback._ctx=True
        unbound=branch_inventory(callback,{},clock)
        self.assertFalse(unbound['branches'][0]['supported'])
        observer=SimpleNamespace(ref='route',ready=True)
        catalogue=SimpleNamespace(route=observer)
        bound=branch_inventory(callback,{'flow':catalogue},clock,observer_context=observer)
        self.assertEqual(bound['branches'][0]['expression'],{'kind':'path','parts':['flow','route','ready']})

    def test_runtime_context_follows_partial_positional_prefix(self):
        from functools import partial
        namespace={}
        exec('def callback(prefix,ctx=None):\n if ctx.ready and prefix==7:return True\n return False\n',namespace)
        callback=partial(namespace['callback'],7)
        callback._ctx=True
        observer=SimpleNamespace(ref='route',ready=True)
        result=branch_inventory(callback,{'flow':SimpleNamespace(route=observer)},clock,observer_context=observer)
        self.assertEqual(result['branches'][0]['expression'],{'kind':'path','parts':['flow','route','ready']})
    def test_guarded_field_writes_keep_values_conditions_and_effect_order(self):
        player=SimpleNamespace(ref='player',level=2,ready=False)
        catalogue=SimpleNamespace(player=player)
        namespace={'cast':catalogue}
        exec('def callback():\n if cast.player.level>1:\n  cast.player.ready=True\n  cast.player.level=3\n',namespace)
        result=branch_inventory(namespace['callback'],{'cast':catalogue},clock)
        writes=result['writes']
        self.assertEqual([row['field'] for row in writes],['ready','level'])
        self.assertEqual(writes[0]['owner'],{'kind':'path','parts':['cast','player']})
        self.assertEqual(writes[0]['value'],{'kind':'literal','value':True})
        self.assertTrue(writes[0]['prerequisites'])
        self.assertEqual(writes[0]['prior_effects'],[])
        self.assertEqual(writes[1]['prior_effects'][0]['operation'],'STORE_ATTR')
        self.assertFalse(writes[0]['projection_validated'])
        self.assertFalse(player.ready)
        self.assertEqual(player.level,2)
    def test_unrelated_metadata_object_is_not_a_partial(self):
        from native_tests.gate_catalogue import unwrap_callback
        metadata=SimpleNamespace(func=lambda:None,args=None,keywords=None)
        self.assertIs(unwrap_callback(metadata)[0],metadata)

    def test_nested_engine_partial_preserves_argument_order(self):
        class Partial:
            def __init__(self,func,*args,**keywords):self.func,self.args,self.keywords=func,args,keywords
            def __call__(self,*args,**keywords):return self.func(*self.args,*args,**dict(self.keywords,**keywords))
        def check(first,second):
            if first<second:return True
        callback=Partial(Partial(check,1),3)
        self.assertTrue(callback())
        branch=branch_inventory(callback,{},clock)['branches'][0]
        self.assertEqual(branch['expression']['left']['value'],1)
        self.assertEqual(branch['expression']['right']['value'],3)

    def test_required_wildcard_event_field_is_not_default_none(self):
        def check(interact=None):
            if interact is None:return True
        check._req={'interact'}
        branch=branch_inventory(check,{},clock)['branches'][0]
        self.assertEqual(branch['expression']['left']['kind'],'unknown')
        self.assertFalse(branch['supported'])

    def test_registration_event_overrides_keyword_default(self):
        def check(*,who=None):
            if who.babies>0:return True
        branch=branch_inventory(check,{'cast':cast},clock,{'who':cast.anon})['branches'][0]
        self.assertEqual(branch['expression']['left']['parts'],['cast','anon','babies'])

    def test_engine_partial_and_closure_keep_native_owner(self):
        class Partial:
            def __init__(self,func,*args,**keywords):self.func,self.args,self.keywords=func,args,keywords
        actor=cast.anon
        def check(who):
            if who.babies>=1:return actor.babies
        result=branch_inventory(Partial(check,actor),{'cast':cast},clock)
        self.assertEqual(result['branches'][0]['expression']['left']['parts'],['cast','anon','babies'])

    def test_predecessor_chain_must_also_hold(self):
        branch=branch_inventory(gate,{'cast':cast},clock)['branches'][1]
        facts={'time.date':1,'cast.anon.babies':0}
        self.assertEqual(solve_prerequisites(branch,facts,True)['status'],'no_scalar_witness')
        facts['time.date']=5
        witness=solve_prerequisites(branch,facts,True)
        self.assertEqual(witness['changes'],{'cast.anon.babies':1})
        self.assertFalse(witness['native_response_validated'])

    def test_join_keeps_alternative_local_bindings_separate(self):
        def check():
            if clock.date<5:threshold=1
            else:threshold=3
            if cast.anon.babies>=threshold:return True
        branches=branch_inventory(check,{'cast':cast},clock)['branches']
        self.assertEqual({b['expression']['right'].get('value') for b in branches[1:]},{1,3})

    def test_native_calls_keep_source_but_are_not_certified(self):
        def check():
            if getattr(cast.anon,'babies',0)>=1:return True
        branch=branch_inventory(check,{'cast':cast},clock)['branches'][0]
        self.assertEqual(branch['expression']['left']['kind'],'call')
        self.assertFalse(branch['supported'])
        self.assertEqual(solve_prerequisites(branch,{},True)['status'],'unresolved')

    def test_prior_write_must_not_be_solved_against_old_facts(self):
        def check():
            cast.anon.babies=3
            if cast.anon.babies>=1:return True
        branch=branch_inventory(check,{'cast':cast},clock)['branches'][0]
        result=solve_prerequisites(branch,{'cast.anon.babies':0},True)
        self.assertEqual(result['reason'],'requires_native_prior_effects')

    def test_temporal_and_durable_edges_are_separate(self):
        result=branch_inventory(gate,{'cast':cast},clock)
        self.assertEqual(len(result['branches']),2)
        self.assertTrue(result['branches'][0]['temporal'])
        self.assertFalse(result['branches'][1]['temporal'])
        self.assertTrue(all(row['supported'] for row in result['branches']))

    def test_unknown_context_is_not_promoted_to_success(self):
        result=branch_inventory(dynamic_gate,{},clock)
        self.assertFalse(result['branches'][0]['supported'])

    def test_clock_witnesses_do_not_mutate_saved_clock(self):
        scenarios=temporal_scenarios(7,4)
        self.assertEqual(len(scenarios),28)
        self.assertEqual(clock.date,1)
        self.assertEqual(len({row['tick'] for row in scenarios}),28)
        self.assertEqual({row['period'] for row in scenarios},set(range(4)))

    def test_readable_inventory_does_not_claim_acceptance(self):
        row={'id':'gate1','source':'native.module.callback','requirements':[],
             'analysis':branch_inventory(gate,{'cast':cast},clock)}
        rendered=render_inventory({'gates':[row]})
        self.assertIn('not a passed-gate certificate',rendered)
        self.assertIn('gate1',rendered)

    def test_mutually_exclusive_times_have_separate_witnesses(self):
        def expression(period):return {'kind':'operation','operator':'==',
            'left':{'kind':'path','parts':['time','period']},'right':{'kind':'literal','value':period}}
        scenarios=[(i,{'time.period':i}) for i in range(4)]
        self.assertEqual(branch_witnesses(expression(0),scenarios)['true'],[0])
        self.assertEqual(branch_witnesses(expression(3),scenarios)['true'],[3])

    def test_missing_child_count_stays_unknown(self):
        expression={'kind':'path','parts':['cast','anon','babies']}
        self.assertEqual(branch_witnesses(expression,[(0,{})])['unknown'],[0])

if __name__=='__main__':unittest.main()
