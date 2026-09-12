"""Check recorded human review against current translations. Never grants review credit."""
import hashlib
import json
from pathlib import Path

from validate_translations import iter_pairs, LABEL_RE

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / 'translation_context/manual_review.json'


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory():
    return {
        p.relative_to(ROOT).as_posix(): {
            'sha256': fingerprint(p),
            'pairs': len(list(iter_pairs(p.read_text(encoding='utf-8-sig').splitlines()))),
        }
        for p in sorted((ROOT / 'tl/zh_hans').rglob('*.rpy'))
    }


def main():
    ledger = json.loads(LEDGER.read_text(encoding='utf-8'))
    current = inventory()
    completed = 0
    stale = []
    invalid = []
    for name, record in ledger['files'].items():
        if record.get('review'):
            if name not in current or current[name]['sha256'] != record['review']['translation_sha256']:
                stale.append(name)
            else:
                review = record['review']
                lines = (ROOT / name).read_text(encoding='utf-8-sig').splitlines()
                pairs = {p.target_line: p for p in iter_pairs(lines)}
                seen = set()
                problems = []
                for item in review['items']:
                    line = item['line']
                    pair = pairs.get(line)
                    if line in seen or pair is None:
                        problems.append(f'duplicate or missing item at {line}')
                    else:
                        labels = [LABEL_RE.match(s) for s in lines[:line] if LABEL_RE.match(s)]
                        ident = labels[-1].group(1) if labels else None
                        digest = hashlib.sha256((pair.source + '\0' + pair.target).encode('utf-8')).hexdigest()
                        if item['id'] != ident or item['pair_sha256'] != digest:
                            problems.append(f'item mismatch at {line}')
                    seen.add(line)
                source = ROOT / review.get('source_local', '.codex_tmp/current7944/src/' + review['source'].removeprefix('game/'))
                if not source.is_file() or fingerprint(source) != review['source_sha256']:
                    problems.append('source missing or changed')
                for dependency in review.get('dependencies', []):
                    path = ROOT / dependency['path']
                    if not path.is_file() or fingerprint(path) != dependency['sha256']:
                        problems.append('dependency missing or changed: ' + dependency['path'])
                if problems:
                    invalid.append((name, problems))
                else:
                    completed += len(review['items'])
    print(f'Inventory: {len(current)} files, {sum(r["pairs"] for r in current.values())} pairs')
    print(f'Current human-reviewed items: {completed}; stale files: {len(stale)}')
    print('Human review credit comes only from explicit records, not this audit.')
    for name in stale:
        print('STALE:', name)
    for name, problems in invalid:
        print('INVALID:', name, '; '.join(problems))
    missing = set(current) - set(ledger['files'])
    print(f'Files absent from ledger: {len(missing)}')
    return bool(stale or missing or invalid)


if __name__ == '__main__':
    raise SystemExit(main())
