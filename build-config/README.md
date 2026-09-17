# AX6000 110M 厂商驱动精简版自动构建

上游：`chasey-dev/immortalwrt-mt798x-rebase` 的 `25.12` 分支。

## 分支和定时任务

- `25.12` 为源码同步分支，不直接添加个人修改。
- `codex/build-ax6000` 为默认管理分支，保存工作流和精简配置。
- 每周五北京时间 **01:00** 检查上游（UTC 周四 17:00），同步成功后按需编译。
- 同一源码提交和管理配置提交已成功发布时跳过；失败或只有草稿时下次重试。
- Actions 页面可手动运行，`force` 可强制编译，`check_only` 只检查同步及发布状态。
- 仅跟踪主源码分支变化，不单独监控 feeds 更新；实际编译时拉取当时的 feeds 并记录版本。
- 同步不使用强制覆盖。发生冲突或权限错误时任务失败，需查看 Actions 日志处理。

## 固件配置

选择上游现成设备 `xiaomi_redmi-router-ax6000-mtkuboot`：NMBM，UBI 起始 `0x600000`、容量 `0x6e00000`（110 MiB），使用上游 factory/sysupgrade 镜像规则。

以每次同步后的 `defconfig/mt7986-ax6000.config` 为基础，保留厂商驱动配套选项，合并 `compact.config` 并改为单设备构建。

- 保留 mt_wifi、WARP、HNAT、MTK 无线配置和加速管理。
- 保留定时重启、ARP 绑定及 OpenClash/DAE 所需的部分依赖。
- 不内置 OpenClash、PassWall、SSR Plus+、DAE 应用或 Clash 内核。
- 保留上游默认登录地址和无线初始行为，不预置个人订阅或固定 Wi-Fi 密码。
- 构建后检查关键驱动、BPF 配置和 110M 分区定义；不满足要求时停止发布。

Release 只上传 AX6000 factory/sysupgrade 固件、包清单、构建配置、feeds 版本信息及 SHA256 校验文件。Artifact 保留 14 天，历史 Release 不自动清理。

## 验证边界

构建成功仅表示通过编译与静态检查，并不代表实机验证通过。初次迁移前应核对设备实际分区、U-Boot 版本和升级标识，不要忽略型号不匹配提示。厂商硬件加速与 DAE/透明代理的组合需在实际设备上验证。

GitHub 定时任务可能延迟；公开仓库长期无活动时可能停用定时工作流。
