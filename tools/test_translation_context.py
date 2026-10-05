"""Regression tests for context formatting safeguards."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from check_translation_context import check_directory, expected_bytes, markdown_layout


class ContextFormatTests(unittest.TestCase):
    def test_lists_tables_headings_and_idempotence(self):
        text = '# 标题\n正文\n\n\n- 甲\n\n- 乙\n\n| A |\n\n|---|\n\n| B |\n'
        expected = '# 标题\n\n正文\n\n- 甲\n- 乙\n\n| A |\n|---|\n| B |\n'
        self.assertEqual(markdown_layout(text), expected)
        self.assertEqual(markdown_layout(expected), expected)

    def test_code_fence_and_nested_indentation_preserved(self):
        code = '````python\n\n# 不作为标题\n- not a list  \n```\n\n\n````'
        text = '# 标题\n\n' + code + '\n\n- 甲\n  - 子项\n'
        self.assertEqual(markdown_layout(text), text)

    def test_bom_crlf_and_json_order(self):
        raw = b'\xef\xbb\xbf' + '{"z": [2,1], "a": "中文"}\r\n'.encode()
        result = expected_bytes(Path('test.json'), raw)
        self.assertNotIn(b'\r', result)
        self.assertFalse(result.startswith(b'\xef\xbb\xbf'))
        self.assertEqual(list(json.loads(result)), ['z', 'a'])
        self.assertEqual(json.loads(result)['z'], [2, 1])

    def test_invalid_duplicate_or_nonfinite_json_rejected(self):
        for raw in (b'{', b'{"x":1,"x":2}', b'{"x":NaN}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                expected_bytes(Path('test.json'), raw)

    def test_check_read_only_and_fix_atomic_preflight(self):
        with tempfile.TemporaryDirectory() as temp, contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            folder = Path(temp)
            doc = folder / 'a.md'
            raw = b'# Header\r\n\r\n\r\nText\r\n'
            doc.write_bytes(raw)
            self.assertEqual(check_directory(folder), 1)
            self.assertEqual(doc.read_bytes(), raw)
            bad = folder / 'b.json'
            bad.write_text('{')
            self.assertEqual(check_directory(folder, True), 1)
            self.assertEqual(doc.read_bytes(), raw)
            bad.write_text('{}\n')
            self.assertEqual(check_directory(folder, True), 0)
            self.assertEqual(check_directory(folder), 0)


if __name__ == '__main__':
    unittest.main()
