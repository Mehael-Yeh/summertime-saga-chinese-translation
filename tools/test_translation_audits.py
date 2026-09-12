"""Regression tests for split-dialogue audit coverage; no game execution."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from audit_sentence_consistency import check_approved
from validate_translations import iter_pairs


class DialogueAuditTests(unittest.TestCase):
    def test_nvl_clear_keeps_source_pair_and_line_numbers(self):
        pairs = list(iter_pairs([
            '    # tutor "Today..."',
            '    nvl clear',
            '',
            '    tutor "今天……"',
            '    # extend " and tomorrow."',
            '    extend "还有明天。"',
        ]))
        self.assertEqual([(p.source_line, p.target_line) for p in pairs], [(1, 4), (5, 6)])
        self.assertEqual(pairs[0].source, 'Today...')
        self.assertEqual(pairs[1].target, '还有明天。')

    def test_does_not_skip_control_flow(self):
        self.assertEqual(list(iter_pairs([
            '    # anon "Hello"',
            '    jump somewhere',
            '    anon "你好"',
        ])), [])

    def check_rule(self, **overrides):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'dialogue.rpy'
            file.write_text(
                'translate zh_hans first:\n'
                '    # anon "Oh."\n    anon "我。"\n'
                'translate zh_hans second:\n'
                '    # anon "Oh."\n    anon "哦。"\n', encoding='utf-8')
            rule = dict(file=str(file), source='Oh.', target='我。', **overrides)
            path = Path(folder) / 'rules.json'
            path.write_text(json.dumps(dict(patterns=[rule])), encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                return check_approved(path)

    def test_id_scopes_same_english_to_correct_context(self):
        self.assertFalse(self.check_rule(id='first'))

    def test_wrong_block_is_detected(self):
        self.assertTrue(self.check_rule(id='second'))

    def test_missing_block_is_detected(self):
        self.assertTrue(self.check_rule(id='missing'))

    def test_legacy_unscoped_rule_still_checks_all_occurrences(self):
        self.assertTrue(self.check_rule())


if __name__ == '__main__':
    unittest.main()
