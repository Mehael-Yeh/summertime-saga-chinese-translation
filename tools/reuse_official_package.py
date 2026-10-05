"""Reuse official game archives from a previous release of the exact game version."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

MODES = ('复制官方原包', '引用原包下载链接', '不复用')


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True, encoding='utf-8')


def select_source(releases, target_tag):
    match = re.fullmatch(r'(v?\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?)-[TPR]\d+', target_tag)
    if not match:
        raise ValueError('Target must be a numbered game-version release')
    version = match[1].removeprefix('v')
    tag_pattern = re.compile(r'v?' + re.escape(version) + r'-[TPR]\d+$')
    asset_pattern = re.compile(r'summertimesaga-' + re.escape(version) +
                               r'-[A-Za-z0-9_.-]+\.(?:zip|7z|apk|exe|dmg|tar\.gz|tar\.bz2|tar\.xz)$')
    candidates = sorted(releases, key=lambda r: (r.get('published_at') or '', r.get('id', 0)), reverse=True)
    for release in candidates:
        if release.get('draft') or release['tag_name'] == target_tag or not tag_pattern.fullmatch(release['tag_name']):
            continue
        assets = [a for a in release.get('assets', [])
                  if a.get('state') == 'uploaded' and asset_pattern.fullmatch(a['name'])]
        if assets:
            return dict(tag=release['tag_name'], assets=assets)
    return None


def verify(path, asset):
    if path.stat().st_size != asset['size']:
        raise ValueError('Archive size mismatch: ' + asset['name'])
    with path.open('rb') as stream:
        checksum = hashlib.file_digest(stream, 'sha256').hexdigest()
    expected = asset.get('digest')
    if expected and expected != 'sha256:' + checksum:
        raise ValueError('Archive SHA256 mismatch: ' + asset['name'])
    return 'sha256:' + checksum


def link_notes(body, source):
    start, end = '<!-- official-game-source:start -->', '<!-- official-game-source:end -->'
    block = start + '\n### 游戏官方原包\n\n'
    block += f"复用同版本发行版 `{source['tag']}` 的下载链接：\n\n"
    block += '\n'.join(f"- [{a['name']}]({a['browser_download_url']})" for a in source['assets'])
    block += '\n\n原包保存在上述发行版，请保留源发行版及附件。\n' + end
    if start in body:
        if end not in body:
            raise ValueError('Incomplete official-source note block')
        return body[:body.index(start)] + block + body[body.index(end) + len(end):]
    return body.rstrip() + '\n\n' + block + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--plan', default='official-package-plan.json')
    args = parser.parse_args()
    if args.prepare == args.apply:
        parser.error('Choose exactly one of --prepare / --apply')
    repo = os.environ['GITHUB_REPOSITORY']
    if args.prepare:
        mode = os.environ['REUSE_MODE']
        if mode not in MODES:
            raise ValueError('Unknown reuse mode')
        tag = os.environ['TARGET_TAG']
        pages = json.loads(gh('api', '--paginate', '--slurp', f'repos/{repo}/releases?per_page=100')) if mode != '不复用' else []
        source = select_source([r for page in pages for r in page], tag) if mode != '不复用' else None
        Path(args.plan).write_text(json.dumps(dict(repo=repo, target=tag, mode=mode, source=source), ensure_ascii=False), encoding='utf-8')
        print(f"Official package source: {source['tag'] if source else 'none'}; mode: {mode}")
        if not source and mode != '不复用':
            print('::notice::No previous official archive for this game version; upload it manually once.')
        return
    plan = json.loads(Path(args.plan).read_text(encoding='utf-8'))
    if plan['repo'] != repo:
        raise ValueError('Plan repository mismatch')
    source = plan['source']
    if not source or plan['mode'] == '不复用':
        return
    destination = json.loads(gh('release', 'view', plan['target'], '--repo', repo, '--json', 'body,assets'))
    with tempfile.TemporaryDirectory(prefix='official-game-') as temp:
        folder = Path(temp)
        if plan['mode'] == '引用原包下载链接':
            body = link_notes(destination['body'] or '', source)
            notes = folder / 'notes.md'
            notes.write_text(body, encoding='utf-8')
            gh('release', 'edit', plan['target'], '--repo', repo, '--notes-file', str(notes))
            return
        existing = {a['name']: a for a in destination['assets']}
        for asset in source['assets']:
            previous = existing.get(asset['name'])
            if previous:
                if previous.get('digest') and previous['digest'] == asset.get('digest') and previous['size'] == asset['size']:
                    print('Already present, matching digest: ' + asset['name'])
                    continue
                raise ValueError('Refusing to overwrite existing archive: ' + asset['name'])
            gh('release', 'download', source['tag'], '--repo', repo, '--pattern', asset['name'], '--dir', str(folder))
            archive = folder / asset['name']
            checksum = verify(archive, asset)
            print(f"Verified {asset['name']}: {checksum}")
            gh('release', 'upload', plan['target'], str(archive), '--repo', repo)
            uploaded = json.loads(gh('release', 'view', plan['target'], '--repo', repo, '--json', 'assets'))['assets']
            copied = next(a for a in uploaded if a['name'] == asset['name'])
            if copied['size'] != asset['size'] or (copied.get('digest') and copied['digest'] != checksum):
                raise ValueError('Uploaded archive verification failed')
            archive.unlink()


if __name__ == '__main__':
    main()
