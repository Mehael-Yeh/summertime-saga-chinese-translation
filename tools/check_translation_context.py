"""Check/fix context layout only; never certify translation or gameplay quality."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def block_kind(line: str) -> str:
    if re.match(r"^\s*[-*+]\s|^\s*\d+\.\s", line):
        return 'list'
    if line.lstrip().startswith('|'):
        return 'table'
    return ''


def markdown_layout(text: str) -> str:
    """Normalize block gaps, preserving content and fenced code verbatim."""
    out: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            out.append(line)
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            continue
        if match:
            if out and out[-1]:
                out.append('')
            out.append(line)
            fence = (match[1][0], len(match[1]))
            continue
        line = line.rstrip()
        if not line:
            if out and out[-1]:
                out.append('')
            continue
        if out and out[-1] == '':
            prev = out[-2] if len(out) > 1 else ''
            if block_kind(prev) and block_kind(prev) == block_kind(line):
                out.pop()
        elif out:
            prev = out[-1]
            if (line.startswith('#') or prev.startswith('#')
                    or re.match(r'^\s{0,3}(`{3,}|~{3,})\s*$', prev)
                    or block_kind(line) != block_kind(prev) and (block_kind(line) or block_kind(prev))):
                out.append('')
        out.append(line)
    # Do not discard trailing blank lines inside an unclosed code fence.
    while not fence and out and not out[-1]:
        out.pop()
    return '\n'.join(out) + '\n' if out else '\n'


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'invalid JSON constant: {value}')


def expected_bytes(path: Path, raw: bytes) -> bytes:
    text = raw.decode('utf-8-sig')
    if path.suffix == '.json':
        data = json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)
        formatted = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    else:
        formatted = markdown_layout(text)
        original = [line.rstrip() for line in text.splitlines() if line.strip()]
        result = [line.rstrip() for line in formatted.splitlines() if line.strip()]
        if original != result:
            raise ValueError('layout normalization changed nonblank content')
    return formatted.encode('utf-8')


def check_directory(directory: Path, fix: bool = False) -> int:
    paths = sorted(p for p in directory.iterdir() if p.is_file() and p.suffix in {'.md', '.json'})
    if not paths:
        print(f'ERROR: no context files in {directory}', file=sys.stderr)
        return 1
    # Validate every file before writing any file, including JSON duplicate keys.
    pending = []
    try:
        for path in paths:
            raw = path.read_bytes()
            expected = expected_bytes(path, raw)
            if raw != expected:
                pending.append((path, expected))
    except (UnicodeError, ValueError) as error:
        print(f'ERROR: {path}: {error}', file=sys.stderr)
        return 1
    for path, expected in pending:
        print(f'{"FIX" if fix else "FORMAT"}: {path.name}')
        if fix:
            path.write_bytes(expected)
    print(f'Context format: {len(paths)} files; {len(pending)} {"fixed" if fix else "mismatch(es)"}. Layout only.')
    return 0 if fix or not pending else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fix', action='store_true', help='Normalize layout; preserve content and JSON order.')
    parser.add_argument('--directory', type=Path, default=ROOT / 'translation_context')
    args = parser.parse_args()
    if not args.directory.is_dir():
        parser.error(f'not a directory: {args.directory}')
    return check_directory(args.directory, args.fix)


if __name__ == '__main__':
    raise SystemExit(main())
