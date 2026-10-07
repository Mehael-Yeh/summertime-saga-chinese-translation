import tempfile
import unittest
from pathlib import Path
from native_tests.rpy_gate_catalogue import crawl_sources,native_statement_graph,python_facts


def node(kind,**fields):
    value=type(kind,(),{})()
    value.filename='game/src/plot/test.rpy';value.linenumber=1
    value.__dict__.update(fields)
    return value


class RpyCatalogueTests(unittest.TestCase):
    def test_native_storage_slots_are_read_without_properties(self):
        class Return:
            __slots__=('filename','linenumber','expression')
            @property
            def arbitrary(self):raise AssertionError('No computed reads')
        value=Return();value.filename='game/src/one.rpy';value.linenumber=8;value.expression='None'
        graph=native_statement_graph([[value]])
        self.assertEqual(graph['statements'][0]['line'],8)
        self.assertEqual(graph['statements'][0]['expression'],'None')

    def test_if_else_preserves_predecessors_and_unactivated_labels(self):
        first=node('Return',expression='saga.event.emit(choice="open")')
        second=node('Return',expression='None')
        unused=node('Label',name='unused',block=[node('If',entries=[('flag',[first]),('True',[second])])])
        graph=native_statement_graph([[unused]])
        returns=[row for row in graph['statements'] if row['node']=='Return']
        self.assertEqual(returns[1]['guards'],[{'expression':'flag','truth':False},{'expression':'True','truth':True}])
        self.assertIn('unused',graph['labels'])
        self.assertEqual(returns[0]['python']['calls'][0]['function'],'saga.event.emit')
        self.assertFalse(graph['all_gates_passed'])

    def test_menu_choice_and_dynamic_call_not_assumed_resolved(self):
        branch=node('Call',label='target',expression=True,arguments=None)
        graph=native_statement_graph([[node('Menu',items=[('Open','has_key',[branch]),('Caption','True',None)])]])
        call=next(row for row in graph['statements'] if row['node']=='Call')
        self.assertEqual(call['guards'][0]['menu_input'],'Open')
        self.assertTrue(graph['call_edges'][0]['dynamic'])
        self.assertEqual(graph['call_edges'][0]['target_rows'],[])

    def test_python_reads_writes_and_conditions_are_static(self):
        facts=python_facts('if saga.cast.anon.key:\n saga.cast.anon.ready=True\n forbidden()')
        self.assertIn('saga.cast.anon.ready',facts['writes'])
        self.assertIn('saga.cast.anon.key',facts['reads'])
        self.assertEqual(facts['conditions'][0]['expression'],'saga.cast.anon.key')
        self.assertEqual(facts['guarded_statements'][0]['guards'],[{'expression':'saga.cast.anon.key','truth':True}])
        self.assertTrue(python_facts('bad syntax >>>')['unresolved'])

    def test_field_dependencies_link_writes_to_conditions(self):
        code=type('Code',(),{'source':'saga.cast.anon.ready=True'})()
        graph=native_statement_graph([[node('Python',code=code),node('If',entries=[('saga.cast.anon.ready',[])])]])
        self.assertEqual(graph['field_dependencies']['saga.cast.anon.ready'],{'producers':['0'],'consumers':['1']})

    def test_direct_sources_have_fingerprints_and_failures_are_retained(self):
        with tempfile.TemporaryDirectory() as root:
            Path(root,'one.rpy').write_text('label unused:\n pass\n',encoding='utf8')
            def parse(filename,text):return None
            report=crawl_sources([root],parse)
            self.assertEqual(len(report['parse_errors']),1)
            self.assertFalse(report['files'][0]['parsed'])
            self.assertEqual(len(report['files'][0]['sha256']),64)
            self.assertFalse(report['all_gates_passed'])

    def test_script_modules_are_not_omitted(self):
        with tempfile.TemporaryDirectory() as root:
            Path(root,'one.rpym').write_text('label module_entry:\n pass\n',encoding='utf8')
            report=crawl_sources([root],lambda filename,text:[])
            self.assertEqual(len(report['files']),1)
            self.assertTrue(report['files'][0]['script_module'])

    def test_module_label_does_not_become_an_unqualified_global_target(self):
        module=node('Label',name='entry',block=[]);module.filename='res/art/shot.rpym'
        graph=native_statement_graph([[module,node('Call',label='entry',expression=False,arguments=None),
            node('Call',label='shot.entry',expression=False,arguments=None)]])
        self.assertNotIn('entry',graph['labels'])
        self.assertEqual(graph['call_edges'][0]['target_rows'],[])
        self.assertEqual(graph['call_edges'][1]['module_target_candidates'],['0'])
        self.assertTrue(graph['call_edges'][1]['module_binding_unverified'])

    def test_python_loop_is_not_unrolled_or_marked_executed(self):
        facts=python_facts('while unknown():\n change_state()')
        self.assertTrue(facts['guarded_statements'][0]['requires_native_control'])

    def test_source_screen_conditions_use_native_sl2_tree(self):
        block=type('SLBlock',(),{})();block.children=[]
        branch=type('SLIf',(),{})();branch.entries=[('saga.cast.anon.key',block)]
        screen=type('SLScreen',(),{})();screen.name='test';screen.children=[branch]
        graph=native_statement_graph([[node('Screen',screen=screen)]])
        conditions=graph['screen_syntax']['conditions']
        self.assertTrue(any(row.get('expression')=='saga.cast.anon.key' for row in conditions))


if __name__=='__main__':unittest.main()
