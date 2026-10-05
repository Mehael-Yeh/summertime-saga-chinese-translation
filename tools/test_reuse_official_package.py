import hashlib
from pathlib import Path
import tempfile
import unittest
import json
import os
from unittest.mock import patch

import reuse_official_package as reuse
from reuse_official_package import cleanup_previous, link_notes, select_move_sources, select_source, verify


def release(tag, date, names, draft=False):
    return dict(tag_name=tag, published_at=date, draft=draft, assets=[dict(name=name, state='uploaded', browser_download_url='https://example.com/'+name) for name in names])


class ReuseTests(unittest.TestCase):
    def setUp(self):
        self.name = 'summertimesaga-21.0.0-wip.8194-pc.zip'
        self.old = release('v21.0.0-wip.8194-R2', '2026-10-05', [self.name, 'zh_hans.rpa'])

    def test_exact_version_and_exclude_destination(self):
        wrong = release('v21.0.0-wip.7944-R3', '2026-10-07', ['summertimesaga-21.0.0-wip.7944-pc.zip'])
        target = release('v21.0.0-wip.8194-R3', '2026-10-08', [self.name])
        source = select_source([wrong, target, self.old], target['tag_name'])
        self.assertEqual(source['tag'], self.old['tag_name'])
        self.assertEqual([a['name'] for a in source['assets']], [self.name])

    def test_newest_with_archive_across_release_types(self):
        new = release('v21.0.0-wip.8194-T5', '2026-10-06', [self.name])
        empty = release('v21.0.0-wip.8194-P7', '2026-10-07', ['zh_hans.rpa'])
        self.assertEqual(select_source([self.old, empty, new], 'v21.0.0-wip.8194-R4')['tag'], new['tag_name'])

    def test_draft_wrong_filename_and_path_ignored(self):
        draft = release('v21.0.0-wip.8194-R3', '2026-10-07', [self.name], True)
        unsafe = release('v21.0.0-wip.8194-R4', '2026-10-08', ['../'+self.name, 'summertimesaga-21.0.0-wip.81940-pc.zip'])
        self.assertIsNone(select_source([draft, unsafe], 'v21.0.0-wip.8194-R5'))

    def test_first_release_and_invalid_tag(self):
        self.assertIsNone(select_source([], 'v21.0.0-wip.8194-R1'))
        with self.assertRaises(ValueError):
            select_source([], 'invalid-tag')

    def test_multiple_platform_archives(self):
        self.old['assets'].append(dict(name='summertimesaga-21.0.0-wip.8194-android.apk', state='uploaded'))
        self.assertEqual(len(select_source([self.old], 'v21.0.0-wip.8194-P1')['assets']), 2)

    def test_size_and_digest_verification(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp)/'sample.zip'
            path.write_bytes(b'archive')
            checksum = 'sha256:'+hashlib.sha256(b'archive').hexdigest()
            asset = dict(name='sample.zip', size=7, digest=checksum)
            self.assertEqual(verify(path, asset), checksum)
            with self.assertRaises(ValueError):
                verify(path, dict(asset, size=8))
            with self.assertRaises(ValueError):
                verify(path, dict(asset, digest='sha256:bad'))

    def test_link_mode_preserves_notes_and_is_idempotent(self):
        source = select_source([self.old], 'v21.0.0-wip.8194-R3')
        notes = link_notes('Original release notes', source)
        self.assertTrue(notes.startswith('Original release notes'))
        self.assertIn(source['assets'][0]['browser_download_url'], notes)
        self.assertEqual(link_notes(notes, source), notes)

    def test_apply_download_verify_upload_and_collision(self):
        content = b'test archive'
        asset = dict(self.old['assets'][0], size=len(content), digest='sha256:'+hashlib.sha256(content).hexdigest())
        with tempfile.TemporaryDirectory() as temp:
            plan = Path(temp)/'plan.json'
            plan.write_text(json.dumps(dict(repo='owner/repo', target='v21.0.0-wip.8194-R3', mode='复制官方原包', source=dict(tag=self.old['tag_name'], assets=[asset]))), encoding='utf-8')
            uploaded = []
            calls = []

            def fake_gh(*args):
                calls.append(args)
                if args[:2] == ('release', 'view'):
                    return json.dumps(dict(body='', assets=uploaded))
                if args[:2] == ('release', 'download'):
                    (Path(args[args.index('--dir')+1])/asset['name']).write_bytes(content)
                elif args[:2] == ('release', 'upload'):
                    self.assertNotIn('--clobber', args)
                    self.assertEqual(Path(args[3]).read_bytes(), content)
                    uploaded.append(asset)
                return ''

            with patch.dict(os.environ, GITHUB_REPOSITORY='owner/repo'), patch('sys.argv', ['reuse', '--apply', '--plan', str(plan)]), patch.object(reuse, 'gh', fake_gh):
                reuse.main()
                reuse.main()  # Matching existing archive is skipped.
                self.assertEqual(sum(c[:2] == ('release', 'upload') for c in calls), 1)
                uploaded[0] = dict(asset, digest='sha256:different')
                with self.assertRaisesRegex(ValueError, 'overwrite'):
                    reuse.main()

    def test_move_includes_older_platform_archives(self):
        mac = 'summertimesaga-21.0.0-wip.8194-mac.zip'
        older = release('v21.0.0-wip.8194-R1', '2026-10-01', [self.name, mac])
        sources = select_move_sources([older, self.old], 'v21.0.0-wip.8194-R3')
        self.assertEqual([(s['tag'], [a['name'] for a in s['assets']]) for s in sources],
                         [('v21.0.0-wip.8194-R2', [self.name]), ('v21.0.0-wip.8194-R1', [mac])])

    def cleanup_fixture(self):
        asset = dict(name=self.name, size=12, digest='sha256:verified', state='uploaded', id=101)
        old = release('v21.0.0-wip.8194-R2', '2026-10-05', [])
        old['assets'] = [asset, dict(name='zh_hans.rpa', id=999, state='uploaded')]
        target = release('v21.0.0-wip.8194-R3', '2026-10-06', [])
        target['assets'] = [dict(asset, id=102)]
        other = release('v21.0.0-wip.7944-R3', '2026-10-07', ['summertimesaga-21.0.0-wip.7944-pc.zip'])
        return [old, target, other], {self.name: dict(size=12, digest='sha256:verified')}

    def test_cleanup_deletes_only_verified_same_version_archive(self):
        releases, verified = self.cleanup_fixture()
        calls = []
        def fake(*args):
            calls.append(args)
            return json.dumps([releases]) if '--slurp' in args else ''
        with patch.object(reuse, 'gh', fake):
            cleanup_previous('owner/repo', 'v21.0.0-wip.8194-R3', verified)
        self.assertEqual([c for c in calls if 'DELETE' in c],
                         [('api', '--method', 'DELETE', 'repos/owner/repo/releases/assets/101')])

    def test_cleanup_preflight_retains_everything_on_mismatch(self):
        for fault in ('old_digest', 'destination_digest', 'newer_release', 'newer_empty_release', 'missing_platform', 'missing_digest'):
            with self.subTest(fault=fault):
                releases, verified = self.cleanup_fixture()
                if fault == 'old_digest':
                    releases[0]['assets'][0]['digest'] = 'sha256:different'
                elif fault == 'destination_digest':
                    releases[1]['assets'][0]['digest'] = 'sha256:different'
                elif fault == 'newer_release':
                    releases[0]['published_at'] = '2026-10-08'
                elif fault == 'newer_empty_release':
                    releases.append(release('v21.0.0-wip.8194-R4', '2026-10-08', []))
                elif fault == 'missing_platform':
                    releases[0]['assets'].append(dict(name='summertimesaga-21.0.0-wip.8194-mac.zip', state='uploaded'))
                else:
                    releases[0]['assets'][0]['digest'] = None
                with patch.object(reuse, 'gh', return_value=json.dumps([releases])) as mocked:
                    with self.assertRaises(ValueError):
                        cleanup_previous('owner/repo', 'v21.0.0-wip.8194-R3', verified)
                    self.assertFalse(any('DELETE' in call.args for call in mocked.call_args_list))


if __name__ == '__main__':
    unittest.main()
