# 使用说明 / User Guide

JNU_MWP_TFLN_PDK V1.0 · 2026-10-15

<a id="installation"></a>
## 安装 / Installation

公开版使用 [安装宏](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/releases/download/installer-macro/Install_JNU_TFLN_PDK.lym)：拖入 KLayout → 运行安装宏 → 安装 / 更新 → 重启。Technology 为 `JNU_MWP_TFLN_PDK`，菜单为 `JNU_MWP_TFLN_PDK V1.0`。
Drag the installer into KLayout, run it, choose Install / Update, then restart. Existing local edits and separately authorized geometry are preserved.

<a id="devices"></a>
## 器件库 / Libraries

四个固定库分别包含 1、1、9、1 个器件；`JNULib_TFLN_pcell` 含 9 个可编辑 PCell。通过 Instance 选择 Library 和器件；固定器件也可用“插入 TFLN 器件 / Insert Device”。库说明不显示作者，固定 GDS 框内保留 `By Songliang Chen, 2026/10/13`。
Four fixed libraries contain 1/1/9/1 devices; `JNULib_TFLN_pcell` provides nine editable PCells. Use Instance to select a library. Author text remains inside fixed-device frames and is omitted from Library descriptions.

PCell 复制自 SOI 公开实现，不依赖 SOI 安装。保留默认尺寸和几何算法，TFLN 光学性能需另行验证。
PCell geometry/defaults are copied from the public SOI implementation and run independently. Select dimensions and verify optical behavior for TFLN.

<a id="layout"></a>
## 功能菜单 / Menu

中英文同时显示，覆盖 JNU PDK 的波导、版图、DRC、更新和授权库安装功能，另保留 TFLN 工艺总览与参数查询。以下共 26 项。
Chinese and English appear together. The menu includes JNU PDK waveguide, layout, DRC, update and authorized-library tools, plus TFLN overview and parameter tools (26 actions).

| 入口 / Action |
|---|
| 路径转波导 / Path to Waveguide |
| 波导转路径 / Waveguide to Path |
| 计算波导长度 / Calculate Waveguide Length |
| 计算波导长度差 / Calculate Waveguide Length Difference |
| 通过波导连接器件 / Cell Connect by Waveguide |
| 为单元生成端口 / Make Pins for Cell |
| 排除图层 / Layer Exclude |
| 数字文本阵列 / Numerical text array |
| 吸附器件 / Snap components |
| 编辑 TFLN 设计规则 / JNU_MWP_TFLN_DRC |
| 运行 TFLN 设计规则检查 / Run JNU_MWP_TFLN_DRC |
| 新建 TFLN 版图 / New Layout |
| 插入 TFLN 器件 / Insert Device… |
| 应用 TFLN 技术与图层 / Apply Technology & Layers |
| 器件参数与端口 / Device & Port Info |
| 300/125 nm 总览 / Overview |
| 400/200 nm 总览 / Overview |
| 600/300 nm 总览 / Overview |
| 600/600 nm 总览 / Overview |
| 打开器件 GDS 文件夹 / Open GDS Folder |
| 器件清单 / Device Index |
| 使用说明 / User Guide |
| 关于 / About |
| 重新加载 TFLN PDK / Reload TFLN PDK |
| 检查 PDK 更新 / Check for PDK Updates |
| 安装／更新白盒器件库 / Install / Update Whitebox Library |

路径转波导：先绘制 Manhattan Path，再选择并运行。复合波导支持直段、弯曲段与 taper 参数。波导转路径恢复中心线。通过波导连接器件对两个选中实例的相向端口创建直波导或 S 弯。吸附器件先选移动组，再将鼠标悬停在固定参考器件上。
For Path to Waveguide, select a Manhattan path; composite mode supports straight/bend widths and tapers. Waveguide to Path restores the centerline. Cell Connect joins facing ports of two selected instances. For Snap components, select the moving group and hover over the fixed component.

DRC 使用原生 Macro Development 编辑和运行当前单元。当前仅提供 PinRec 与波导接触、波导在 DevRec 内的结构检查；尚无 TFLN 制造最小线宽/间距阈值，不能作为工艺签核。
DRC uses the native macro editor and active-cell runner. Rules check PinRec contact and DevRec containment only; foundry width/spacing limits are not yet supplied.

“安装／更新白盒器件库”选择已获授权的本地 GDS 文件夹，按当前 Cell 名和端口匹配，复制到 KLayout 用户目录下独立私有目录。每次安装保留旧版本，不向 Git 仓库写入白盒。
Install / Update Whitebox Library accepts an authorized local GDS folder, validates current cell names and ports, and stores a new version in a separate private user directory.

<a id="ports"></a>
## 端口与识别 / Ports

固定库共 47 个光学端口；PinRec 在 1/10，方向短 Path 总长 20 nm，名称 opt1…；DevRec 在 68/0。PCell 自行生成相应端口和识别框。固定器件作者文字在框内。
Fixed devices provide 47 optical ports. PinRec 1/10 uses 20 nm directional paths and opt1… labels; DevRec is 68/0. PCells generate their own ports and frames.

<a id="layers"></a>
## 图层 / Layers

| Layer | Name | 定义 / Definition |
|---|---|---|
| 1/0 | Waveguide | 实际上表面宽度；红色 / Top-surface width; red |
| 3/0 | SiO2_Open | SiO₂ 湿法刻蚀开窗、缓坡 / Wet-etch opening |
| 4/0 | NiCr | 200 nm |
| 5/0 | Au | 1 µm |
| 7/0 | Dicing | 划片标记 / Dicing marks |
| 10/0 | Text | 作者与器件文字 / Author and device text |
| 1/10 | PinRec | 光学端口 / Optical ports |
| 68/0 | DevRec | 器件框 / Device recognition |
| 1/11 | PinRecM | 金属端口辅助定义 / Metal port definition |
| 81/0 | FbrTgt | 光纤目标辅助定义 / Fiber target definition |

DBU = 0.0001 µm。2/0 已删除；EC01–EC03 低台阶待处理。无设计的开窗、电极和划片层仅定义。
Layer 2/0 is removed. Lower steps of EC01–EC03 remain deferred. Layers without design geometry are definitions only.

<a id="index"></a>
## 文件索引 / Files

每个固定器件只有一个当前 [GDS 索引](DEVICE_INDEX.md)，包含完整参数；另有 4 个分组总览。EC01/EC02 的 MFD 仍为 `MFDUnknowum`。MMI07 不再注册。
The device index links one current GDS per fixed device and four overviews. EC01/EC02 retain `MFDUnknowum`; MMI07 is no longer registered.
