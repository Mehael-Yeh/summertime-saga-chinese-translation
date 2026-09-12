#!/usr/bin/env python3
"""Read-only audit of spaces between Chinese and English in target strings."""
from pathlib import Path
import re

from validate_translations import decode, iter_pairs

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'\{[^{}]*\}|\[[^\[\]]*\]|\\[A-Za-z]|[^{}\[\]\\]+|.', re.DOTALL)
CHINESE = r'\u3400-\u9fff\u3001-\u303f\uff01-\uff65\u2018-\u201d\u2026'
LATIN = r'A-Za-z\u00c0-\u024f'
GAP = re.compile(rf'(?<=[{CHINESE}])[ \t]+(?=[{LATIN}])|(?<=[{LATIN}])[ \t]+(?=[{CHINESE}])')


def normalize(text: str) -> str:
    """Use visible adjacency; preserve markup, interpolation and English phrases."""
    visible = []
    positions = []
    for match in TOKEN.finditer(text):
        token = match.group()
        if token.startswith('{'):
            # Formatting is invisible; spacing/layout tags create a boundary.
            if re.match(r'\{(?:/?(?:i|b|u|s|size|color|font|pen|outlinecolor|alpha|plain|rb|rt|art)|/?(?:a|cps))(?:[=}])', token):
                continue
            visible.append('\n')
            positions.append(None)
        elif token.startswith('['):
            # Names rendered by interpolation follow the same adjacency rule.
            visible.append('A')
            positions.append(None)
        elif token.startswith('\\'):
            visible.append('\n')
            positions.append(None)
        else:
            visible.extend(token)
            positions.extend(range(match.start(), match.end()))
    remove = {positions[i] for match in GAP.finditer(''.join(visible))
              for i in range(match.start(), match.end())}
    return ''.join(char for i, char in enumerate(text) if i not in remove)


def main() -> int:
    count = 0
    for path in sorted((ROOT / 'tl' / 'zh_hans').rglob('*.rpy')):
        text, _ = decode(path.read_bytes(), path)
        for pair in iter_pairs(text.splitlines()):
            if normalize(pair.target) != pair.target:
                print(f'{path.relative_to(ROOT)}:{pair.target_line}: mixed Chinese/English spacing')
                count += 1
    print(f'Mixed spacing: {count} mismatch(es)')
    return int(count != 0)


if __name__ == '__main__':
    raise SystemExit(main())
