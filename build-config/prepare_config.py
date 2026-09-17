"""保留上游厂商驱动选项，合并 compact 配置并收敛为 110M 单设备。"""
import re
import sys
from pathlib import Path

TARGET = 'CONFIG_TARGET_mediatek_filogic_DEVICE_xiaomi_redmi-router-ax6000-mtkuboot'


def parse(text):
    result = {}
    for line in text.splitlines():
        match = re.fullmatch(r'(CONFIG_\w[\w-]*)=(.*)', line)
        unset = re.fullmatch(r'# (CONFIG_\w[\w-]*) is not set', line)
        if match:
            result[match[1]] = match[2]
        elif unset:
            result[unset[1]] = 'n'
    return result


def verify(root):
    config = parse((root / '.config').read_text())
    for key in [TARGET, 'CONFIG_PACKAGE_kmod-mt_wifi', 'CONFIG_PACKAGE_kmod-warp',
                'CONFIG_PACKAGE_kmod-mediatek_hnat', 'CONFIG_PACKAGE_luci-app-mtwifi-cfg',
                'CONFIG_PACKAGE_luci-app-autoreboot', 'CONFIG_PACKAGE_luci-app-arpbind',
                'CONFIG_KERNEL_CGROUP_BPF', 'CONFIG_KERNEL_BPF_STREAM_PARSER',
                'CONFIG_KERNEL_BPF_EVENTS', 'CONFIG_KERNEL_DEBUG_INFO_BTF',
                'CONFIG_PACKAGE_kmod-sched-bpf', 'CONFIG_PACKAGE_kmod-xdp-sockets-diag']:
        assert config.get(key) == 'y', f'必要配置未生效：{key}'
    for key in ['CONFIG_TARGET_MULTI_PROFILE', 'CONFIG_PACKAGE_kmod-mt7915e',
                'CONFIG_PACKAGE_luci-app-openclash', 'CONFIG_PACKAGE_luci-app-passwall',
                'CONFIG_PACKAGE_luci-app-daed']:
        assert config.get(key, 'n') == 'n', f'意外启用：{key}'
    dts = (root / 'target/linux/mediatek/dts-ext/mt7986a-xiaomi-redmi-router-ax6000-mtkuboot.dts').read_text()
    assert re.search(r'reg\s*=\s*<0x600000\s+0x6e00000>', dts), '上游 110M 分区布局已改变，请人工核查'
    print('单设备、厂商无线驱动、110M 分区及精简配置检查通过')


def verify_kernel(root):
    # 顶层 CONFIG_KERNEL_* 与 Linux 的 CONFIG_* 不是一一对应；检查最终内核配置。
    paths = list((root / 'build_dir').glob('target-*/linux-mediatek_filogic/linux-*/.config'))
    assert len(paths) == 1, f'预期一个已生成的内核配置，实际找到 {len(paths)} 个'
    config = parse(paths[0].read_text())
    for key in ['CONFIG_BPF', 'CONFIG_BPF_SYSCALL', 'CONFIG_BPF_JIT',
                'CONFIG_CGROUP_BPF', 'CONFIG_BPF_STREAM_PARSER',
                'CONFIG_BPF_EVENTS', 'CONFIG_DEBUG_INFO_BTF', 'CONFIG_XDP_SOCKETS']:
        assert config.get(key) == 'y', f'实际内核缺少必要功能：{key}'
    for key in ['CONFIG_NET_CLS_BPF', 'CONFIG_NET_ACT_BPF', 'CONFIG_XDP_SOCKETS_DIAG']:
        assert config.get(key) in ('y', 'm'), f'实际内核缺少必要模块：{key}'
    print('实际 Linux 内核 BPF/BTF/XDP 配置检查通过')


if __name__ == '__main__':
    if sys.argv[1] == '--verify-kernel':
        verify_kernel(Path(sys.argv[2]))
    elif sys.argv[1] == '--verify':
        verify(Path(sys.argv[2]))
    else:
        root = Path(sys.argv[1])
        config = parse((root / 'defconfig/mt7986-ax6000.config').read_text())
        config.update(parse(Path(sys.argv[2]).read_text()))
        for key in list(config):
            if key.startswith('CONFIG_TARGET_DEVICE_') or (key.startswith('CONFIG_TARGET_') and '_DEVICE_' in key):
                del config[key]
        config.update({TARGET: 'y', 'CONFIG_TARGET_MULTI_PROFILE': 'n',
                       'CONFIG_TARGET_PER_DEVICE_ROOTFS': 'n',
                       'CONFIG_TARGET_mediatek': 'y', 'CONFIG_TARGET_mediatek_filogic': 'y'})
        (root / '.config').write_text(''.join(f'# {key} is not set\n' if value == 'n' else f'{key}={value}\n' for key, value in config.items()))
