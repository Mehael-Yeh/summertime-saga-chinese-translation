import unittest
from types import SimpleNamespace as NS
from native_tests.screen_catalogue import screen_inventory


class ScreenCatalogue(unittest.TestCase):
    def inventory(self, root):
        return screen_inventory({('native', None): NS(function=root)})

    def test_nested_conditions_and_sensitive_actions_remain_inventory(self):
        button = NS(keyword=[('sensitive', 'who in place'), ('action', 'Emit(interact=who)')], children=[])
        condition = NS(entries=[('saga.time.dark', NS(children=[button]))])
        result = self.inventory(NS(children=[condition]))
        self.assertEqual({row['kind'] for row in result['conditions']}, {'if', 'sensitive', 'action'})
        self.assertTrue(all(row['status']=='inventory_only_not_validated' for row in result['conditions']))
        self.assertEqual(result['unresolved_nodes'], [])

    def test_local_expressions_are_not_executed(self):
        result = self.inventory(NS(expression='dangerous_default()', children=[]))
        self.assertEqual(result['conditions'][0]['expression'], 'dangerous_default()')

    def test_python_branches_preserve_state_effect_barrier(self):
        result = self.inventory(NS(code=NS(source='mutate()\nif ready:\n    pass')))
        self.assertTrue(result['conditions'][0]['requires_native_prior_effects'])

    def test_wrapped_roots_and_unknown_schema_are_explicit(self):
        def wrapper():
            raise AssertionError('Never execute screen functions')
        wrapper.__wrapped__ = NS(children=[NS(new_native_schema=True)])
        result = self.inventory(wrapper)
        self.assertEqual(result['unresolved_nodes'][0]['reason'], 'unrecognized_screen_node')


if __name__ == '__main__':
    unittest.main()
