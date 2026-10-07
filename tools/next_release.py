"""Choose an unused numbered release tag from all repository tags and releases."""
import json
import os
import re
import subprocess


def next_release(version, release_type, existing):
    version = version.strip()
    if not re.fullmatch(r'v?\d+\.\d+\.\d+(?:-[A-Za-z0-9.]+)?', version):
        raise ValueError('请输入游戏版本号，例如 v21.0.0-wip.7944，不要附加 T/P/R 编号')
    if re.search(r'-[TPR]\d+$', version):
        raise ValueError('游戏版本号不要附加 T/P/R 编号')
    code = {'测试版': 'T', '预发行版': 'P', '发行版': 'R'}[release_type]
    pattern = re.compile(re.escape(version) + '-' + code + r'(\d+)$')
    numbers = [int(match[1]) for tag in existing if (match := pattern.fullmatch(tag))]
    suffix = code + str(max(numbers, default=0) + 1)
    return version + '-' + suffix, version + ' Chinese Translation ' + suffix, code != 'R'


def existing_release(version, release_type, tag, release):
    # Reuse the same version/type validation without allocating a new release.
    first_tag, _, prerelease = next_release(version, release_type, [])
    prefix = first_tag[:-1]
    if not re.fullmatch(re.escape(prefix) + r'[1-9]\d*', tag):
        raise ValueError('重发标签必须匹配游戏版本和发布类型，包含完整 T/P/R 编号')
    if release.get('tag_name') != tag or release.get('draft', True):
        raise ValueError('重发目标必须是已发布的 Release')
    if release.get('prerelease') != prerelease:
        raise ValueError('重发目标的预发行状态与发布类型不符')
    return tag, release.get('name') or tag, prerelease


def resolve_version(version, releases):
    if version.strip():
        return version.strip()
    published = [release for release in releases
                 if not release.get('draft', True) and release.get('published_at')]
    if not published:
        raise ValueError('没有已发布的 Release，请手动填写游戏版本号')
    latest = max(published, key=lambda release: release['published_at'])
    version = re.sub(r'-[TPR]\d+$', '', latest['tag_name'])
    # Validate the inferred game version before using it for a release target.
    next_release(version, '发行版', [])
    print(f'Using game version {version} from latest published Release {latest["tag_name"]}')
    return version


def main():
    repo = os.environ['GITHUB_REPOSITORY']
    def pages(endpoint):
        result = subprocess.run(
            ['gh', 'api', '--paginate', '--slurp', f'repos/{repo}/{endpoint}?per_page=100'],
            check=True, capture_output=True, text=True)
        return [item for page in json.loads(result.stdout) for item in page]
    target = os.environ.get('EXISTING_RELEASE', '')
    releases = pages('releases')
    version = resolve_version(os.environ.get('GAME_VERSION', ''), releases)
    if target:
        # Query only the requested existing target; do not create or move its tag.
        release = next((item for item in releases if item['tag_name'] == target), {})
        tag, title, prerelease = existing_release(
            version, os.environ['RELEASE_TYPE'], target, release)
    else:
        existing = {item['name'] for item in pages('tags')}
        existing.update(item['tag_name'] for item in releases)
        tag, title, prerelease = next_release(
            version, os.environ['RELEASE_TYPE'], existing)
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
        output.write(f'tag={tag}\ntitle={title}\nprerelease={str(prerelease).lower()}\n')
    print(f'Release target: {tag} ({title}); rebuilding={bool(target)}')


if __name__ == '__main__':
    main()
