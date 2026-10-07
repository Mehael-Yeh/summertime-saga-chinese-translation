import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('route_history', Path(__file__).parent / 'native_tests/check_route_history.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RouteHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        rows = {'events': [{'requested': 'native action'}]}
        raw = json.dumps(rows).encode()
        (self.root / 'segment.json').write_bytes(raw)
        self.report = {'history_segments': [{'file': 'segment.json', 'sha256': hashlib.sha256(raw).hexdigest(),
                                              'ranges': {'events': [0, 1]}}],
                       'events': [{'returned': 'native action'}], 'labels': [], 'choices': [], 'transitions': [],
                       'record_counts': {'events': 2, 'labels': 0, 'choices': 0, 'transitions': 0}}

    def check(self):
        path = self.root / 'report.json'
        path.write_text(json.dumps(self.report), encoding='utf-8')
        return module.check_history(path)

    def test_retains_archived_and_live_records(self):
        self.assertEqual(self.check()['events'], 2)

    def test_changed_evidence_is_rejected(self):
        (self.root / 'segment.json').write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'digest mismatch'): self.check()

    def test_gap_or_duplicate_ranges_are_rejected(self):
        self.report['history_segments'][0]['ranges']['events'] = [1, 2]
        with self.assertRaisesRegex(ValueError, 'Missing or duplicated'): self.check()

    def test_dropped_live_records_are_rejected(self):
        self.report['events'] = []
        with self.assertRaisesRegex(ValueError, 'counts'): self.check()

    def test_segment_cannot_reference_an_unrelated_file(self):
        self.report['history_segments'][0]['file'] = '../outside.json'
        with self.assertRaisesRegex(ValueError, 'leaves'): self.check()


if __name__ == '__main__':
    unittest.main()
