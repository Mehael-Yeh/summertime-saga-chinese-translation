import functools
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace


class ChangelogPerformanceTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.preferences = SimpleNamespace(language='zh_hans')
        self.screen = SimpleNamespace(scope={'shown': 2})
        self.restarts = []
        def translate(source):
            self.calls.append(source)
            return source.replace('- Original.', '- 中文。').replace('Preview', '预览版')
        api = SimpleNamespace(translate_string=translate, get_screen=lambda name: self.screen,
            restart_interaction=lambda: self.restarts.append(True))
        namespace = {'renpy': api, '_preferences': self.preferences,
            '_ssct_logs_functools': functools, '_ssct_logs_re': re}
        source = Path('tl/zh_hans/changelog_translation8194.rpy').read_text(encoding='utf8')
        code = source.split('init -1 python:\n', 1)[1].split('\ninit 1:', 1)[0]
        exec(textwrap.dedent(code), namespace)
        self.functions = namespace
        self.content = '{=logs_menu_group}v1 - Preview 1{/=}\n\n- Original.\n\n\n{=logs_menu_group}v0{/=}\n\n- Unknown.'

    def test_sections_preserve_all_newlines_tags_and_unknown_entries(self):
        text = self.functions['_ssct_changelog_text'](self.content)
        parts = self.functions['_ssct_changelog_sections'](self.content)
        self.assertEqual('\n'.join(parts), text)
        self.assertEqual(len(parts), 2)
        self.assertIn('- 中文。', text)
        self.assertIn('- Unknown.', text)
        self.assertIn('预览版 1', text)

    def test_repeated_refresh_reuses_cached_sections_and_translations(self):
        parts = self.functions['_ssct_changelog_sections'](self.content)
        count = len(self.calls)
        for unused in range(10):
            self.assertIs(parts, self.functions['_ssct_changelog_sections'](self.content))
        self.assertEqual(len(self.calls), count)

    def test_language_switch_and_source_change_do_not_reuse_wrong_text(self):
        self.functions['_ssct_changelog_text'](self.content)
        self.preferences.language = None
        self.assertEqual(self.functions['_ssct_changelog_text'](self.content), self.content)
        self.preferences.language = 'zh_hans'
        self.assertIn('- New entry.', self.functions['_ssct_changelog_text'](self.content + '\n- New entry.'))

    def test_reveal_requires_reader_near_end_and_stops_at_last_section(self):
        reveal = self.functions['_ssct_changelog_reveal']
        scroll = SimpleNamespace(value=0, page=100, range=1000)
        reveal(scroll, 24)
        self.assertEqual(self.screen.scope['shown'], 2)
        scroll.value = 850
        reveal(scroll, 24)
        self.assertEqual(self.screen.scope['shown'], 3)
        self.assertEqual(len(self.restarts), 1)
        self.screen.scope['shown'] = 24
        reveal(scroll, 24)
        self.assertEqual(len(self.restarts), 1)

    def test_empty_and_headerless_texts_and_bounded_cache(self):
        sections = self.functions['_ssct_changelog_sections']
        self.assertEqual(sections(''), ())
        self.assertEqual(sections('- Original.'), ('- 中文。',))
        for number in range(20):
            sections(str(number))
        self.assertLessEqual(self.functions['_ssct_changelog_cached_sections'].cache_info().currsize, 8)


if __name__ == '__main__':
    unittest.main()
