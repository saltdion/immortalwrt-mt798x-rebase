"""根据上次成功发布判定是否编译，失败后下一次定时运行会重试。"""
import json
import os
import subprocess
from pathlib import Path


def api(path):
    result = subprocess.run(['gh', 'api', path], capture_output=True, text=True)
    if result.returncode:
        if '(HTTP 404)' in result.stderr:
            return None
        raise RuntimeError(result.stderr)
    return json.loads(result.stdout)


if __name__ == '__main__':
    repo = os.environ['GITHUB_REPOSITORY']
    branch = api(f'repos/{repo}/branches/25.12')
    assert branch, '源码分支不存在'
    sha = branch['commit']['sha']
    config_sha = os.environ['GITHUB_SHA']
    tag = f'ax6000-mtk-25.12-{sha[:12]}-{config_sha[:12]}'
    release = api(f'repos/{repo}/releases/tags/{tag}')
    build = os.environ.get('FORCE_BUILD') == 'true' or not release or release['draft']
    with Path(os.environ['GITHUB_OUTPUT']).open('a') as output:
        output.write(f'sha={sha}\ntag={tag}\nbuild={str(build).lower()}\n')
    with Path(os.environ['GITHUB_STEP_SUMMARY']).open('a') as summary:
        summary.write(f'源码提交：`{sha}`\n\n发布标识：`{tag}`\n\n需要编译：{build}\n')
