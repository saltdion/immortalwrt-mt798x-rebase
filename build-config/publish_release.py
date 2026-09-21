"""完成所有附件上传后才将草稿发布，作为下次构建判断依据。"""
import os
import subprocess
import sys
from pathlib import Path
from check_release import api

if __name__ == '__main__':
    repo, tag = os.environ['GITHUB_REPOSITORY'], os.environ['RELEASE_TAG']
    sha = os.environ['SOURCE_SHA']
    output = Path(sys.argv[1])
    notes = output / 'release-notes.md'
    notes.write_text(f'红米 AX6000 / hanwckf 110M / ImmortalWrt 25.12 厂商无线驱动精简版。\n\n源码：`{sha}`\n\n配置：`{os.environ["GITHUB_SHA"]}`\n\n编译成功不代表已经实机测试。仅适用于匹配的 110M MTK U-Boot 布局；从其他设备标识迁移时请先核对兼容性。\n\n不内置 OpenClash、PassWall 或 DAE 本体，保留相关依赖及厂商无线管理。\n')
    if not api(f'repos/{repo}/releases/tags/{tag}'):
        subprocess.run(['gh', 'release', 'create', tag, '--repo', repo, '--target', sha, '--draft', '--title', f'AX6000 110M MTK compact 25.12 {tag[-25:]}', '--notes-file', str(notes)], check=True)
    # 构建信息保留在 Artifact 中，Release 只上传固件、包清单及对应校验值。
    assets = [str(p) for p in output.iterdir() if p.is_file() and
              (p.suffix in ('.bin', '.manifest') or p.name == 'sha256sums')]
    subprocess.run(['gh', 'release', 'upload', tag, '--repo', repo, '--clobber', *assets], check=True)
    subprocess.run(['gh', 'release', 'edit', tag, '--repo', repo, '--draft=false', '--notes-file', str(notes)], check=True)
