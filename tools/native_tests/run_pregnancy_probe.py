"""Verify pregnancy multipliers in an existing isolated official-game copy."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
import pickle
import zlib


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', type=Path)
    parser.add_argument('probe_name')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    stage = args.stage.resolve()
    stage.relative_to(repo / '.codex_tmp')
    if Path(args.probe_name).name != args.probe_name or not args.probe_name.endswith('.rpy'):
        raise ValueError('Existing probe filename required')
    archive = stage / 'game/zh_hans.rpa'
    if archive.exists():
        # Trusted repository-built local archive: prevent a duplicate new Mod.
        with archive.open('rb') as stream:
            header = stream.readline().split()
            stream.seek(int(header[1], 16))
            entries = pickle.loads(zlib.decompress(stream.read()))
        if any('pregnancy_chance' in name for name in entries):
            raise ValueError('Stage archive already contains the pregnancy Mod')
    probe = stage / 'game' / args.probe_name
    original = probe.read_bytes()
    source = repo / 'mods/pregnancy_chance/pregnancy_chance.rpy'
    target = stage / 'game/mods/pregnancy_chance/pregnancy_chance.rpy'
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    report = stage / 'pregnancy_probe_report.json'
    started = time.time()
    process = None
    try:
        probe.write_bytes(Path(__file__).with_name('pregnancy_chance.rpy').read_bytes())
        with (stage / 'pregnancy_probe_stderr.txt').open('wb') as stderr:
            process = subprocess.Popen([str(stage / 'lib/py3-windows-x86_64/python.exe'),
                str(stage / 'summertimesaga.py'), str(stage)], stderr=stderr,
                creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait(timeout=30)
        if process.returncode or (stage / 'pregnancy_probe_stderr.txt').stat().st_size:
            raise RuntimeError('Native process failed; inspect stage stderr/traceback')
        if not report.exists() or report.stat().st_mtime < started:
            raise RuntimeError('Missing fresh report')
        result = json.loads(report.read_text(encoding='utf8'))
        if not result.get('passed'):
            raise RuntimeError(result)
        result['mod_sha256'] = hashlib.sha256(source.read_bytes()).hexdigest()
        result['probe_sha256'] = hashlib.sha256(Path(__file__).with_name('pregnancy_chance.rpy').read_bytes()).hexdigest()
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        print(json.dumps({'version': result['version'], 'passed': result['passed'],
            'roll_cases': len(result['rolls']), 'ui_phases': len(result['ui']),
            'mod_sha256': result['mod_sha256']}, ensure_ascii=True))
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        probe.write_bytes(original)


if __name__ == '__main__':
    main()
