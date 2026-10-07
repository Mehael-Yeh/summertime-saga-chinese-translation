import unittest

from next_release import existing_release, next_release


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

    def test_rebuild_existing_r4(self):
        tag = 'v21.0.0-wip.8194-R4'
        release = dict(tag_name=tag, name='R4 title', draft=False, prerelease=False)
        self.assertEqual(existing_release('v21.0.0-wip.8194', '发行版', tag, release),
                         (tag, 'R4 title', False))

    def test_rebuild_rejects_invalid_target(self):
        for tag in ['v21.0.0-wip.7944-R4', 'v21.0.0-wip.8194-P4',
                    'v21.0.0-wip.8194-R0', 'v21.0.0-wip.8194-R4-extra']:
            release = dict(tag_name=tag, draft=False, prerelease=False)
            with self.assertRaises(ValueError):
                existing_release('v21.0.0-wip.8194', '发行版', tag, release)

    def test_rebuild_requires_published_matching_release(self):
        tag = 'v21.0.0-wip.8194-R4'
        for release in [{}, dict(tag_name=tag, draft=True, prerelease=False),
                        dict(tag_name=tag, draft=False, prerelease=True)]:
            with self.assertRaises(ValueError):
                existing_release('v21.0.0-wip.8194', '发行版', tag, release)


if __name__ == '__main__':
    unittest.main()
