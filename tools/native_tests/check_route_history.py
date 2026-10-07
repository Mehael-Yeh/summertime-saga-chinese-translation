"""Verify retained replay evidence; never certify gameplay completion."""
import argparse
import hashlib
import json
from pathlib import Path


def check_history(report_path):
    report_path = Path(report_path).resolve()
    report = json.loads(report_path.read_text(encoding='utf-8'))
    totals = dict.fromkeys(('events', 'labels', 'choices', 'transitions'), 0)
    for segment in report['history_segments']:
        path = (report_path.parent / segment['file']).resolve()
        if path.parent != report_path.parent:
            raise ValueError('History segment leaves the isolated report directory')
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != segment['sha256']:
            raise ValueError('History segment digest mismatch: ' + path.name)
        records = json.loads(raw)
        if set(records) != set(segment['ranges']):
            raise ValueError('History segment range keys mismatch')
        for key, rows in records.items():
            if key not in totals or not isinstance(rows, list):
                raise ValueError('Unsupported history record collection')
            if segment['ranges'][key] != [totals[key], totals[key] + len(rows)]:
                raise ValueError('Missing or duplicated history range: ' + key)
            totals[key] += len(rows)
    for key in totals:
        totals[key] += len(report[key])
    if totals != report['record_counts']:
        raise ValueError('Retained history counts do not match the report')
    return totals


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    args = parser.parse_args()
    print(json.dumps({'evidence_integrity': 'passed', 'record_counts': check_history(args.report),
                      'all_routes_certified_by_this_check': False}, indent=2))
