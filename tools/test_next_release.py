import unittest

from next_release import next_release


class ReleaseNumberTests(unittest.TestCase):
    def test_independent_versions_and_types(self):
        existing = ['v21.0.0-wip.7944-T1', 'v21.0.0-wip.7944-P2',
                    'v21.0.0-wip.7944-R2', 'v21.0.0-wip.7922-T99']
        for kind, suffix, prerelease in [('测试版', 'T2', True),
                                          ('预发行版', 'P3', True),
                                          ('发行版', 'R3', False)]:
            self.assertEqual(next_release(' v21.0.0-wip.7944 ', kind, existing),
                             ('v21.0.0-wip.7944-' + suffix,
                              'v21.0.0-wip.7944 Chinese Translation ' + suffix,
                              prerelease))

    def test_highest_number_and_exact_match(self):
        tags = ['v21.0.0-wip.7944-T9', 'v21.0.0-wip.7944-T11',
                'v21.0.0-wip.7944-T3', 'v21.0.0-wip.7944-T100-other']
        self.assertEqual(next_release('v21.0.0-wip.7944', '测试版', tags)[0],
                         'v21.0.0-wip.7944-T12')

    def test_first_release(self):
        self.assertEqual(next_release('v21.0.0-wip.7944', '发行版', [])[0],
                         'v21.0.0-wip.7944-R1')

    def test_reject_invalid_version(self):
        for version in ['', 'v21.0.0-wip.7944-T2', 'bad\nversion', '$(command)']:
            with self.assertRaises(ValueError):
                next_release(version, '发行版', [])


if __name__ == '__main__':
    unittest.main()
