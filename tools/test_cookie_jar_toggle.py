"""Focused state tests for the optional Mod; not a translation inventory audit."""
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest


def load_functions(cookies=False):
    text = (Path(__file__).resolve().parents[1] / 'mods/cookie_jar_unlock/cookie_jar_unlock.rpy').read_text(encoding='utf-8')
    block = text.split('init 998 python:\n', 1)[1].split('\n# Attach after', 1)[0]
    calls = []
    persistent = SimpleNamespace(cookies=cookies, earned={'scene-one'})
    renpy = SimpleNamespace(save_persistent=lambda: calls.append('save'), restart_interaction=lambda: calls.append('refresh'), notify=lambda value: calls.append(value), translate_string=lambda value: value)
    namespace = dict(persistent=persistent, renpy=renpy, saga=SimpleNamespace(menu=SimpleNamespace(cast=lambda: None), lewd=SimpleNamespace(intf={'scene': True})), _=lambda value: value)
    exec(textwrap.dedent(block), namespace)
    return namespace, calls


class CookieToggleTests(unittest.TestCase):
    def test_enable_restore_and_repeat_preserve_earned_records(self):
        ns, calls = load_functions()
        for _ in range(2):
            self.assertFalse(ns['_ssct_cookie_jar_unlocked']())
            self.assertEqual(ns['_ssct_cookie_jar_button_label'](), 'Unlock all Cookie Jar entries')
            ns['_ssct_toggle_cookie_jar']()
            self.assertTrue(ns['persistent'].cookies)
            self.assertEqual(ns['_ssct_cookie_jar_button_label'](), 'Restore normal Cookie Jar unlocks')
            ns['_ssct_toggle_cookie_jar']()
            self.assertFalse(ns['persistent'].cookies)
        self.assertEqual(ns['persistent'].earned, {'scene-one'})
        self.assertEqual(calls.count('save'), 4)
        self.assertEqual(calls.count('refresh'), 4)

    def test_existing_unlock_or_setting_change_is_reflected(self):
        ns, _ = load_functions(True)
        self.assertTrue(ns['_ssct_cookie_jar_unlocked']())
        ns['_ssct_toggle_cookie_jar']()
        self.assertFalse(ns['persistent'].cookies)
        ns['persistent'].cookies = True
        self.assertTrue(ns['_ssct_cookie_jar_unlocked']())

    def test_incompatible_interface_does_not_save_or_change_state(self):
        for value in (None, 1, 'yes'):
            ns, calls = load_functions(value)
            ns['_ssct_toggle_cookie_jar']()
            self.assertIs(ns['persistent'].cookies, value)
            self.assertEqual(len(calls), 1)
        ns, calls = load_functions(False)
        del ns['saga'].lewd
        ns['_ssct_toggle_cookie_jar']()
        self.assertFalse(ns['persistent'].cookies)
        self.assertEqual(len(calls), 1)


if __name__ == '__main__':
    unittest.main()
