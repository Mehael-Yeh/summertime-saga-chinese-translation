"""Targeted completion regressions in an existing repository-local game copy."""
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
    parser.add_argument('case', choices=['sunday25', 'sunday26', 'chair', 'bed', 'maria', 'office', 'office-desk', 'office-cabinet', 'office-bin', 'office-canvas', 'tv-account'])
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    stage = args.stage.resolve()
    stage.relative_to(repo / '.codex_tmp')
    if Path(args.probe_name).name != args.probe_name or not args.probe_name.endswith('.rpy'):
        raise ValueError('An existing probe filename is required')
    probe = stage / 'game' / args.probe_name
    original = probe.read_bytes()
    options_path = None
    options_original = None
    if args.case.startswith('sunday'):
        tick = int(args.case[6:])
        source = 'perfect_save_sunday302.rpy'
        options_path = stage / 'sunday302_options.json'
        options = {'tick': tick}
        report = stage / f'sunday302_{tick}.json'
        expected = 'interaction_menu_reached' if tick in (25, 26) else 'native_schedule_closed'
    elif args.case in ('chair', 'bed'):
        source = 'perfect_save_initial_use.rpy'
        options_path = stage / 'initial_use_options.json'
        options = {'tick': 5, 'case': args.case}
        report = stage / f'initial_use_{args.case}_5.json'
        expected = 'first_use_interactions_passed'
    elif args.case=='tv-account':
        source='perfect_save_tv_account.rpy'
        report=stage / 'tv_account_regression.json'
        expected=None
    elif args.case.startswith('office'):
        source = 'perfect_save_office_canvas.rpy'
        options_path = stage / 'smith_options.json'
        targets={'office-desk':'school_desk','office-cabinet':'school_cabinet',
                 'office-bin':'school_bin','office-canvas':'school_canvas'}
        target=targets.get(args.case)
        options={'case':'perfect','target':target}
        report=stage / ('smith_perfect'+('_'+target if target else '')+'.json')
        expected=None
    else:
        source = 'perfect_save_maria_choices.rpy'
        report = stage / 'maria_regression.json'
        expected = None
    if options_path and options_path.exists():
        options_original = options_path.read_bytes()
    if report.exists():
        shutil.copy2(report, report.with_name(report.stem + f'.previous-{time.time_ns()}.json'))
    process = None
    started = time.time()
    try:
        for path in (repo / 'mods/perfect_save').glob('*.rpy'):
            shutil.copy2(path, stage / 'game/mods/perfect_save' / path.name)
        shutil.copy2(Path(__file__).with_name('native_script_continuation.py'), stage / 'native_script_continuation.py')
        probe.write_bytes(Path(__file__).with_name(source).read_bytes())
        if options_path:
            options_path.write_text(json.dumps(options), encoding='utf8')
        stderr = stage / f'completion_{args.case}_stderr.txt'
        with stderr.open('wb') as stream:
            process = subprocess.Popen([str(stage / 'lib/py3-windows-x86_64/python.exe'),
                str(stage / 'summertimesaga.py'), str(stage)], stderr=stream,
                creationflags=subprocess.CREATE_NO_WINDOW)
            process.wait(timeout=55)
        if process.returncode or stderr.stat().st_size:
            raise RuntimeError(f'Native process failed: {process.returncode}; see {stderr}')
        if not report.exists() or report.stat().st_mtime < started:
            raise RuntimeError('A fresh native report is required')
        result = json.loads(report.read_text(encoding='utf8'))
        if expected and result.get('status') != expected:
            raise RuntimeError(f'Unexpected native result: {result.get("status")}')
        if not expected and not result.get('passed'):
            raise RuntimeError('Native regression did not pass')
        current = hashlib.sha256((repo / 'mods/perfect_save/completion_state.rpy').read_bytes()).hexdigest()
        observed = result.get('mod_sha256', {}).get('completion_state.rpy', result.get('source_sha256'))
        if observed != current:
            raise RuntimeError('Native report does not match the current Mod')
        print(json.dumps({'case': args.case, 'status': result.get('status', 'passed'),
                          'report': str(report)}, ensure_ascii=False))
    finally:
        if process is not None and process.poll() is None:
            process.kill()
            process.wait()
        probe.write_bytes(original)
        if options_path:
            if options_original is None:
                options_path.unlink(missing_ok=True)
            else:
                options_path.write_bytes(options_original)


if __name__ == '__main__':
    main()
