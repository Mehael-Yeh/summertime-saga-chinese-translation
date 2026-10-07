"""Measure the changelog on an existing isolated official-game stage."""
import argparse
import ast
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', type=Path)
    parser.add_argument('probe_name')
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    stage = args.stage.resolve()
    stage.relative_to(repo / '.codex_tmp')
    if Path(args.probe_name).name != args.probe_name or not args.probe_name.endswith('.rpy'):
        raise ValueError('Existing probe filename required')
    probe = stage / 'game' / args.probe_name
    original = probe.read_bytes()
    archive = stage / 'game/zh_hans.rpa'
    if archive.exists():
        raise ValueError('Use a stage without a packed Chinese translation to avoid duplicate scripts')
    sys.path.insert(0, str(repo / 'tools'))
    from validate_translations import iter_pairs
    source = args.baseline or repo / 'tl/zh_hans/changelog_translation8194.rpy'
    pairs = {ast.literal_eval('"' + pair.source + '"'): ast.literal_eval('"' + pair.target + '"')
        for pair in iter_pairs(source.read_text(encoding='utf8').splitlines())}
    (stage / 'changelog_probe_pairs.json').write_text(json.dumps(pairs, ensure_ascii=False), encoding='utf8')
    for name in ('changelog_translation8194.rpy', 'base_box/style_box.rpy', 'src/menu/logs.rpy', 'src/menu/core.rpy'):
        target = stage / 'game/tl/zh_hans' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source if name == 'changelog_translation8194.rpy' else repo / 'tl/zh_hans' / name, target)
    shutil.copytree(repo / 'tl/zh_hans/fonts', stage / 'game/tl/zh_hans/fonts', dirs_exist_ok=True)
    report = stage / 'changelog_probe_report.json'
    started = time.time()
    process = None
    try:
        probe.write_bytes(Path(__file__).with_name('changelog_performance.rpy').read_bytes())
        with (stage / 'changelog_probe_stderr.txt').open('wb') as stderr:
            process = subprocess.Popen([str(stage / 'lib/py3-windows-x86_64/python.exe'),
                str(stage / 'summertimesaga.py'), str(stage)], stderr=stderr,
                creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait(timeout=55)
        if process.returncode or (stage / 'changelog_probe_stderr.txt').stat().st_size:
            raise RuntimeError('Native process failed; inspect stage stderr/traceback')
        if not report.exists() or report.stat().st_mtime < started:
            raise RuntimeError('Missing fresh report')
        result = json.loads(report.read_text(encoding='utf8'))
        if not result.get('passed'):
            raise RuntimeError(result)
        result['translation_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
        result['official_changelog_sha256'] = hashlib.sha256((stage / 'game/changelog.txt').read_bytes()).hexdigest()
        result['probe_sha256'] = hashlib.sha256(Path(__file__).with_name('changelog_performance.rpy').read_bytes()).hexdigest()
        result['installation_scope'] = 'Current changelog helper/screen, font configuration and menu labels; not a full translation-package or gameplay compatibility test'
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        shutil.copy2(report, stage / ('changelog_probe_before.json' if args.baseline else 'changelog_probe_after.json'))
        summary = {key: value for key, value in result.items() if key != 'metrics'}
        summary['coverage'] = [{key: value for key, value in row.items() if key != 'english_fallback_entries'} for row in result['coverage']]
        print(json.dumps(summary, ensure_ascii=False))
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        probe.write_bytes(original)


if __name__ == '__main__':
    main()
