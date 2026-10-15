# 验证记录 / Validation

2026-10-15 · KLayout 0.30.9 原生执行 / Native checks

- 四组固定库 1/1/9/1，12 个实例保存重开，47 个光学端口与 12 个 DevRec。 / Fixed libraries, native placement and save/reopen.
- 9 个独立 PCell：非空几何、PinRec、DevRec、参数编辑、GDS 保存重开和同名重载。 / Independent PCells, geometry, ports, editing and reload.
- 26 项中英并列菜单，重复注册、快捷键保留。 / Bilingual menu and shortcut retention.
- 波导互转及 GDS 恢复、水平/垂直器件连接、端口生成、Basic.Text 阵列、吸附、波导长度及长度差。 / Waveguide/layout regression checks.
- 结构 DRC 对确定违规版图连续两次检出 marker；无工艺线宽/间距阈值。 / Structural DRC detects known violations twice; no foundry thresholds.
- SiEPIC 识别 12 个固定器件的 47 个端口，旋转/镜像后方向、位置正确；SOI 与 TFLN 的公开及内部 PCell 可同进程并存。 / SiEPIC recognition, transformed ports and SOI/TFLN coexistence.
- 本地授权库导入保留旧版本、拒绝端口错位及越界索引。 / Local library import retains versions and rejects invalid ports and paths.

公开文件检查验证矩形固定黑盒、端口、识别框、署名、文件链接和来源隔离；公开 PCell 源码单独测试。安装器逻辑沿用已验证版本。
Public-file checks cover fixed rectangular blackboxes, interfaces, labels, links and source isolation; PCell source is checked separately. Installer logic is unchanged.
