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


def main():
    repo = os.environ['GITHUB_REPOSITORY']
    def pages(endpoint):
        result = subprocess.run(
            ['gh', 'api', '--paginate', '--slurp', f'repos/{repo}/{endpoint}?per_page=100'],
            check=True, capture_output=True, text=True)
        return [item for page in json.loads(result.stdout) for item in page]
    existing = {item['name'] for item in pages('tags')}
    existing.update(item['tag_name'] for item in pages('releases'))
    tag, title, prerelease = next_release(
        os.environ['GAME_VERSION'], os.environ['RELEASE_TYPE'], existing)
    with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
        output.write(f'tag={tag}\ntitle={title}\nprerelease={str(prerelease).lower()}\n')
    print(f'Next release: {tag} ({title})')


if __name__ == '__main__':
    main()
