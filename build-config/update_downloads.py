"""只展示最新已发布固件的 sysupgrade 链接，不修改 Release 附件。"""
import argparse
import base64
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote

REPO = 'saltdion/immortalwrt-mt798x-rebase'
BRANCH = 'codex/build-ax6000'
START, END = '<!-- firmware-downloads:start -->', '<!-- firmware-downloads:end -->'


def api(endpoint, payload=None):
    args = ['gh', 'api', f'repos/{REPO}/{endpoint}']
    if payload is not None:
        args += ['--method', 'PUT', '--input', '-']
    return json.loads(subprocess.check_output(args, input=json.dumps(payload) if payload else None,
                                             text=True, encoding='utf-8'))


def render(releases):
    candidates = []
    for r in releases:
        if r.get('draft') or not r.get('published_at') or not r['tag_name'].startswith('ax6000-mtk-25.12-'):
            continue
        assets = [a for a in r.get('assets', []) if a.get('state') == 'uploaded' and
                  'xiaomi_redmi-router-ax6000-mtkuboot' in a['name'] and a['name'].endswith('squashfs-sysupgrade.bin')]
        if assets:
            candidates.append((r['published_at'], r['id'], r, assets))
    table = '| 发布时间（北京时间） | 固件 | 下载 |\n| --- | --- | --- |\n'
    if not candidates:
        return table + '| — | 暂无已发布的 sysupgrade 固件 | — |'
    _, _, r, assets = max(candidates, key=lambda x: x[:2])
    time = datetime.fromisoformat(r['published_at'].replace('Z', '+00:00')).astimezone(timezone(timedelta(hours=8)))
    links = [f'[sysupgrade](https://github.com/{REPO}/releases/download/{quote(r["tag_name"], safe="")}/{quote(a["name"], safe="")})' for a in sorted(assets, key=lambda a: a['name'])]
    return table + f'| {time:%Y-%m-%d %H:%M:%S} | AX6000 110M MTK compact 25.12 | {" · ".join(links)} |'


def replace(text, table):
    assert text.count(START) == text.count(END) == 1
    begin, end = text.index(START) + len(START), text.index(END)
    assert begin < end
    return text[:begin] + '\n\n' + table + '\n\n' + text[end:]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--publish', action='store_true')
    args = parser.parse_args()
    releases, page = [], 1
    while True:
        batch = api(f'releases?per_page=100&page={page}')
        releases.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    table = render(releases)
    if not args.publish:
        path = Path('README.md')
        path.write_bytes(replace(path.read_text(encoding='utf-8'), table).encode('utf-8'))
    else:
        # 每次读取最新 README，并使用 SHA 防止覆盖并发编辑。
        current = api(f'contents/README.md?ref={quote(BRANCH, safe="")}')
        old = base64.b64decode(current['content']).decode('utf-8')
        new = replace(old, table)
        if new != old:
            api('contents/README.md', dict(message='docs: refresh latest sysupgrade download',
                branch=BRANCH, sha=current['sha'], content=base64.b64encode(new.encode('utf-8')).decode('ascii')))
        print('最新 sysupgrade 下载列表已同步。')
