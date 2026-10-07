"""Run name inheritance in an isolated stage without changing baseline saves."""
import argparse
import hashlib
import json
import shutil
import subprocess
import time
from pathlib import Path


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
    probe = stage / 'game' / args.probe_name
    original = probe.read_bytes()
    savedir = stage / 'ssct-name-probe-saves'
    if savedir.exists():
        raise ValueError('Use a fresh probe save directory')
    baseline = list((stage / 'ssct-perfect-mod-tests').glob('quick-6-*.save'))
    if len(baseline) != 1:
        raise ValueError('One isolated quick-6 baseline required')
    baseline_hash = hashlib.sha256(baseline[0].read_bytes()).hexdigest()
    savedir.mkdir()
    shutil.copy2(baseline[0], savedir / baseline[0].name)
    report = stage / 'perfect_name_report.json'
    process = None
    started = time.time()
    try:
        for source in (repo / 'mods/perfect_save').glob('*.rpy'):
            shutil.copy2(source, stage / 'game/mods/perfect_save' / source.name)
        probe.write_bytes(Path(__file__).with_name('perfect_save_name.rpy').read_bytes())
        with (stage / 'name_probe_stderr.txt').open('wb') as stderr:
            process = subprocess.Popen([str(stage / 'lib/py3-windows-x86_64/python.exe'),
                str(stage / 'summertimesaga.py'), str(stage)], stderr=stderr,
                creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait(timeout=55)
        if process.returncode:
            raise RuntimeError(f'Native exit {process.returncode}')
        if (stage / 'name_probe_stderr.txt').stat().st_size:
            raise RuntimeError('Native stderr is nonempty')
        if hashlib.sha256(baseline[0].read_bytes()).hexdigest() != baseline_hash:
            raise RuntimeError('Baseline save changed')
        if not report.exists() or report.stat().st_mtime < started:
            raise RuntimeError('Missing fresh report')
        result = json.loads(report.read_text(encoding='utf8'))
        if not result.get('passed'):
            raise RuntimeError(result)
        result['source_sha256'] = hashlib.sha256((repo / 'mods/perfect_save/perfect_save.rpy').read_bytes()).hexdigest()
        result['baseline_sha256'] = baseline_hash
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
        print(json.dumps(result, ensure_ascii=False))
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        probe.write_bytes(original)


if __name__ == '__main__':
    main()
