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

    def test_menu_tags_follow_jumps_and_ignore_dynamic_arguments(self):
        menu=Menu([('Yes','True',[])])
        menu.item_arguments=[NS(arguments=[('_choice',"'observed'")]),
                             NS(arguments=[('_choice','unknown()')])]
        self.ns['renpy'].game.script.namemap['future_scene']=Label([menu,Jump('future_scene')])
        self.assertEqual(self.ns['_ssct_completion_script_choices']('future_scene'),frozenset(('observed',)))

    def test_repeat_history_does_not_require_intro_label_names(self):
        actor=NS(ref='future_person')
        self.native['cast'].append(actor)
        self.native['step'].append(NS(ref='future_person_level1'))
        branch=If([("saga.cast.future_person < 'visit.noon'",[Jump('future_visit.noon1')])])
        branch.next=Jump('future_visit.noon2')
        branch.filename='game/src/plot/future_visit.rpy'
        branch.linenumber=1
        self.ns['renpy'].game.script.namemap['branch']=branch
        model={'memo':{},'sources':[]}
        self.ns['_ssct_completion_greetings'](model)
        self.assertTrue(model['memo'][('cast','future_person','visit.noon')])

        # Similar numbering alone does not identify the repeated sibling.
        branch.next=Jump('another_visit.noon2')
        model={'memo':{},'sources':[]}
        self.ns['_ssct_completion_greetings'](model)
        self.assertEqual(model['memo'],{})

    def initial_interaction_model(self, source, *, once=False, presentation_state=False):
        from unittest.mock import patch
        import sys
        clear,abort=object(),object()
        def call(*args):self.fail('Projection must not execute dialogue')
        def req(*args):self.fail('Projection must not execute predicates')
        def transition(*args):self.fail('Projection must not execute presentation')
        actor=NS(ref='future_player')
        item=NS(ref='future_item',used=False)
        self.native['cast'].append(actor)
        self.native['prop'].append(item)
        functions={'call':call,'clear':clear,'abort':abort,
                   'unknown':lambda:self.fail('Unknown effect must not execute'),
                   '__name__':'saga.logic.once' if once else 'saga.logic.future_item'}
        exec(source,functions)
        node=NS(ref='future_item_intro',pool=[(functions['interact'],(('interact',item),),None,0)])
        self.ns['renpy'].game.script.namemap['first_scene']=Label(
            [Python('unknown_effect()')] if presentation_state else [Return(None)])
        model={'memo':{},'fields':{},'listeners':{},'sources':[]}
        with patch.dict(sys.modules,{'saga.event':NS(call=call,transition=transition),
                'saga.logic.util':NS(req=req),'saga.util.sentinel':NS(clear=clear,abort=abort)}):
            self.ns['_ssct_completion_initial_interactions'](model,[node])
        return model

    def test_native_one_off_retires_item_observer_without_callback_execution(self):
        model=self.initial_interaction_model("def interact():\n call('first_scene')\n return abort,clear",once=True)
        self.assertFalse(model['listeners'][('step','future_item_intro')])
        self.assertEqual(len(model['one_off_retirements']),1)

    def test_one_off_with_unknown_state_effect_is_not_retired(self):
        model=self.initial_interaction_model("def interact():\n call('first_scene')\n return abort,clear",once=True,presentation_state=True)
        self.assertEqual(model['listeners'],{})
        self.assertEqual(len(model['unresolved_one_offs']),1)

    def test_guarded_first_use_sets_marker_but_keeps_repeat_action(self):
        model=self.initial_interaction_model("def interact(interact):\n if not interact.used:\n  call('first_scene')\n  interact.used=True\n return abort")
        self.assertTrue(model['fields'][('prop','future_item','used')])
        self.assertEqual(model['listeners'],{})

    def test_guarded_unknown_effect_does_not_complete_first_use(self):
        model=self.initial_interaction_model("def interact(interact):\n if not interact.used:\n  call('first_scene')\n  unknown()\n  interact.used=True\n return abort")
        self.assertEqual(model['fields'],{})

    def test_missing_native_one_off_label_is_reported(self):
        model=self.initial_interaction_model("def interact():\n call('missing_scene')\n return abort,clear",once=True)
        self.assertFalse(model['listeners'][('step','future_item_intro')])
        self.assertEqual(model['one_off_retirements'][0]['missing_presentation_labels'],['missing_scene'])

    def test_unguarded_boolean_write_is_not_a_first_use_marker(self):
        model=self.initial_interaction_model("def interact(interact):\n call('first_scene')\n interact.used=True\n return abort")
        self.assertEqual(model['fields'],{})

    def prop_effect_model(self,source):
        class Item:
            ref='future_canvas'
            noop=False
            def add(self,flag):self.tags.add(flag)
            def remove(self,flag):self.tags.discard(flag)
        item=Item();item.noop=True;item.tags=set()
        self.native['prop'].append(item)
        namespace={'prop':self.native['prop']}
        exec(source,namespace)
        node=NS(ref='future01_end',pool=[(namespace['complete'],(),None,0)])
        route=NS(ref='future',step=node)
        self.native['flow'].append(route);self.native['step'].append(node)
        return item,self.ns['_ssct_completion_model']([route],[node])

    def test_native_prop_tag_and_attribute_delete_are_applied(self):
        item,model=self.prop_effect_model("def complete():\n prop.future_canvas.add('changed')\n del prop.future_canvas.noop")
        self.assertEqual(item.tags,set())
        self.assertTrue(item.noop)
        self.ns['_ssct_completion_apply'](model,[])
        self.assertEqual(item.tags,{'changed'})
        self.assertFalse(item.noop)
        self.assertNotIn('noop',item.__dict__)
        self.assertEqual(self.ns['_ssct_completion_validate'](model)['failures'],[])

    def test_later_native_write_supersedes_attribute_delete(self):
        item,model=self.prop_effect_model("def complete():\n del prop.future_canvas.noop\n prop.future_canvas.noop=True")
        self.assertNotIn(('prop','future_canvas','noop'),model['deleted_fields'])
        self.ns['_ssct_completion_apply'](model,[])
        self.assertTrue(item.noop)

    def test_later_native_delete_supersedes_attribute_write(self):
        item,model=self.prop_effect_model("def complete():\n prop.future_canvas.noop=True\n del prop.future_canvas.noop")
        self.assertNotIn(('prop','future_canvas','noop'),model['fields'])
        self.ns['_ssct_completion_apply'](model,[])
        self.assertFalse(item.noop)

    def test_later_prop_tag_remove_clears_added_tag(self):
        item,model=self.prop_effect_model("def complete():\n prop.future_canvas.add('changed')\n prop.future_canvas.remove('changed')")
        self.assertFalse(model['prop_tags'][('prop','future_canvas','changed')])
        self.ns['_ssct_completion_apply'](model,[])
        self.assertEqual(item.tags,set())

    def test_expanded_choice_intersection_projects_native_memory(self):
        actor=NS(ref='future_person')
        self.native['cast'].append(actor)
        menu=Menu([])
        menu.item_arguments=[NS(arguments=[('_choice',"'observed'")])]
        self.ns['renpy'].game.script.namemap['future_scene']=Label([menu])
        functions={'cast':self.native['cast'],'store':NS(_choice={'live_only'}),
                   'call':lambda *args: self.fail('Native callback must not run')}
        exec("def complete():\n call('future_scene')\n cast.future_person.put(*{'observed','unselected'}.intersection(store._choice))",functions)
        node=NS(ref='future01_end',pool=[(functions['complete'],(),None,0)])
        route=NS(ref='future',step=node)
        self.native['flow'].append(route)
        self.native['step'].append(node)
        model=self.ns['_ssct_completion_model']([route],[node])
        self.assertTrue(model['memo'][('cast','future_person','observed')])
        self.assertNotIn(('cast','future_person','unselected'),model['memo'])
        self.assertEqual(functions['store']._choice,{'live_only'})

        # Repeat handlers may store a one-tag intersection before expanding it.
        exec("def complete():\n call('future_scene')\n opts={'observed'}.intersection(store._choice)\n cast.future_person.put(*opts)",functions)
        node.pool=[(functions['complete'],(),None,0)]
        model=self.ns['_ssct_completion_model']([route],[node])
        self.assertTrue(model['memo'][('cast','future_person','observed')])

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


    def test_tv_subscription_persists_without_forcing_session_or_credentials(self):
        import sys
        from unittest.mock import patch
        class Television:
            ref='future_tv'
            hdd=set()
            ram=set()
        class PPV:
            def __init__(self,dev):
                self.dev=dev
                self.freq=NS(ref='future_subscription')
            @property
            def auto(self):return self.freq in self.dev.hdd
        # Native frequencies are hashable catalogue values.
        class Frequency:ref='future_subscription'
        tv=Television()
        account=PPV(tv)
        account.freq=Frequency()
        tv.tuner={123:NS(freq=account),1:NS(freq=Frequency())}
        other=NS(ref='ordinary_prop')
        self.native['prop'].extend((tv,other))
        model={}
        with patch.dict(sys.modules,{'saga.tech.television':NS(Television=Television,PPV=PPV)}):
            self.ns['_ssct_completion_tv_accounts'](model)
            self.ns['_ssct_completion_tv_accounts'](model)
        self.assertEqual(model['tv_accounts'],[(tv.ref,123,account.freq)])
        self.assertEqual(tv.hdd,{account.freq})
        self.assertEqual(tv.ram,set())
        self.assertTrue(account.auto)


if __name__ == '__main__': unittest.main()
