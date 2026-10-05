"""Guard native settings against duplicate injection and unsupported layouts."""
import ast
from pathlib import Path
from types import SimpleNamespace as Node
import unittest

source = Path(__file__).resolve().parents[1] / 'mods/controls_guide/controls_guide.rpy'
lines = source.read_text(encoding='utf-8').splitlines()
start = lines.index('init 998 python:') + 1
end = lines.index('init 999 python:')
namespace = {}
exec(compile(ast.parse('\n'.join(line[4:] if line.startswith('    ') else line for line in lines[start:end])), str(source), 'exec'), namespace)
install = namespace['_ssct_install_controls']


def native_layout():
    tab = Node(keyword=[('action', "SetField(persistent, 'pref', 'display')")])
    tabs = Node(name='hbox', children=[tab])
    content = Node(entries=[("persistent.pref == 'sound'", Node(children=[]))])
    grid = Node(name='vpgrid', children=[content], keyword=[('cols', '2')])
    return Node(children=[tabs, grid]), tabs, grid


class ControlsHookTests(unittest.TestCase):
    def test_preserves_native_content_and_is_idempotent(self):
        screen, tabs, grid = native_layout()
        native_tab, native_content = tabs.children[0], grid.children[0]
        self.assertTrue(install(screen, Node(name='mod_tab'), Node(name='mod_rows')))
        self.assertTrue(install(screen, Node(name='mod_tab'), Node(name='mod_rows')))
        self.assertIs(tabs.children[0], native_tab)
        self.assertIs(grid.children[0], native_content)
        self.assertEqual(len(tabs.children), 2)
        self.assertEqual(len(grid.children), 2)
        expr = dict(grid.keyword)['cols']
        self.assertEqual(eval(expr, {'persistent': Node(pref='display')}), 2)
        self.assertEqual(eval(expr, {'persistent': Node(pref='ssct_controls_guide')}), 1)

    def test_rejects_missing_grid_without_partial_mutation(self):
        screen, tabs, grid = native_layout()
        screen.children.remove(grid)
        self.assertFalse(install(screen, Node(), Node()))
        self.assertEqual(len(tabs.children), 1)

    def test_rejects_ambiguous_layout(self):
        screen, tabs, grid = native_layout()
        screen.children.append(Node(name='hbox', children=list(tabs.children)))
        self.assertFalse(install(screen, Node(), Node()))
        self.assertEqual(len(grid.children), 1)


if __name__ == '__main__':
    unittest.main()
