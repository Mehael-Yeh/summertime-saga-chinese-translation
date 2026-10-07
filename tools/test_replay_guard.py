import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location(
    'replay_guard', pathlib.Path(__file__).parent / 'native_tests/replay_guard.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReplayGuardTests(unittest.TestCase):
    def test_direct_native_write_is_a_postcondition_without_execution(self):
        import types
        actors=types.SimpleNamespace(person=types.SimpleNamespace(token=5))
        scope={'actors':actors}
        exec('def callback():\n    actors.person.token = 7\n    raise RuntimeError("must not execute")',scope)
        fields={(kind,ref):names for kind,ref,names in module.catalogue_effect_fields(scope['callback'],{'cast':actors})}
        self.assertIn('token',fields['cast','person'])
        self.assertEqual(actors.person.token,5)

    def test_animation_write_is_not_added_to_scheduler_reads(self):
        import types
        actors=types.SimpleNamespace(person=types.SimpleNamespace(when=1))
        scope={'actors':actors}
        exec('def callback():\n    actors.person.when = 2',scope)
        reads=module.catalogue_dependencies(scope['callback'],{'cast':actors})
        effects=module.catalogue_effect_fields(scope['callback'],{'cast':actors})
        self.assertNotIn('when',reads[0][2])
        self.assertIn('when',effects[0][2])

    def test_animation_timestamp_cannot_revive_a_goal(self):
        import types
        actors=types.SimpleNamespace(person=types.SimpleNamespace(memo=set(),when=1,cash=10))
        scope={'actors':actors}
        exec('def callback():\n    return actors.person.cash',scope)
        dependencies=module.catalogue_dependencies(scope['callback'],{'cast':actors})
        self.assertEqual(dependencies,(('cast','person',('cash','memo','step','where')),))
        fields=dependencies[0][2]
        before=module.stored_facts(actors.person,included=fields)
        actors.person.when=2
        self.assertEqual(before,module.stored_facts(actors.person,included=fields))
        actors.person.cash=20
        self.assertNotEqual(before,module.stored_facts(actors.person,included=fields))

    def test_navigation_cycles_suspend_but_long_acyclic_paths_work(self):
        scheduler=module.DependencyScheduler()
        for index in range(100):
            self.assertFalse(scheduler.navigation_cycle('task','same',(index,index+1)))
        self.assertTrue(scheduler.navigation_cycle('task','same',(0,1)))
        self.assertFalse(scheduler.eligible('task','same'))
        self.assertFalse(scheduler.navigation_cycle('task','key_acquired',(0,1)))
        self.assertTrue(scheduler.eligible('task','key_acquired'))

    def test_frontiers_do_not_certify_unfinished_waits_or_old_placeholders(self):
        stages=('new01_setup','new99_hold','new100_setup','new101_hold')
        self.assertEqual(module.finite_endpoint_kind('null',stages),'native_null')
        self.assertIsNone(module.finite_endpoint_kind('new99_hold',stages,True,'Future',0))
        self.assertIsNone(module.finite_endpoint_kind('new101_hold',stages,True,'Future',1))
        self.assertIsNone(module.finite_endpoint_kind('new101_hold',stages,False,'Future',0))
        self.assertEqual(module.finite_endpoint_kind('new101_hold',stages,True,'Future',0),'native_future_placeholder')

    def test_notes_query_is_derived_from_screen_not_version_or_method_name(self):
        self.assertEqual(module.native_screen_query('what.notes()'),'notes')
        self.assertEqual(module.native_screen_query('what.note()'),'note')
        self.assertEqual(module.native_screen_query('what.future_task_list()'),'future_task_list')
        self.assertIsNone(module.native_screen_query('what.note(force=True)'))
        self.assertIsNone(module.native_screen_query('other.note()'))
    def test_notes_wait_is_not_a_manual_task_and_localization_does_not_matter(self):
        self.assertEqual(module.task_priority(True,'Purchase a wrench.'),0)
        self.assertEqual(module.task_priority(True,'购买扳手。'),0)
        self.assertIsNone(module.task_priority(True,False))
        self.assertIsNone(module.task_priority(True,None))
        self.assertEqual(module.task_priority(False,None),1)
    def test_reminder_waits_for_a_real_prerequisite_change(self):
        scheduler=module.DependencyScheduler()
        self.assertEqual(scheduler.observe('npc_task','no_key','no_key'),'await_prerequisite_change')
        self.assertFalse(scheduler.eligible('npc_task','no_key'))
        self.assertTrue(scheduler.eligible('npc_task','has_key'))
        self.assertEqual(scheduler.observe('npc_task','has_key','task_advanced'),'observed_state_change')

    def test_successful_walk_does_not_complete_or_suspend_its_goal(self):
        scheduler=module.DependencyScheduler()
        self.assertEqual(scheduler.observe('npc_task','same','same',navigation=True),'journey')
        self.assertTrue(scheduler.eligible('npc_task','same'))
        self.assertEqual(scheduler.observe('npc_task','same','same',navigation=True,reached=False),'await_prerequisite_change')

    def test_blocked_goal_does_not_block_other_prerequisite_actions(self):
        scheduler=module.DependencyScheduler()
        scheduler.observe('borrow','missing_card','missing_card')
        self.assertTrue(scheduler.eligible('get_card','missing_card'))
        self.assertFalse(scheduler.eligible('borrow','missing_card'))

    def test_stored_facts_reads_slots_without_running_computed_properties(self):
        class Native:
            __slots__=('memo','where')
            def __init__(self):self.memo={'flag':False};self.where='room'
            @property
            def plan(self):raise AssertionError('computed native code must not run')
        actor=Native()
        before=module.stored_facts(actor,ignored=('where',))
        actor.where='hall'
        self.assertEqual(before,module.stored_facts(actor,ignored=('where',)))
        actor.memo['flag']=True
        self.assertNotEqual(before,module.stored_facts(actor,ignored=('where',)))

    def test_callback_catalogue_dependencies_are_read_without_executing(self):
        import types
        actor_module=types.ModuleType('saga.cast')
        function_globals={'actors':actor_module}
        exec('def callback():\n    value = actors.person\n    raise AssertionError("must not execute")',function_globals)
        self.assertEqual(module.catalogue_references(function_globals['callback']),(('cast','person'),))

    def test_catalogue_proxy_and_aliased_global_keep_dependency_identity(self):
        catalogue=object()
        function_globals={'people':catalogue}
        exec('def callback():\n    return people.person',function_globals)
        self.assertEqual(module.catalogue_references(function_globals['callback'],{'cast':catalogue}),
                         (('cast','person'),))

    def test_native_menu_goal_reads_only_literal_event_inputs(self):
        self.assertEqual(module.native_choice_target("saga.event.emit(choice='topic', who=saga.cast.actor)"),('topic','actor'))
        self.assertIsNone(module.native_choice_target("saga.event.emit(choice=get_topic(), who=saga.cast.actor)"))
        self.assertIsNone(module.native_choice_target("other.emit(choice='topic', who=saga.cast.actor)"))
        self.assertIsNone(module.native_choice_target("saga.event.emit(choice='topic', who=actor)"))

    def test_filter_order_does_not_reset_attempts_after_restart(self):
        first=[('who','actor'),('choice','topic')]
        second=list(reversed(first))
        self.assertEqual(module.filter_key(first),module.filter_key(second))
        self.assertNotEqual(module.filter_key(first),module.filter_key([('who','other'),('choice','topic')]))

    def test_clock_does_not_inject_dawn_or_run_in_a_device(self):
        self.assertFalse(module.clock_button_allowed('nav', False, 3, 0))
        self.assertFalse(module.clock_button_allowed('nav', True, 0, 1))
        self.assertFalse(module.clock_button_allowed('use', False, 0, 1))
        self.assertTrue(module.clock_button_allowed('nav', False, 0, 1))

    def test_current_replay_python_blocks_compile_before_game_launch(self):
        path = pathlib.Path(__file__).parent / 'native_tests/perfect_save_route_execution.rpy'
        self.assertEqual(module.validate_python_blocks(path), 2)

    def test_all_native_probe_python_blocks_compile_before_game_launch(self):
        paths=list((pathlib.Path(__file__).parent/'native_tests').glob('*.rpy'))
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(probe=path.name):module.validate_python_blocks(path)

    def test_navigation_uses_first_visible_hop_not_remote_destination(self):
        graph = {'room': ['hall'], 'hall': ['outside'], 'outside': ['shop'], 'shop': []}
        self.assertEqual(module.first_visible_hop('room', 'shop', graph.get), 'hall')

    def test_navigation_cycles_do_not_fake_a_path(self):
        graph = {'room': ['hall'], 'hall': ['room']}
        self.assertIsNone(module.first_visible_hop('room', 'shop', graph.get))

    def test_telescope_view_is_not_a_road_to_distant_actor(self):
        graph = {'room':['scope','hall'], 'scope':['church'], 'hall':['map'],
                 'map':['church'], 'church':[]}
        physical={'room','hall','map','church'}
        self.assertEqual(module.first_visible_hop('room','church',graph.get,physical.__contains__),'hall')
        self.assertEqual(module.first_visible_hop('room','scope',graph.get,physical.__contains__),'scope')

    def test_unreachable_actor_seen_only_in_device_has_no_physical_path(self):
        graph={'room':['scope'],'scope':['church'],'church':[]}
        self.assertIsNone(module.first_visible_hop('room','church',graph.get,lambda x:x!='scope'))

    def test_navigation_rechecks_changed_visible_destinations(self):
        graph = {'room': ['hall'], 'hall': []}
        self.assertIsNone(module.first_visible_hop('room', 'shop', graph.get))
        graph['hall'].append('shop');graph['shop']=[]
        self.assertEqual(module.first_visible_hop('room', 'shop', graph.get), 'hall')

    def test_reentering_menu_visits_other_enabled_choices(self):
        visits = {}
        offered = ['topic', 'exercise', 'leave']
        self.assertEqual([module.choose_unexplored(offered, visits, 'menu')
                          for _ in range(3)], offered)

    def test_separate_menus_do_not_share_choice_counts(self):
        visits = {}
        module.choose_unexplored(['a', 'b'], visits, 'first')
        self.assertEqual(module.choose_unexplored(['a', 'b'], visits, 'second'), 'a')

    def test_same_dialogue_stalls(self):
        guard = module.ReplayGuard()
        self.assertIsNone(guard.observe(0, ('say', 1), 'quest'))
        self.assertEqual(guard.observe(3, ('say', 1), 'quest'), 'unchanged_interaction')

    def test_new_dialogue_in_same_quest_is_progress(self):
        guard = module.ReplayGuard()
        for index in range(100):
            self.assertIsNone(guard.observe(index, ('say', index), 'quest'))

    def test_same_inventory_screen_with_different_items_is_not_a_cycle(self):
        guard = module.ReplayGuard()
        for index in range(100):
            self.assertIsNone(guard.observe(index, ('pause', 'inv', str(index)), 'quest'))

    def test_shared_map_action_from_different_places_is_not_a_cycle(self):
        guard = module.ReplayGuard()
        for index in range(100):
            self.assertIsNone(guard.observe(index, ('nav', 'place'+str(index), 'map'), 'quest'))

    def test_dialogue_cycle_is_bounded(self):
        guard = module.ReplayGuard(repeat_limit=3)
        for index in range(4):
            self.assertIsNone(guard.observe(index / 10, index % 2, 'quest'))
        self.assertEqual(guard.observe(.4, 0, 'quest'), 'repeated_interaction_cycle')

    def test_native_state_change_resets_cycle_count(self):
        guard = module.ReplayGuard(repeat_limit=2)
        for index in range(40):
            self.assertIsNone(guard.observe(index, index % 2, index // 2))

    def test_planning_time_does_not_count_as_screen_idle(self):
        guard = module.ReplayGuard()
        guard.observe(0, 'screen', 'quest')
        guard.begin_interaction(10)
        self.assertIsNone(guard.observe(10.1, 'screen', 'quest'))
        self.assertEqual(guard.observe(13, 'screen', 'quest'), 'unchanged_interaction')

    def test_successful_journey_does_not_consume_failure_budget(self):
        self.assertTrue(module.navigation_succeeded('navigation','a',None,'b',None,'b'))
        self.assertTrue(module.navigation_succeeded('navigation','a',None,'a','map','map'))

    def test_native_fence_is_not_a_successful_journey(self):
        self.assertFalse(module.navigation_succeeded('navigation','a',None,'a',None,'b'))

    def test_back_requires_actual_context_change(self):
        self.assertTrue(module.navigation_succeeded('navigation_back','a','map','a',None,None))
        self.assertFalse(module.navigation_succeeded('navigation_back','a',None,'a',None,None))

    def test_new_interactions_do_not_erase_cycle_evidence(self):
        guard = module.ReplayGuard(repeat_limit=3)
        for index in range(4):
            guard.begin_interaction(index * 10)
            self.assertIsNone(guard.observe(index * 10, index % 2, 'quest'))
        guard.begin_interaction(40)
        self.assertEqual(guard.observe(40, 0, 'quest'), 'repeated_interaction_cycle')


class GlobalProgramInputTests(unittest.TestCase):
    def test_pc_timer_refresh_is_not_new_content(self):
        self.assertEqual(module.window_input_state({'mail':{'st':100,'mode':'inbox'}}),
                         module.window_input_state({'mail':{'st':200,'mode':'inbox'}}))

    def test_pc_content_change_is_observed(self):
        self.assertNotEqual(module.window_input_state({'mail':{'st':100,'mode':'inbox'}}),
                            module.window_input_state({'mail':{'st':100,'mode':'message'}}))

    def test_window_state_observation_does_not_mutate_native_ram(self):
        ram={'mail':{'st':100,'mode':'inbox'}}
        module.window_input_state(ram)
        self.assertEqual(ram,{'mail':{'st':100,'mode':'inbox'}})

    def test_missing_interact_is_not_a_declared_back_button(self):
        self.assertFalse(module.declared_input_matches({'app':'sys','op':'quit'},{'interact':None}))
        self.assertTrue(module.declared_input_matches({'interact':None},{'interact':None}))

    def test_actual_button_must_declare_every_pending_field(self):
        self.assertFalse(module.declared_input_matches({'interact':'item'},{'interact':'item','choice':'take'}))
        self.assertFalse(module.declared_input_matches({'interact':'another'},{'interact':'item'}))

    def test_native_extra_context_is_preserved_by_selecting_actual_action(self):
        actual={'interact':'item','source':'shop'}
        self.assertTrue(module.declared_input_matches(actual,{'interact':'item'}))
        self.assertEqual(actual['source'],'shop')

    def test_frozen_global_job_filter_is_admitted(self):
        def job():pass
        item=object()
        self.assertTrue(module.has_public_program_input([(job,frozenset({('interact',item)}),None,0)],{item}))

    def test_dialogue_completion_notification_is_not_a_button(self):
        def listener():pass
        actor=object()
        self.assertFalse(module.has_public_program_input([(listener,frozenset({('who',actor),('choice',None)}),None,0)],{actor}))
        self.assertTrue(module.has_public_program_input([(listener,frozenset({('who',actor),('choice','task')}),None,0)],{actor}))

    def test_navigation_program_is_not_independent_quest(self):
        def navigation():pass
        navigation.__module__='saga.logic.auto'
        item=object()
        self.assertFalse(module.has_public_program_input([(navigation,frozenset({('interact',item)}),None,0)],{item}))


if __name__ == '__main__':
    unittest.main()
