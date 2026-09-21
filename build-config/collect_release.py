"""只收集本设备固件，避免将通用 BL2 文件当作刷机镜像发布。"""
import hashlib
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

if __name__ == '__main__':
    root, output = map(Path, sys.argv[1:])
    output.mkdir(exist_ok=True)
    images = root / 'bin/targets/mediatek/filogic'
    files = sorted(images.glob('*xiaomi_redmi-router-ax6000-mtkuboot*.bin'))
    assert any(p.name.endswith('factory.bin') for p in files), '未生成 factory 固件'
    assert any(p.name.endswith('sysupgrade.bin') for p in files), '未生成 sysupgrade 固件'
    manifests = sorted(images.glob('*xiaomi_redmi-router-ax6000-mtkuboot*.manifest'))
    assert manifests, '未生成软件包清单'
    for path in files + manifests:
        shutil.copy2(path, output / path.name)
    now = datetime.now(ZoneInfo('Asia/Shanghai')).isoformat()
    (output / 'build-info.txt').write_text(f'北京时间：{now}\n源码提交：{os.environ["SOURCE_SHA"]}\n配置提交：{os.environ["GITHUB_SHA"]}\n设备：xiaomi_redmi-router-ax6000-mtkuboot\n布局：UBI 起始 0x600000，容量 0x6e00000（110 MiB）\n')
    # 校验表只引用 Release 中实际上传的镜像与包清单。
    (output / 'sha256sums').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(output.iterdir()) if p.is_file() and p.suffix in ('.bin', '.manifest')))
