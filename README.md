# ImmortalWrt - MT798x

## 本 Fork：AX6000 110M 定时构建

### 固件下载列表

仅显示最近一次已成功发布且包含 sysupgrade 镜像的记录，时间为北京时间。编译发布后自动刷新。

<!-- firmware-downloads:start -->

| 发布时间（北京时间） | 固件 | 下载 |
| --- | --- | --- |
| 2026-09-17 15:28:53 | AX6000 110M MTK compact 25.12 | [sysupgrade](https://github.com/saltdion/immortalwrt-mt798x-rebase/releases/download/ax6000-mtk-25.12-dea037c4c6bb-4208e5be376a/immortalwrt-mediatek-filogic-xiaomi_redmi-router-ax6000-mtkuboot-squashfs-sysupgrade.bin) |

<!-- firmware-downloads:end -->

每周五北京时间 **01:00** 自动同步上游 `25.12`，有尚未成功发布的源码或构建配置时编译厂商无线驱动精简版，并发布 Release。

默认管理分支为 `codex/build-ax6000`；`25.12` 专门用于同步上游。支持手动强制编译及仅检查模式。完整说明见 [自动构建说明](build-config/README.md)。

```
This repository is worked on ImmortalWrt with MTK OpenWrt Feeds patches imported.
```

## Commit Cutoff Revisions

### ImmortalWrt: [1d34e7b](https://github.com/immortalwrt/immortalwrt/commit/1d34e7b88708d4eeb3feabe0b2b6f835a909c9c0)

```
mediatek: fix merge conflict

Fixes: #2458

Fixes: 3a0e732472ba ("Merge Official Source")
Signed-off-by: Tianling Shen <cnsztl@immortalwrt.org>
```

### MTK OpenWrt Feeds: [511100a](https://github.com/mediatek/mtk-openwrt-feeds/commit/511100a886cf99a12588ccbb810c70928a772027)

```
[openwrt-25.12][mt7988][npu][Enable NPU L4S in autobuild defconfig]

[Description]
Enable NPU package and L4S support in mt798x_rfb autobuild defconfig:
1. Add CONFIG_PACKAGE_kmod-npu=y
2. Add CONFIG_MTK_NPU_L4S=y
for both mt7992 and mt7996 25.12 profiles.

[Info to Customer]
N/A

Change-Id: I124b7f93a7c068ac87cd35343039470276baaf5e
```

### l1parser: [081bb31](https://github.com/chasey-dev/l1parser/commit/081bb31211efc74594d25bfd1bb5811f3408a205)

```
feat(ucode): add get all device map support
```
## About External Devices HNAT
> [!WARNING]
> Current HNAT support for external devices is basic and lack of complete test for various types. Please use with caution.

> [!IMPORTANT]
> Please keep interface `rxppd` in your bridge device (e.g. `br-lan`) while using external device HNAT.

### Support Matrix:
|               |  Ext as WAN   | Ext as LAN                |
|   :----:      |   :----:      | :----:                    |
|  **Ethernet** |      ✔️       |   ❌                     |
| **AP/ApCli**  |      ✔️       |   ⚠️(**Untested**)       |

## Acknowledgements
HNAT support for external devices is adapted from [Padavanonly's repo](https://github.com/padavanonly/immortalwrt-mt798x-6.6).
