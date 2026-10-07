"""Regression tests for split-dialogue audit coverage; no game execution."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from audit_sentence_consistency import check_approved
from validate_translations import iter_pairs, validate_file


class SupportScriptAuditTests(unittest.TestCase):
    def check(self, baseline, current):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / 'runtime.rpy'
            path.write_text(current, encoding='utf-8', newline='\n')
            with patch('validate_translations.git_blob', return_value=baseline.encode()), \
                    patch('validate_translations.git_autocrlf', return_value=False):
                return validate_file(root, path, 'HEAD', True)

    def test_helper_migration_preserves_valid_runtime_setup(self):
        old='translate zh_hans python:\n    def font():\n        return "font.ttf"\n    gui.text_font = font()\n'
        new='init python:\n    def font():\n        return "font.ttf"\n\ntranslate zh_hans python:\n    gui.text_font = font()\n'
        self.assertEqual(self.check(old,new), [])

    def test_language_switch_redefinition_is_rejected(self):
        text='translate zh_hans python:\n    def helper():\n        return 1\n'
        self.assertTrue(any('serialization identity' in issue for issue in self.check(text,text)))

    def test_invalid_runtime_python_is_rejected(self):
        old='translate zh_hans python:\n    gui.text_font = "font.ttf"\n'
        new='translate zh_hans python:\n    gui.text_font = (\n'
        self.assertTrue(any('syntax error' in issue for issue in self.check(old,new)))

    def test_removing_dialogue_cannot_reclassify_it_as_support(self):
        old='translate zh_hans first:\n    # anon "Hi"\n    anon "你好"\n'
        new='translate zh_hans python:\n    gui.text_font = "font.ttf"\n'
        self.assertTrue(any('translation label sequence' in issue for issue in self.check(old,new)))

    def test_old_new_table_structure_remains_protected(self):
        old='translate zh_hans strings:\n    old "Hi"\n    new "你好"\n'
        new=old+'    pass\n'
        self.assertTrue(any('non-translation structure' in issue for issue in self.check(old,new)))

    def test_mixed_runtime_and_dialogue_still_requires_immutable_structure(self):
        old='translate zh_hans python:\n    gui.text_font = "font.ttf"\n\ntranslate zh_hans first:\n    # anon "Hi"\n    anon "你好"\n'
        new=old.replace('translate zh_hans first:', 'translate zh_hans other:')
        self.assertTrue(any('translation label sequence' in issue for issue in self.check(old,new)))


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
