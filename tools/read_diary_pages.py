"""Read diary pages by event registration; never execute game bytecode."""
import argparse, dis, hashlib, json, marshal, re
from pathlib import Path
from validate_translations import iter_pairs

def collect(source, translation):
    code = marshal.loads(source.read_bytes()[16:])
    instructions = list(dis.get_instructions(code))
    pairs = {p.source: p for p in iter_pairs(translation.read_text(encoding='utf-8-sig').splitlines())}
    pages = []
    for i, op in enumerate(instructions):
        if op.opname != 'LOAD_NAME' or op.argval != 'add':
            continue
        args = instructions[i+1:i+3]
        if len(args) != 2 or any(a.opname != 'LOAD_CONST' for a in args):
            raise ValueError('Unexpected diary registration at offset ' + str(op.offset))
        event, lines = [a.argval for a in args]
        if not isinstance(event, str) or not isinstance(lines, tuple) or not all(isinstance(s, str) for s in lines):
            raise ValueError('Unexpected diary registration arguments')
        rows = []
        for n, text in enumerate(lines, 1):
            key = text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', r'\n')
            pair = pairs.get(key)
            visible = re.sub(r'\[[^\]]*\]|\{[^}]*\}', '', text)
            literal_only = not re.search(r'[A-Za-z]', visible)
            rows.append({'row': n, 'source': key, 'target': pair.target if pair else None,
                         'literal_only': literal_only,
                         'translation_line': pair.target_line if pair else None})
        pages.append({'event': event, 'event_page': 1 + sum(p['event'] == event for p in pages), 'rows': rows})
    if not pages:
        raise ValueError('No diary registrations found')
    return {'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'translation_sha256': hashlib.sha256(translation.read_bytes()).hexdigest(),
            'order': 'Events follow runtime book.index; pages and rows within each event follow registration order.',
            'pages': pages}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--translation', type=Path, default=Path('tl/zh_hans/extracted/jenny_diary.rpy'))
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.source, args.translation)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    missing = [(p['event'], p['event_page'], r['row']) for p in result['pages'] for r in p['rows'] if r['source'] and r['target'] is None and not r['literal_only']]
    print('Pages:', len(result['pages']), 'Events:', len({p['event'] for p in result['pages']}), 'Missing nonempty translations:', len(missing))
    print('Missing:', missing)
    print('Extraction does not grant human review credit.')

if __name__ == '__main__':
    main()
