"""Reuse official game archives from a previous release of the exact game version."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

MOVE_MODE = '复制并仅保留最新原包'
MODES = (MOVE_MODE, '复制官方原包', '引用原包下载链接', '不复用')


def gh(*args):
    return subprocess.check_output(['gh', *args], text=True, encoding='utf-8')


def eligible_releases(releases, target_tag):
    match = re.fullmatch(r'(v?\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?)-[TPR]\d+', target_tag)
    if not match:
        raise ValueError('Target must be a numbered game-version release')
    version = match[1].removeprefix('v')
    tag_pattern = re.compile(r'v?' + re.escape(version) + r'-[TPR]\d+$')
    asset_pattern = re.compile(r'summertimesaga-' + re.escape(version) +
                               r'-[A-Za-z0-9_.-]+\.(?:zip|7z|apk|exe|dmg|tar\.gz|tar\.bz2|tar\.xz)$')
    candidates = sorted(releases, key=lambda r: (r.get('published_at') or '', r.get('id', 0)), reverse=True)
    result = []
    for release in candidates:
        if release.get('draft') or release['tag_name'] == target_tag or not tag_pattern.fullmatch(release['tag_name']):
            continue
        assets = [a for a in release.get('assets', [])
                  if a.get('state') == 'uploaded' and asset_pattern.fullmatch(a['name'])]
        if assets:
            result.append(dict(tag=release['tag_name'], assets=assets, published_at=release.get('published_at')))
    return result


def select_source(releases, target_tag):
    return next(iter(eligible_releases(releases, target_tag)), None)


def select_move_sources(releases, target_tag):
    # Keep the newest archive per platform/name, including platforms present
    # only in older releases. Every retained source is copied before cleanup.
    seen, sources = set(), []
    for source in eligible_releases(releases, target_tag):
        assets = [a for a in source['assets'] if a['name'] not in seen]
        seen.update(a['name'] for a in assets)
        if assets:
            sources.append(dict(source, assets=assets))
    return sources


def cleanup_previous(repo, target, verified):
    pages = json.loads(gh('api', '--paginate', '--slurp', f'repos/{repo}/releases?per_page=100'))
    releases = [r for page in pages for r in page]
    destination = next(r for r in releases if r['tag_name'] == target)
    if destination.get('draft') or not destination.get('published_at'):
        raise ValueError('Cleanup requires a published destination release')
    version = target.rsplit('-', 1)[0].removeprefix('v')
    tag_pattern = re.compile(r'v?' + re.escape(version) + r'-[TPR]\d+$')
    for release in releases:
        if (not release.get('draft') and tag_pattern.fullmatch(release['tag_name'])
                and (release.get('published_at') or '') > destination['published_at']):
            raise ValueError('A newer release exists; refusing cleanup')
    targets = []
    # Preflight every old asset before deleting anything. Unknown/different
    # archives remain intact, and a concurrently published newer release blocks cleanup.
    for source in eligible_releases(releases, target):
        for asset in source['assets']:
            reference = verified.get(asset['name'])
            if not reference or not asset.get('digest') or asset['digest'] != reference['digest'] or asset['size'] != reference['size']:
                raise ValueError('Old archive not verified against destination: ' + asset['name'])
            if not isinstance(asset.get('id'), int):
                raise ValueError('Missing asset API id')
            targets.append(asset)
    current = {a['name']: a for a in destination.get('assets', [])}
    for name, expected in verified.items():
        actual = current.get(name)
        if not actual or actual['size'] != expected['size'] or actual.get('digest') != expected['digest']:
            raise ValueError('Destination changed before cleanup: ' + name)
    for asset in targets:
        gh('api', '--method', 'DELETE', f"repos/{repo}/releases/assets/{asset['id']}")
        print('Deleted old official archive: ' + asset['name'])


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
        releases = [r for page in pages for r in page]
        source = select_source(releases, tag) if mode != '不复用' else None
        move_sources = select_move_sources(releases, tag) if mode == MOVE_MODE else []
        Path(args.plan).write_text(json.dumps(dict(repo=repo, target=tag, mode=mode, source=source, move_sources=move_sources), ensure_ascii=False), encoding='utf-8')
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
        verified = {}
        sources = plan.get('move_sources') or [source]
        transfers = [(s['tag'], a) for s in sources for a in s['assets']]
        for source_tag, asset in transfers:
            previous = existing.get(asset['name'])
            if previous:
                if previous.get('digest') and previous['digest'] == asset.get('digest') and previous['size'] == asset['size']:
                    print('Already present, matching digest: ' + asset['name'])
                    verified[asset['name']] = dict(size=asset['size'], digest=asset['digest'])
                    continue
                raise ValueError('Refusing to overwrite existing archive: ' + asset['name'])
            gh('release', 'download', source_tag, '--repo', repo, '--pattern', asset['name'], '--dir', str(folder))
            archive = folder / asset['name']
            checksum = verify(archive, asset)
            print(f"Verified {asset['name']}: {checksum}")
            gh('release', 'upload', plan['target'], str(archive), '--repo', repo)
            uploaded = json.loads(gh('release', 'view', plan['target'], '--repo', repo, '--json', 'assets'))['assets']
            copied = next(a for a in uploaded if a['name'] == asset['name'])
            if copied['size'] != asset['size'] or (copied.get('digest') and copied['digest'] != checksum):
                raise ValueError('Uploaded archive verification failed')
            if plan['mode'] == MOVE_MODE and copied.get('digest') != checksum:
                raise ValueError('Destination SHA256 unavailable; old archives retained')
            verified[asset['name']] = dict(size=asset['size'], digest=checksum)
            archive.unlink()
        if plan['mode'] == MOVE_MODE:
            cleanup_previous(repo, plan['target'], verified)


if __name__ == '__main__':
    main()
