"""Check catalogue changes without pretending to validate an untested engine."""

import ast
from pathlib import Path
from types import SimpleNamespace as Node
import textwrap
import unittest


def helpers():
    path = Path(__file__).resolve().parents[1] / 'mods/perfect_save/perfect_save.rpy'
    body = path.read_text(encoding='utf-8').split('init 998 python:\n', 1)[1]
    body = body.split('\ninit 999 python:', 1)[0]
    module = ast.parse(textwrap.dedent(body))
    wanted = {'_ssct_perfect_stages', '_ssct_perfect_terminal', '_ssct_perfect_open_targets', '_ssct_perfect_contacts', '_ssct_perfect_reset_supported'}
    module.body = [node for node in module.body
                   if isinstance(node, ast.FunctionDef) and node.name in wanted]
    namespace = {}
    exec(compile(module, str(path), 'exec'), namespace)
    return namespace


class CatalogueCompatibility(unittest.TestCase):
    def setUp(self):
        namespace = helpers()
        self.stages = namespace['_ssct_perfect_stages']
        self.terminal = namespace['_ssct_perfect_terminal']
        self.route = Node(ref='example')
        self.empty = Node(ref='null')

    def node(self, ref, *, waiting=False, pool=()):
        return Node(ref=ref, done=True if waiting else 50.0,
                    hint='Native future-content hint' if waiting else None,
                    pool=pool)

    def test_route_names_and_three_digit_quest_numbers(self):
        valid = self.node('example100_setup')
        other = self.node('example_extra100_setup')
        self.assertEqual(self.stages(self.route, [other, valid]), (valid,))

    def test_newer_number_supersedes_retained_old_placeholder(self):
        old = self.node('example99_hold', waiting=True)
        new = self.node('example100_play', pool=('native event',))
        self.assertIs(self.terminal(self.route, [old, new], self.empty), self.empty)

    def test_current_native_placeholder_requires_no_named_node(self):
        new = self.node('example107_future', waiting=True)
        old = self.node('example09_play')
        self.assertIs(self.terminal(self.route, [new, old], self.empty), new)

    def test_actionful_hint_is_not_a_future_terminal(self):
        active = self.node('example12_setup', waiting=True, pool=('event',))
        self.assertIs(self.terminal(self.route, [active], self.empty), self.empty)

    def test_no_quests_is_empty(self):
        self.assertIs(self.terminal(self.route, [], self.empty), self.empty)

    def test_untracked_native_clear_uses_none_endpoint(self):
        self.assertIsNone(self.terminal(self.route,[self.node('example01_outro')],None))

    def test_ambiguous_current_future_endpoints_fail_before_save(self):
        first=self.node('example12_future_a',waiting=True)
        second=self.node('example12_future_b',waiting=True)
        with self.assertRaisesRegex(ValueError,'Ambiguous native'):
            self.terminal(self.route,[first,second],self.empty)


class NativeOpeningDiscovery(unittest.TestCase):
    def setUp(self):
        namespace = helpers()
        self.place = Node(ref='native_place')
        self.catalogue = Node(native_place=self.place)
        namespace['saga'] = Node(sets=self.catalogue)
        self.discover = namespace['_ssct_perfect_open_targets']

    def callback(self, source, **values):
        namespace = {'sets': self.catalogue, **values}
        exec(source, namespace)
        return namespace['callback']

    def targets(self, callback):
        return self.discover([Node(pool=[(callback, None)])], [self.place])

    def test_native_literal_is_discovered_without_running_callback(self):
        # The native opening must be in reachable bytecode, after a side effect.
        callback = self.callback('def callback():\n    forbidden()\n    sets.native_place.open()',
                                 forbidden=lambda: self.fail('callback executed'))
        self.assertEqual(self.targets(callback), (self.place,))

    def test_native_default_target(self):
        callback = self.callback('def callback(place=sets.native_place):\n    place.open()')
        self.assertEqual(self.targets(callback), (self.place,))

    def test_native_helper_is_inspected_without_execution(self):
        helper = self.callback('def callback():\n    sets.native_place.open()')
        helper.__module__ = 'saga.logic.example'
        callback = self.callback('def callback():\n    helper()', helper=helper)
        self.assertEqual(self.targets(callback), (self.place,))

    def test_unknown_object_is_not_opened(self):
        callback = self.callback('def callback(other=other):\n    other.open()', other=Node())
        self.assertEqual(self.targets(callback), ())

    def test_empty_future_node_has_no_opening(self):
        self.assertEqual(self.discover([Node(pool=())], [self.place]), ())


class DailyResetProtocol(unittest.TestCase):
    def setUp(self):self.supported=helpers()['_ssct_perfect_reset_supported']

    def test_future_actor_literal_state_and_memory_reset(self):
        def reset(ctx):
            ctx.work=False
            ctx.remove('sleep','temporary')
        self.assertTrue(self.supported(reset))

    def test_story_or_unknown_helper_must_not_execute(self):
        def reset(ctx):
            forbidden_story()
        self.assertFalse(self.supported(reset))

    def test_dynamic_memory_arguments_are_not_assumed_safe(self):
        def reset(ctx,flag):
            ctx.remove(flag)
        self.assertFalse(self.supported(reset))

    def test_unbounded_reset_loop_is_rejected(self):
        def reset(ctx):
            while True:ctx.work=False
        self.assertFalse(self.supported(reset))


class ContactEligibility(unittest.TestCase):
    def setUp(self):
        namespace=helpers()
        self.images=True
        self.art=True
        namespace['renpy']=Node(has_image=lambda _:self.images,loadable=lambda _:self.art)
        self.contacts=namespace['_ssct_perfect_contacts']
        self.actor=Node(ref='native_actor',type='town',info=(),name='Native name',
                        age=30,kind='f',size='C',bio='Native background')

    def test_complete_native_profile_is_accepted(self):
        self.assertEqual(self.contacts([self.actor]),[self.actor])

    def test_incidental_face_does_not_create_a_biography(self):
        del self.actor.info
        self.assertEqual(self.contacts([self.actor]),[])
        self.assertFalse(hasattr(self.actor,'info'))

    def test_wrong_statistics_shape_is_rejected(self):
        self.actor.info='not native cards'
        self.assertEqual(self.contacts([self.actor]),[])

    def test_missing_background_is_rejected(self):
        del self.actor.bio
        self.assertEqual(self.contacts([self.actor]),[])

    def test_missing_profile_art_is_rejected(self):
        self.art=False
        self.assertEqual(self.contacts([self.actor]),[])

    def test_female_size_required_but_male_size_is_not(self):
        del self.actor.size
        self.assertEqual(self.contacts([self.actor]),[])
        self.actor.kind='m'
        self.assertEqual(self.contacts([self.actor]),[self.actor])


if __name__ == '__main__':
    unittest.main()
