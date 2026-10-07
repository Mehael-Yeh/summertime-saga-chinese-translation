"""Check archive content boundaries and compile guards for both release variants."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from build_rpa import build, read_index, verify


class PackageVariantsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'game'
        self.translation = {
            'tl/zh_hans/dialogue.rpy': b'translate zh_hans strings:\n',
            'tl/zh_hans/dialogue.rpyc': b'compiled translation fixture',
            'tl/zh_hans/fonts/font.ttf': b'font fixture',
            'tl/zh_hans/image.png': b'image fixture',
        }
        self.mods = {'mods/example/mod.rpy': b'init python:\n    pass\n',
                     'mods/example/mod.rpyc': b'compiled mod fixture'}
        for name, content in {**self.translation, **self.mods, 'mods/example/README.md': b'docs'}.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)

    def test_both_variants_preserve_identical_translation_bytes(self):
        for include_mods in (True, False):
            archive = Path(self.temp.name) / ('with.rpa' if include_mods else 'without.rpa')
            build(self.root, archive, include_mods=include_mods)
            verify(self.root, archive, include_mods=include_mods)
            key, index = read_index(archive)
            expected = set(self.translation) | (set(self.mods) if include_mods else set())
            self.assertEqual(set(index), expected)
            with archive.open('rb') as stream:
                for name, content in self.translation.items():
                    offset, length = (value ^ key for value in index[name][0])
                    stream.seek(offset)
                    self.assertEqual(stream.read(length), content)

    def test_no_mod_verification_rejects_archive_containing_mods(self):
        archive = Path(self.temp.name) / 'with.rpa'
        build(self.root, archive)
        with self.assertRaisesRegex(ValueError, 'Archive entries differ'):
            verify(self.root, archive, include_mods=False)

    def test_verification_rejects_modified_translation(self):
        archive = Path(self.temp.name) / 'without.rpa'
        build(self.root, archive, include_mods=False)
        (self.root / 'tl/zh_hans/dialogue.rpy').write_bytes(b'changed translation')
        with self.assertRaisesRegex(ValueError, 'Content mismatch'):
            verify(self.root, archive, include_mods=False)

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(Path(__file__).with_name('build_rpa.py')),
            '--root', str(self.root), '--output', str(Path(self.temp.name) / 'cli.rpa'), *args],
            capture_output=True, text=True)

    def test_compile_guard_only_requires_selected_package_scripts(self):
        (self.root / 'mods/example/mod.rpyc').unlink()
        self.assertEqual(self.run_cli('--exclude-mods', '--require-compiled').returncode, 0)
        result = self.run_cli('--require-compiled')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('mods/example/mod.rpy', result.stderr)

    def test_compile_guard_rejects_missing_translation_compilation(self):
        (self.root / 'tl/zh_hans/dialogue.rpyc').unlink()
        result = self.run_cli('--exclude-mods', '--require-compiled')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('tl/zh_hans/dialogue.rpy', result.stderr)

    def test_cli_verify_only_respects_variant_selection(self):
        self.assertEqual(self.run_cli('--exclude-mods', '--require-compiled').returncode, 0)
        self.assertEqual(self.run_cli('--exclude-mods', '--verify-only').returncode, 0)
        self.assertNotEqual(self.run_cli('--verify-only').returncode, 0)


if __name__ == '__main__':
    unittest.main()
