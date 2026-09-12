#!/usr/bin/env python3
"""Read-only checks for Ren'Py Chinese translation files.

The checker never rewrites files. It validates source/translation string pairs and,
for tracked files changed from a Git ref, verifies that only translated string
payloads changed while program structure, line count, encoding markers, and line
endings stayed intact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable

STRING_RE = re.compile(r'"(?P<body>(?:\\.|[^"\\])*)"')
TRANSLATE_RE = re.compile(r'^translate\s+zh_hans(?:\s+|:)')
LABEL_RE = re.compile(r'^translate\s+zh_hans\s+([^:]+):')
OLD_RE = re.compile(r'^\s*old\s+"')
NEW_RE = re.compile(r'^\s*new\s+"')
SOURCE_COMMENT_RE = re.compile(r'^\s*#\s*(?!game/)(?:[^"\n]*?)"')
TRANSLATABLE_LINE_RE = re.compile(
    r'^(?P<prefix>\s*(?:(?:old|new|extend)\s+|[A-Za-z_][\w.]*\b[^\"\n]*?)?)'
    r'"(?P<body>(?:\\.|[^"\\])*)"(?P<suffix>.*)$'
)

SQUARE_RE = re.compile(r'\[[^\[\]\n]+\]')
# The inner [index] match alone misses a corrupted outer conversion, e.g. [when[1]!l].
NESTED_CONVERSION_RE = re.compile(r'\][!！][A-Za-z]+(?=\])')
CURLY_RE = re.compile(r'\{[^{}\n]+\}')
PRINTF_RE = re.compile(r'%\([^)]+\)[#0 +\-]?\d*(?:\.\d+)?[diouxXeEfFgGcrsa]|%(?!%)[#0 +\-]?\d*(?:\.\d+)?[diouxXeEfFgGcrsa]')

# Character names whose spelling must survive source-to-translation mapping.
# Deliberately excludes highly ambiguous everyday words such as May and Hope.
CHARACTER_NAMES = (
    'Anon', 'Erik', 'Jenny', 'Debbie', 'Diane', 'Tony', 'Maria', 'Tina',
    'Roxxy', 'Eve', 'Mia', 'Judith', 'Kevin', 'Annie', 'Bridget', 'Bissette',
    'Smith', 'Johnson', 'Harris', 'Helen', 'Tammy', 'Tori', 'Melody', 'Vivian',
    'Jane', 'June', 'Aqua', 'Daisy', 'Odette', 'Consuela', 'Josephine', 'Josie',
    'Lily', 'Becca', 'Missy', 'Ursula', 'Dimitri', 'Igor', 'Yumi', 'Barb',
    'Dexter', 'Cedric', 'Hana', 'Ivy', 'Kassy', 'Liu', 'Titomi', 'Yoshi', 'Zana',
)

# Confirmed Chinese name substitutions. These are reported only; never fixed.
FORBIDDEN_NAME_FORMS = {
    '匿名': 'Anon',
    '珍妮': 'Jenny',
    '詹妮': 'Jenny',
    '黛比': 'Debbie',
    '黛安': 'Diane',
    '洛克茜': 'Roxxy',
    '洛茜': 'Roxxy',
    '伊芙': 'Eve',
    '米娅': 'Mia',
    '朱迪丝': 'Judith',
    '朱迪思': 'Judith',
    '凯文': 'Kevin',
    '塔米': 'Tammy',
    '托尼': 'Tony',
    '史密斯': 'Smith',
    '比塞特': 'Bissette',
    '约翰逊': 'Johnson',
    '布里奇特': 'Bridget',
    '哈里斯': 'Harris',
}


@dataclass(frozen=True)
class Pair:
    source_line: int
    target_line: int
    source: str
    target: str


def decode(data: bytes, path: Path) -> tuple[str, bool]:
    bom = data.startswith(b'\xef\xbb\xbf')
    try:
        return data.decode('utf-8-sig'), bom
    except UnicodeDecodeError as exc:
        raise ValueError(f'{path}: not valid UTF-8: {exc}') from exc


def newline_style(data: bytes) -> str:
    crlf = data.count(b'\r\n')
    lf = data.count(b'\n')
    if crlf and crlf == lf:
        return 'CRLF'
    if not crlf and lf:
        return 'LF'
    if not lf:
        return 'none'
    return 'mixed'


def quoted_body(line: str) -> str | None:
    match = STRING_RE.search(line)
    return match.group('body') if match else None


def iter_pairs(lines: list[str]) -> Iterable[Pair]:
    for index, line in enumerate(lines):
        source = None
        if SOURCE_COMMENT_RE.match(line):
            source = quoted_body(line)
            cursor = index + 1
            while cursor < len(lines) and (
                not lines[cursor].strip() or lines[cursor].lstrip().startswith('#')
                or lines[cursor].strip() == 'nvl clear'
            ):
                cursor += 1
            if cursor < len(lines):
                target = quoted_body(lines[cursor])
                if source is not None and target is not None:
                    yield Pair(index + 1, cursor + 1, source, target)
        elif OLD_RE.match(line):
            source = quoted_body(line)
            cursor = index + 1
            while cursor < len(lines) and (
                not lines[cursor].strip() or lines[cursor].lstrip().startswith('#')
            ):
                cursor += 1
            if cursor < len(lines) and NEW_RE.match(lines[cursor]):
                target = quoted_body(lines[cursor])
                if source is not None and target is not None:
                    yield Pair(index + 1, cursor + 1, source, target)


def tokens(text: str) -> Counter[str]:
    """Return protected tokens while allowing visible dom/sub text to be localized.

    ``{dom=...}`` and ``{sub=...}`` are custom display tags: the key controls
    styling, while the value is player-visible text. Compare their tag type and
    count, not the localized value.
    """
    curly = []
    for token in CURLY_RE.findall(text):
        match = re.fullmatch(r'\{(dom|sub)=[^{}]+\}', token)
        curly.append(f'{{{match.group(1)}=*}}' if match else token)
    found = (SQUARE_RE.findall(text) + NESTED_CONVERSION_RE.findall(text)
             + curly + PRINTF_RE.findall(text))
    return Counter(found)


def names_in(text: str) -> set[str]:
    return {
        name for name in CHARACTER_NAMES
        if re.search(rf'(?<![A-Za-z]){re.escape(name)}(?![A-Za-z])', text)
    }


def normalize_structure(text: str) -> list[str]:
    result: list[str] = []
    in_translate = False
    for line in text.splitlines():
        if line and not line[0].isspace():
            in_translate = bool(TRANSLATE_RE.match(line))
        if in_translate and not line.lstrip().startswith('#'):
            match = TRANSLATABLE_LINE_RE.match(line)
            if match:
                line = f'{match.group("prefix")}"<TRANSLATION>"{match.group("suffix")}'
        result.append(line)
    return result


def git_blob(root: Path, ref: str, path: Path) -> bytes | None:
    rel = path.relative_to(root).as_posix()
    proc = subprocess.run(
        ['git', 'show', f'{ref}:{rel}'], cwd=root, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, check=False,
    )
    return proc.stdout if proc.returncode == 0 else None


def git_autocrlf(root: Path) -> bool:
    proc = subprocess.run(
        ['git', 'config', '--bool', 'core.autocrlf'], cwd=root, text=True,
        encoding='utf-8', stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        check=False,
    )
    return proc.returncode == 0 and proc.stdout.strip().lower() == 'true'


def git_changed(root: Path, ref: str) -> set[Path]:
    proc = subprocess.run(
        ['git', 'diff', '--name-only', ref, '--', '*.rpy'], cwd=root,
        text=True, encoding='utf-8', stdout=subprocess.PIPE, check=True,
    )
    return {(root / line.strip()).resolve() for line in proc.stdout.splitlines() if line.strip()}


def validate_file(root: Path, path: Path, ref: str, compare: bool) -> list[str]:
    issues: list[str] = []
    data = path.read_bytes()
    try:
        text, bom = decode(data, path)
    except ValueError as exc:
        return [str(exc)]
    lines = text.splitlines()

    for pair in iter_pairs(lines):
        source_tokens = tokens(pair.source)
        target_tokens = tokens(pair.target)
        if source_tokens != target_tokens:
            issues.append(
                f'{path}:{pair.target_line}: placeholder/tag mismatch; '
                f'source={dict(source_tokens)}, target={dict(target_tokens)}'
            )
        if pair.source and not pair.target:
            issues.append(f'{path}:{pair.target_line}: empty translation for non-empty source')
        missing_names = names_in(pair.source) - names_in(pair.target)
        # Some quest-hint strings use literal ``Anon`` as a stand-in for the
        # player. In Chinese UI text, second person keeps custom player names
        # from being replaced by the unexplained literal word "Anon".
        if (
            'Anon' in missing_names
            and re.search(r'\bvisit Anon\b', pair.source)
            and '你' in pair.target
        ):
            missing_names.remove('Anon')
        if missing_names:
            issues.append(
                f'{path}:{pair.target_line}: English character name missing or changed: '
                f'{", ".join(sorted(missing_names))}'
            )

    for line_no, line in enumerate(lines, 1):
        if line.lstrip().startswith('#'):
            continue
        if line.count('"') and quoted_body(line) is None:
            issues.append(f'{path}:{line_no}: unclosed or unsupported double-quoted string')
        if '「' in line or '」' in line:
            issues.append(
                f'{path}:{line_no}: corner quote found in active translation; use “...” instead'
            )
        for chinese, english in FORBIDDEN_NAME_FORMS.items():
            if chinese in line:
                issues.append(
                    f'{path}:{line_no}: Chinese character-name form {chinese!r}; expected {english}'
                )

    labels = LABEL_RE.findall(text)
    duplicates = [label for label, count in Counter(labels).items() if count > 1]
    if duplicates:
        issues.append(f'{path}: duplicate translation labels: {duplicates}')

    if compare:
        base_data = git_blob(root, ref, path)
        if base_data is not None:
            try:
                base_text, base_bom = decode(base_data, path)
            except ValueError as exc:
                issues.append(str(exc))
            else:
                if bom != base_bom:
                    issues.append(f'{path}: UTF-8 BOM state changed from {base_bom} to {bom}')
                base_newline = newline_style(base_data)
                current_newline = newline_style(data)
                autocrlf_checkout = (
                    git_autocrlf(root) and base_newline == 'LF' and current_newline == 'CRLF'
                )
                if base_newline != current_newline and not autocrlf_checkout:
                    issues.append(
                        f'{path}: newline style changed from {base_newline} to {current_newline}'
                    )
                base_lines = base_text.splitlines()
                if len(lines) != len(base_lines):
                    issues.append(
                        f'{path}: line count changed from {len(base_lines)} to {len(lines)}'
                    )
                base_labels = LABEL_RE.findall(base_text)
                if labels != base_labels:
                    issues.append(f'{path}: translation label sequence changed')
                if normalize_structure(text) != normalize_structure(base_text):
                    issues.append(f'{path}: non-translation structure changed relative to {ref}')
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    parser.add_argument('--scope', type=Path, default=Path('tl/zh_hans'))
    parser.add_argument('--base-ref', default='HEAD')
    parser.add_argument('--changed', action='store_true', help='check only tracked .rpy files changed from base ref')
    parser.add_argument('--no-compare', action='store_true', help='skip Git structural comparison')
    args = parser.parse_args()

    root = args.root.resolve()
    scope = (root / args.scope).resolve()
    paths = sorted(scope.rglob('*.rpy'))
    if args.changed:
        changed = git_changed(root, args.base_ref)
        paths = [path for path in paths if path.resolve() in changed]

    issues: list[str] = []
    for path in paths:
        issues.extend(validate_file(root, path, args.base_ref, not args.no_compare))

    if issues:
        print(f'FAILED: {len(issues)} issue(s) in {len(paths)} file(s)')
        for issue in issues:
            print(f'- {issue}')
        return 1
    print(f'OK: validated {len(paths)} Ren\'Py translation file(s)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
