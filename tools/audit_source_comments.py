#!/usr/bin/env python3
"""Read-only source-comment audit against decompiled Ren'Py dialogue.

Only unique, exact statement digests in the corresponding source file count as
evidence. Unmatched blocks are reported as unverified, never guessed or rewritten.
Run against a trusted, matching-version extraction, not arbitrary loose scripts.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path


def audit(source_root, scope):
    matched = unverified = 0
    differences = []
    for path in sorted(scope.glob('*.rpy')):
        source = source_root / 'src' / 'plot' / path.name
        if not source.exists():
            continue
        by_hash = {}
        for line in source.read_text(encoding='utf-8-sig').splitlines():
            code = line.strip()
            if '"' not in code or code.startswith('#'):
                continue
            digest = hashlib.md5((code + '\r\n').encode('utf-8')).hexdigest()[:8]
            by_hash.setdefault(digest, set()).add(code)
        block = digest = None
        for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
            found = re.match(r'translate zh_hans (\w+)_([a-f0-9]{8})(?:_\d+)?:', line)
            if found:
                block, digest = line, found[2]
            elif line and not line[0].isspace() and not line.startswith('#'):
                block = digest = None
            if not block or not line.lstrip().startswith('# ') or '"' not in line:
                continue
            candidates = by_hash.get(digest, set())
            if len(candidates) != 1:
                unverified += 1
                continue
            matched += 1
            expected = next(iter(candidates))
            if line.strip()[2:] != expected:
                differences.append(dict(file=path.as_posix(), line=number,
                                        block=block, expected=expected))
    return dict(matched=matched, unverified=unverified, differences=differences)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--scope', type=Path, default=Path('tl/zh_hans/src/plot'))
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not (args.source_root / 'src' / 'plot').is_dir():
        parser.error('source root must contain src/plot')
    report = audit(args.source_root, args.scope)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(f"Matched: {report['matched']}; unverified: {report['unverified']}; differences: {len(report['differences'])}")
    raise SystemExit(bool(report['differences']))
