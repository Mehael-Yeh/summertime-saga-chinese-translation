"""Projection primitives: unknown expressions stay unknown; callbacks never run."""
import ast
from pathlib import Path
from types import SimpleNamespace as NS
import textwrap
import unittest
from test_perfect_save_catalogue import helpers


class Label:
    def __init__(self, block): self.block = block


class Return:
    def __init__(self, expression): self.expression = expression


class If:
    def __init__(self, entries): self.entries = entries


class Menu:
    def __init__(self, items): self.items = items


class Jump:
    def __init__(self, target): self.target, self.expression = target, False


class Call:
    def __init__(self, label): self.label, self.expression = label, False


class Python:
    def __init__(self, source): self.code = NS(source=source)


class Catalogue(list):
    def __getattr__(self, ref):
        return next(item for item in self if item.ref == ref)


class Projection(unittest.TestCase):
    def setUp(self):
        import sys
        from unittest.mock import patch
        self.clear=object()
        sentinel_patch=patch.dict(sys.modules,{'saga.util.sentinel':NS(clear=self.clear)})
        sentinel_patch.start()
        self.addCleanup(sentinel_patch.stop)
        path = Path(__file__).resolve().parents[1] / 'mods/perfect_save/completion_state.rpy'
        module = ast.parse(textwrap.dedent(path.read_text(encoding='utf8').split('init 997 python:\n', 1)[1]))
        native = {key: Catalogue() for key in ('cast', 'prop', 'sets', 'step', 'flow')}
        namespace = {'saga': NS(**native, time=NS()),
                     '_ssct_perfect_stages': helpers()['_ssct_perfect_stages'],
                     'renpy': NS(ast=NS(Label=Label, Return=Return, If=If, Menu=Menu, Jump=Jump, Call=Call, Python=Python),
                                 game=NS(script=NS(namemap={}))),
                     '_ssct_completion_catalogues': lambda: native}
        module.body = [node for node in module.body if isinstance(node, ast.FunctionDef)
                       and node.name != '_ssct_completion_catalogues']
        exec(compile(module, str(path), 'exec'), namespace)
        self.ns, self.native = namespace, native

    def returns(self, block):
        self.ns['renpy'].game.script.namemap['future_scene'] = Label(block)
        return self.ns['_ssct_completion_script_returns']('future_scene')

    def test_future_menu_and_branch_literals(self):
        self.assertEqual(self.returns([Menu([('One', 'unknown()', [Return("'tea'")]),
                                             ('Two', 'True', [If([('unknown()', [Return("'coffee'")])])])])]),
                         frozenset(('tea', 'coffee')))

    def test_native_reference_is_resolved_without_eval(self):
        # SimpleNamespace is not hashable, unlike native catalogue entities.
        class Actor:
            ref = 'future_person'
        person = Actor()
        self.native['cast'].append(person)
        self.assertEqual(self.returns([Return('saga.cast.future_person')]), frozenset((person,)))

    def test_arbitrary_expression_is_not_executed(self):
        self.assertEqual(self.returns([Return("__import__('os').system('must_not_run')")]), frozenset())

    def test_script_variable_reply_is_inferred_without_running_python(self):
        self.assertEqual(self.returns([Python("renpy.dynamic(chosen='tea')"), Return('chosen')]),frozenset(('tea',)))

    def test_call_jump_cycle_is_bounded(self):
        self.ns['renpy'].game.script.namemap['other'] = Label([Call('future_scene'), Return("'reward'")])
        self.assertEqual(self.returns([Jump('other')]), frozenset(('reward',)))

    def test_pure_clock_reset_is_settled_without_callback_execution(self):
        final = NS(ref='future_repeat_ready', pool=[])
        functions = {'step': self.native['step']}
        exec('def reset(): return step.future_repeat_ready', functions)
        reset = functions['reset']
        start = NS(ref='future_repeat_reset', pool=[(reset, (), None, 0)])
        flow = NS(ref='future_repeat', step=start)
        self.native['flow'].append(flow)
        self.native['step'].extend((start, final))
        model = {'listeners': {('flow', flow.ref): True}}
        self.ns['_ssct_completion_repeat_states'](model)
        self.assertIs(flow.step, final)

    def test_side_effect_reset_is_not_invoked_or_selected(self):
        final = NS(ref='future_ready', pool=[])
        def reset():
            raise AssertionError('must never execute')
            return final
        start = NS(ref='future_reset', pool=[(reset, (), None, 0)])
        flow = NS(ref='future', step=start)
        self.native['flow'].append(flow)
        self.native['step'].extend((start, final))
        self.ns['_ssct_completion_repeat_states']({'listeners': {('flow', flow.ref): True}})
        self.assertIs(flow.step, start)

    def test_untracked_numbered_flow_is_not_a_repeat_program(self):
        final=NS(ref='future99_outro',pool=[])
        functions={'step':self.native['step']}
        exec('def reset(): return step.future99_outro',functions)
        start=NS(ref='future01_intro',pool=[(functions['reset'],(),None,0)])
        flow=NS(ref='future',step=start)
        self.native['flow'].append(flow)
        self.native['step'].extend((start,final))
        self.ns['_ssct_completion_repeat_states']({'listeners':{('flow','future'):True}})
        self.assertIs(flow.step,start)

    def test_future_device_repair_uses_native_destination(self):
        final = NS(ref='future_device_idle', pool=[])
        functions = {'step': self.native['step']}
        exec('def repair(): return step.future_device_idle', functions)
        repair = functions['repair']
        start = NS(ref='future_device_repair', pool=[(repair, (), None, 0)])
        device = NS(ref='future_device', step=start)
        self.native['prop'].append(device)
        self.native['step'].extend((start, final))
        model = {}
        self.ns['_ssct_completion_device_states'](model, self.native['step'])
        self.assertIs(device.step, final)

    def test_device_tag_receiver_comes_from_native_event_filter(self):
        class PC:
            ref='future_laptop'
            step=None
        device=PC()
        self.native['prop'].append(device)
        namespace={}
        exec("def callback(ctx, what=None): what.add('paired')",namespace)
        node=NS(ref='future01_connect',pool=[(namespace['callback'],(('what',device),),None,0)])
        route=NS(ref='future',step=node)
        self.native['flow'].append(route)
        self.native['step'].append(node)
        model=self.ns['_ssct_completion_model']([route],[node])
        self.assertTrue(model['device_tags'][('prop','future_laptop','paired')])

    def qualification(self,owned=True,conditional=False):
        anon=NS(ref='anon')
        reward=NS(ref='future_permit',where=anon if owned else None)
        device=NS(ref='future_gate')
        crowd=[device]
        self.ns['saga'].event=NS(crowd=crowd,detach=lambda item:crowd.remove(item))
        self.native['cast'].append(anon)
        self.native['prop'].extend((reward,device))
        retry=NS(ref='future_gate_retry',pool=[])
        namespace={'cast':self.native['cast'],'prop':self.native['prop'],
            'step':self.native['step'],'clear':self.clear,'unknown':lambda:False}
        body="def register():\n if not unknown(): return step.future_gate_retry\n prop.future_permit.move(cast.anon)\n"
        body+=(" if unknown(): return clear\n return None" if conditional else " return clear")
        exec(body,namespace)
        initial=NS(ref='future_gate_intro',pool=[(namespace['register'],(),None,0)])
        device.step=initial
        self.native['step'].extend((initial,retry))
        model={}
        self.ns['_ssct_completion_device_states'](model,self.native['step'])
        return device,model

    def test_acquired_qualification_clears_native_intro_without_callback(self):
        device,model=self.qualification()
        self.assertEqual(device.step.ref,'future_gate_intro')
        self.assertNotIn(device,self.ns['saga'].event.crowd)
        self.assertFalse(model['listeners'][('prop','future_gate')])
        self.assertEqual(model['acquired_terminals'],[('future_gate','future_gate_intro','register')])

    def test_unowned_reward_does_not_clear_qualification(self):
        device,model=self.qualification(owned=False)
        self.assertEqual(device.step.ref,'future_gate_retry')
        self.assertEqual(model['acquired_terminals'],[])

    def test_conditional_clear_after_reward_is_not_assumed(self):
        device,model=self.qualification(conditional=True)
        self.assertEqual(device.step.ref,'future_gate_retry')
        self.assertEqual(model['acquired_terminals'],[])

    def test_partial_auth_and_later_tag_remove_use_original_receiver(self):
        import functools
        class PC:
            ref='future_laptop'
            step=None
        device=PC()
        self.native['prop'].append(device)
        namespace={}
        exec("def auth(ctx): ctx.auto=True\ndef clear(ctx, what=None): what.remove('paired')",namespace)
        node=NS(ref='future01_connect',pool=[(functools.partial(namespace['auth'],device),(),None,0),
            (namespace['clear'],(('what',device),),None,0)])
        route=NS(ref='future',step=node)
        self.native['flow'].append(route)
        self.native['step'].append(node)
        model=self.ns['_ssct_completion_model']([route],[node])
        self.assertTrue(model['fields'][('prop','future_laptop','auto')])
        self.assertFalse(model['device_tags'][('prop','future_laptop','paired')])


if __name__ == '__main__': unittest.main()
