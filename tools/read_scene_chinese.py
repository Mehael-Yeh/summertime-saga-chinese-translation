"""Show Chinese dialogue in source scene order; never grants review credit."""
from pathlib import Path
import argparse
import re

from validate_translations import iter_pairs, quoted_body

ROOT = Path(__file__).resolve().parents[1]
LOCATION = re.compile(r'^\s*# game/(.+):(\d+)\s*$')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('script', help='Path relative to game/, e.g. src/plot/ano02.rpy')
    parser.add_argument('--source-root', type=Path, default=ROOT / '.codex_tmp/current7944/src')
    parser.add_argument('--start', type=int, default=1)
    parser.add_argument('--end', type=int, default=100000)
    args = parser.parse_args()
    source = args.source_root / args.script
    translated = ROOT / 'tl/zh_hans' / args.script
    lines = translated.read_text(encoding='utf-8-sig').splitlines()
    by_location = {}
    for pair in iter_pairs(lines):
        if lines[pair.source_line - 1].lstrip().startswith('old '):
            continue
        location = next((LOCATION.match(s) for s in reversed(lines[:pair.source_line]) if LOCATION.match(s)), None)
        if location:
            by_location[(location[1], int(location[2]))] = pair
    # Ren'Py strings are global: repeated menu labels may belong to another file.
    shared = {}
    for path in sorted((ROOT / 'tl/zh_hans').rglob('*.rpy')):
        content = path.read_text(encoding='utf-8-sig').splitlines()
        for pair in iter_pairs(content):
            if content[pair.source_line - 1].lstrip().startswith('old '):
                shared.setdefault(pair.source, set()).add(pair.target)
    for n, line in enumerate(source.read_text(encoding='utf-8-sig').splitlines(), 1):
        if not args.start <= n <= args.end:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        pair = by_location.get((args.script.replace('\\', '/'), n))
        if pair and quoted_body(line) != pair.source:
            pair = None
        indent = line[:len(line) - len(line.lstrip())]
        if pair:
            speaker = stripped.split()[0] if not stripped.startswith(('"', "'")) else ('菜单' if stripped.endswith(':') else '叙述')
            print(f'S{n}/T{pair.target_line} {indent}{speaker}: {pair.target}')
        elif stripped.startswith('"'):
            body = quoted_body(line)
            values = shared.get(body, set())
            label = next(iter(values)) if len(values) == 1 else (body if body and re.fullmatch(r'\[[^\[\]]+\]', body) else '【共享译文未定位或有歧义，待回查】')
            match = re.search(r'"(?:\\.|[^"\\])*"(.*)$', stripped)
            suffix = match[1] if match else ''
            print(f'S{n} {indent}菜单: {label}{suffix}')
        elif stripped.startswith(('label ', 'menu', 'if ', 'elif ', 'else:', 'call ', 'jump ', 'return', 'scene ', 'nvl ', '$ ')):
            print(f'S{n} {line}')
        elif quoted_body(line) is not None:
            print(f'S{n} {indent}【原文此处有文本，译文未按位置匹配，待回查】')


if __name__ == '__main__':
    main()
