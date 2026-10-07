"""Price adaptation must not zero unrelated native aggregates."""
import ast
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


def price_total():
    path=Path(__file__).resolve().parents[1]/'mods/perfect_save/reacquisition.rpy'
    body=path.read_text(encoding='utf8').split('init 998 python:\n',1)[1].split('\ninit 999 python:',1)[0]
    module=ast.parse(textwrap.dedent(body))
    module.body=[node for node in module.body if isinstance(node,ast.FunctionDef) and node.name=='_ssct_owned_zero_total']
    namespace={}
    exec(compile(module,str(path),'exec'),namespace)
    return namespace['_ssct_owned_zero_total']


class NativePriceProtocol(unittest.TestCase):
    def setUp(self):self.total=price_total()

    def test_native_price_generator_is_zero_and_consumed(self):
        items=[SimpleNamespace(cost=100),SimpleNamespace(cost=75)]
        prices=(item.cost for item in items)
        self.assertEqual(self.total(prices),0)
        self.assertEqual(list(prices),[])
        self.assertEqual([item.cost for item in items],[100,75])

    def test_other_generator_keeps_native_sum(self):
        items=[SimpleNamespace(amount=100),SimpleNamespace(amount=75)]
        self.assertEqual(self.total(item.amount for item in items),175)

    def test_other_sum_and_start_remain_native(self):
        self.assertEqual(self.total([100,75],5),180)

    def test_native_invalid_price_property_is_not_silently_skipped(self):
        class Item:
            @property
            def cost(self):raise ValueError('native price invalid')
        with self.assertRaisesRegex(ValueError,'native price invalid'):
            self.total(item.cost for item in [Item()])


if __name__=='__main__':unittest.main()
