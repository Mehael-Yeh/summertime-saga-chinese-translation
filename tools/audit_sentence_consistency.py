#!/usr/bin/env python3
"""Read-only repeated/similar source audit. Candidates are not translation errors."""
import argparse
from collections import defaultdict
from difflib import SequenceMatcher
import json
from pathlib import Path
import re
from validate_translations import iter_pairs


def normalize(text):
    return re.sub(r'[^\w\[\].]+', ' ', re.sub(r'\{[^{}]*\}', '', text).casefold()).strip()


def scan(root):
    groups = defaultdict(list)
    for path in sorted(root.rglob('*.rpy')):
        lines = path.read_text(encoding='utf-8-sig').splitlines()
        for pair in iter_pairs(lines):
            prefix = lines[pair.target_line-1].split('"', 1)[0].strip()
            speaker = prefix.split()[0] if prefix else 'narration'
            key = normalize(pair.source)
            if not key:
                continue
            groups[key].append(dict(file=path.as_posix(), line=pair.target_line,
                                    speaker=speaker, source=pair.source, target=pair.target))
    repeated = [dict(source=k, occurrences=v) for k,v in groups.items()
                if len(v)>1 and len({normalize(x['target']) for x in v})>1]
    repeated.sort(key=lambda g: (-len(g['occurrences']), g['source']))
    # An inverted index avoids quadratic comparisons across the complete corpus.
    eligible = {k for k in groups if len(k.split()) >= 5}
    index = defaultdict(set)
    for k in eligible:
        for word in set(k.split()):
            index[word].add(k)
    similar = []
    for key in sorted(eligible):
        words = set(key.split())
        rare = sorted(words, key=lambda w: (len(index[w]),w))[:2]
        candidates = set().union(*(index[w] for w in rare))
        for other in sorted(candidates):
            if other <= key or min(len(key),len(other))/max(len(key),len(other)) < .85:
                continue
            score = SequenceMatcher(None,key,other,autojunk=False).ratio()
            if score < .90:
                continue
            a,b = groups[key],groups[other]
            same_speaker = sorted({x['speaker'] for x in a}&{x['speaker'] for x in b})
            if same_speaker and {normalize(x['target']) for x in a} != {normalize(x['target']) for x in b}:
                similar.append(dict(score=round(score,4), speakers=same_speaker, left=a, right=b))
    return dict(repeated_candidates=repeated, similar_candidates=similar,
                note='Heuristic candidates only; punctuation, speaker, context and meaning require review.')


def check_approved(path):
    patterns=json.loads(path.read_text(encoding='utf-8'))['patterns']
    cache={}
    issues=[]
    for rule in patterns:
        file=rule['file']
        if file not in cache:
            lines=Path(file).read_text(encoding='utf-8-sig').splitlines()
            block=None
            blocks={}
            for number,line in enumerate(lines,1):
                match=re.match(r'^translate\s+zh_hans\s+([^:]+):',line)
                if match:
                    block=match.group(1)
                blocks[number]=block
            cache[file]=[(p,blocks[p.target_line]) for p in iter_pairs(lines)]
        matches=[p for p,block in cache[file] if p.source==rule['source']
                 and ('id' not in rule or rule['id']==block)]
        if not matches:
            issues.append(f'{file}: approved source missing')
        for pair in matches:
            if pair.target!=rule['target']:
                issues.append(f'{file}:{pair.target_line}: approved wording differs')
    for issue in issues:
        print(issue)
    print(f'Approved patterns: {len(patterns)}; {len(issues)} mismatch(es)')
    return bool(issues)


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope',type=Path,default=Path('tl/zh_hans'))
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check-approved',type=Path,help='Validate reviewed source/file wording without fuzzy scan')
    args=parser.parse_args()
    if args.check_approved:
        raise SystemExit(check_approved(args.check_approved))
    if args.output is None:
        parser.error('--output is required unless --check-approved is used')
    report=scan(args.scope)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"Repeated candidates: {len(report['repeated_candidates'])}; similar candidates: {len(report['similar_candidates'])}")
