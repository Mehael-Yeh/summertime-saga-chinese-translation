import ast
import textwrap
import sys
import time
import unittest
from enum import IntEnum
from pathlib import Path
from types import SimpleNamespace as NS, ModuleType
from unittest.mock import patch
from native_tests import native_wallet_protocol
from native_tests import replay_guard


class Function:
    def __init__(self, callable, *args):
        self.callable, self.args = callable, args


class Emit:
    def __init__(self, value):
        self.value = value


class Return:
    def __init__(self, value):
        self.value = value


class Screen:
    def __init__(self, game=None, nodes=()):
        self.scope, self.nodes = {'game': game}, nodes

    def visit_all(self, append):
        append(self)  # Non-button nodes have no is_sensitive method.
        for node in self.nodes:
            append(node)


class EndInteraction(Exception):
    pass


class NavigationResponses(unittest.TestCase):
    def test_drag_without_button_sensitivity_is_unknown_and_not_dispatched(self):
        drag=NS(clicked=Emit({'app':'pics','op':'init'}))
        self.screens['use']=Screen(nodes=[drag])
        self.assertIsNone(self.namespace['_ssct_navigation_sensitivity'](drag))
        self.assertEqual(self.namespace['_ssct_navigation_controls'](),[])
        self.namespace['json']=__import__('json')
        self.assertTrue(self.namespace['_ssct_navigation_surface']())

    def setUp(self):
        source = Path(__file__).parent / 'native_tests/perfect_save_navigation_responses.rpy'
        body = source.read_text(encoding='utf8').split('init 1000 python:\n', 1)[1].split('\nlabel ', 1)[0]
        tree = ast.parse(textwrap.dedent(body))
        functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
        self.state = NS(phase=4, started=time.monotonic(), row={}, advances=0)
        self.probe = NS(**vars(self.state))
        self.patch = patch.dict(sys.modules, {'ssct_navigation_probe': self.probe})
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.screens = {}
        self.actions = []
        def run(action):
            self.actions.append(action)
            if isinstance(action, Function):
                return action.callable(*action.args)
        def end(value):
            raise EndInteraction(value)
        self.namespace = {'sys': sys, 'time': time, 'Function': Function, 'Emit': Emit, 'Return': Return,
                          'native_wallet_protocol':native_wallet_protocol,
                          'ssct_replay_guard':replay_guard,
                          'renpy': NS(get_mode=lambda: 'screen', get_screen=self.screens.get,
                                      run=run, end_interaction=end,
                                      game=NS(script=NS(namemap={}),context=lambda:NS(current='native-statement')))}
        exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), self.namespace)

    def keypad(self, goal, code=''):
        module = ModuleType('native_test_keypad')
        module.goal = goal
        Game = type('Game', (), {'__module__': module.__name__})
        game = Game()
        game.code, game.wait = code, None
        game.received = []
        game.input = game.received.append
        actions = [Function(game.input, digit) for digit in '123456789*0#']
        self.screens['mini_keypad'] = Screen(game, [NS(clicked=action, is_sensitive=lambda: True) for action in actions])
        self.patch_module = patch.dict(sys.modules, {module.__name__: module})
        self.patch_module.start()
        self.addCleanup(self.patch_module.stop)
        return game

    def test_keypad_uses_this_native_module_goal_and_rendered_button(self):
        game = self.keypad('8391', '83')
        self.namespace['_ssct_navigation_tick']()
        self.assertEqual(game.received, ['9'])
        self.assertEqual(self.probe.row['device_inputs'][0]['input'], '9')
        self.assertFalse(self.probe.row['device_inputs'][0]['return_stubbed'])

    def test_keypad_submits_with_native_hash_button(self):
        game = self.keypad('8391', '8391')
        self.namespace['_ssct_navigation_tick']()
        self.assertEqual(game.received, ['#'])

    def test_unsupported_keypad_recipe_fails_before_input(self):
        game = self.keypad('8391', '0')
        with self.assertRaisesRegex(ValueError, 'Unsupported native keypad recipe'):
            self.namespace['_ssct_navigation_tick']()
        self.assertEqual(game.received, [])

    def test_clock_scenario_uses_rendered_action_without_assigning_saved_time(self):
        class Tod(IntEnum):
            dawn=0
            noon=1
            dusk=2
            dark=3
        clock = NS(now=4, tod=Tod.dawn, dawn=Tod.dawn, noon=Tod.noon, dusk=Tod.dusk, dark=Tod.dark)
        self.namespace['saga'] = NS(time=clock)
        action = Emit({'interact': Tod.noon})
        self.screens['nav'] = Screen(nodes=[NS(clicked=action, is_sensitive=lambda: True)])
        self.probe.phase, self.probe.tick, self.probe.clock_inputs = 5, 5, []
        with self.assertRaises(EndInteraction):
            self.namespace['_ssct_navigation_tick']()
        self.assertEqual(self.actions, [action])
        self.assertEqual(clock.now, 4)
        self.assertEqual(self.probe.phase, 6)

    def next_frontier(self, interactions):
        self.probe.pending=[{'slot':'device-checkpoint','source_path':[{'protocol':'interaction','event_signature':'native-input'}]}]
        self.probe.cases, self.probe.limit = 0, 10
        self.probe.run_started=time.monotonic()
        self.probe.include_interactions=interactions
        self.probe.baseline_slot='stable-room-baseline'
        self.namespace['_ssct_navigation_write']=lambda status:None
        loaded=[]
        self.namespace['renpy'].load=loaded.append
        self.namespace['_ssct_navigation_next']()
        return loaded

    def test_devices_replay_native_paths_from_stable_baseline(self):
        self.assertEqual(self.next_frontier(True), ['stable-room-baseline'])
        self.assertEqual(self.probe.replay_pending, [{'protocol':'interaction','event_signature':'native-input'}])

    def test_navigation_checkpoints_do_not_replay_from_wrong_parent(self):
        self.assertEqual(self.next_frontier(False), ['device-checkpoint'])
        self.assertEqual(self.probe.replay_pending, [])

    def test_navigation_anchor_loads_saved_place_and_keeps_full_input_provenance(self):
        prefix=[{'protocol':'sets','target':'place'}]
        tail=[{'protocol':'interaction','target':'device'}]
        case={'slot':'device-snapshot','source_path':prefix+tail,
              'replay_anchor':{'kind':'ordinary_navigation','slot':'native-place','path':prefix}}
        self.assertEqual(replay_guard.native_replay_start(case,'room',True),('native-place',prefix,tail))

    def test_device_checkpoint_or_changed_prefix_cannot_skip_native_inputs(self):
        for anchor in ({'kind':'device','slot':'unsafe','path':[]},
                       {'kind':'ordinary_navigation','slot':'place','path':[{'target':'different'}]}):
            with self.assertRaises(ValueError):
                replay_guard.native_replay_start({'source_path':[],'replay_anchor':anchor},'room',True)

    def test_waiting_keypad_cannot_bypass_response_deadline(self):
        game=self.keypad('8391')
        game.wait=True
        self.probe.started=time.monotonic()-16
        with self.assertRaisesRegex(ValueError,'interaction deadline'):
            self.namespace['_ssct_navigation_tick']()
        self.assertEqual(game.received,[])

    def test_replay_cannot_reset_case_deadline(self):
        self.probe.phase=3
        self.probe.started=time.monotonic()
        self.probe.case_started=time.monotonic()-31
        with self.assertRaisesRegex(ValueError,'case replay deadline'):
            self.namespace['_ssct_navigation_tick']()

    def test_menu_frontier_includes_only_actual_sensitive_rendered_actions(self):
        enabled, disabled, hidden = object(), object(), object()
        screen=Screen(nodes=[NS(clicked=enabled,is_sensitive=lambda:True),
                             NS(clicked=disabled,is_sensitive=lambda:False)])
        screen.scope['items']=[NS(action=enabled),NS(action=disabled),NS(action=hidden)]
        self.screens['choice']=screen
        self.assertEqual([index for index,item in self.namespace['_ssct_navigation_choices']()], [0])

    def test_path_descriptors_do_not_recursively_embed_frontiers(self):
        self.probe.current_path=[]
        self.probe.is_replay=True
        self.probe.dispatch={'protocol':'choice','target':'Continue','choice_index':1,
                             'source_path':[{'protocol':'other'}],'slot':'checkpoint','source_context':'context'}
        self.namespace['_ssct_navigation_path_input']()
        self.assertEqual(self.probe.current_path,[{'protocol':'choice','target':'Continue','choice_index':1}])

    def test_completed_interaction_does_not_reexplore_unrelated_town_states(self):
        self.probe.include_interactions=True
        self.probe.current_path=[{'protocol':'interaction'}]
        self.probe.tick=4
        self.probe.rows=[{}]
        self.namespace['saga']=NS(time=NS(now=4),gui=NS(step=NS(ref='nav')),
                                  camera=NS(what=NS(ref='room'),focus=None))
        self.namespace['_ssct_navigation_expand']()
        self.assertTrue(self.probe.rows[-1]['interaction_case_terminal'])

    def test_device_return_adapter_uses_only_rendered_sensitive_buttons(self):
        enabled, disabled=Return(False),Return(True)
        self.screens['use']=Screen(nodes=[NS(clicked=enabled,is_sensitive=lambda:True),
                                         NS(clicked=disabled,is_sensitive=lambda:False)])
        self.assertEqual(self.namespace['_ssct_navigation_returns'](),[enabled])

    def test_literal_native_call_screen_uses_its_actual_input_surface(self):
        self.namespace['renpy'].game.script.namemap['native-statement']=NS(line='call screen arbitrary_device(who)')
        control=Return(None)
        self.screens['arbitrary_device']=Screen(nodes=[NS(clicked=control,is_sensitive=lambda:True)])
        self.assertEqual(self.namespace['_ssct_navigation_called_screen']()[0],'arbitrary_device')
        self.assertEqual(self.namespace['_ssct_navigation_returns'](),[control])

    def test_computed_call_screen_target_is_not_evaluated(self):
        self.namespace['renpy'].game.script.namemap['native-statement']=NS(line='call screen expression danger()')
        self.assertEqual(self.namespace['_ssct_navigation_called_screen'](),(None,None))

    def test_targeted_frontier_keeps_original_native_input_path(self):
        self.probe.seed_case={'source_context':'original','source_path':[], 'target':'device','protocol':'interaction'}
        self.namespace['_ssct_navigation_initial_frontier']()
        self.assertEqual(self.probe.pending,[self.probe.seed_case])

    def test_targeted_frontier_rejects_missing_source_provenance(self):
        self.probe.seed_case={'source_path':[],'target':'device','protocol':'interaction'}
        with self.assertRaises(ValueError):self.namespace['_ssct_navigation_initial_frontier']()

    def test_device_action_returns_its_real_payload_to_native_screen_caller(self):
        payload=(23,42)
        with self.assertRaises(EndInteraction) as stopped:
            self.namespace['_ssct_navigation_device_run'](Function(lambda:payload))
        self.assertIs(stopped.exception.args[0],payload)


if __name__ == '__main__':
    unittest.main()
