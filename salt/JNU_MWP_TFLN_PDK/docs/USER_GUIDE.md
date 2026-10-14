# JNU_MWP_TFLN_PDK V1.0 使用说明 / User Guide

公开版包含固定黑盒和运行工具。波导层中的矩形表示占位包络；内部设计轮廓由独立授权提供。
The public edition contains fixed blackboxes and runtime tools. Rectangles on the waveguide layer represent placement envelopes; internal geometry requires separate authorization.

<a id="devices"></a>
## 工艺器件库 / Process libraries

在 KLayout **Instance → Library** 中选择 `JNULib_TFLN_300_125`、`JNULib_TFLN_400_200`、`JNULib_TFLN_600_300` 或 `JNULib_TFLN_600_600`。库名最后两项为膜厚及刻蚀深度（nm），器件数量依次为 1、1、10、1。

Select one of these four libraries in **Instance → Library**. The final two numbers specify film thickness and etch depth in nm. The libraries contain 1, 1, 10 and 1 devices respectively.

13 个固定器件含 4 个端面耦合器、7 个 MMI 和 PSR、PDMC。Cell 与文件名保留 `thickness`（薄膜厚度）、`etchDepth`（刻蚀深度）、`sidewallAngle`（侧壁角度）、晶向与传播方向；端面耦合器还有 MFD（模场直径）和包层。

The 13 devices comprise four edge couplers, seven MMIs, a PSR and a PDMC. Cell and file names encode thickness, etchDepth, sidewallAngle, crystal cut and propagation direction. Edge couplers also encode MFD and cladding.

`Xcut_Yprop` 表示 x 切 y 传；`Xcut_Zprop` 表示 x 切 z 传；`Unknow` 表示未确定。`MFD3.2um` 表示 3.2 µm 模场直径。工程角度与目录名义角度的差异保留在清单中。EC01–EC03 低台阶待处理。

`Xcut_Yprop` means X-cut with Y propagation, `Xcut_Zprop` means X-cut with Z propagation, and `Unknow` marks an unknown value. `MFD3.2um` means a 3.2 µm mode field diameter. Source versus nominal angle discrepancies are retained in the manifest. Lower steps of EC01–EC03 remain pending.

<a id="ports"></a>
## 端口与识别 / Ports and recognition

全部器件共 55 个光学端口。`1/10 PinRec` 使用总长 20 nm 的有向短 Path 和 `opt1`、`opt2` 等文字，宽度为器件接口宽度；`68/0 DevRec` 是单一矩形，左右边与端口端面齐平。

All devices provide 55 optical ports. `1/10 PinRec` uses directed 20 nm paths and optN labels with the device interface width. `68/0 DevRec` is one rectangle whose left and right edges align with the port facets.

端口坐标、宽度、方向与本地代表器件一致，可进行实例旋转、镜像及 SiEPIC 识别。多细指端面耦合器的光纤接口保留为单一逻辑端口，端口宽度表示整体端面包络。

Port coordinates, widths and directions match the local representative devices. Instances support rotation, mirroring and SiEPIC recognition. A multi-rail edge-coupler facet remains one logical optical port with an envelope width.

作者文字位于器件框内下方的留白区，最大字高 3 µm，短器件自动缩小。`1/11 PinRecM` 与 `81/0 FbrTgt` 仅建立定义，本批没有对应图形。

Author text sits in the lower blank area inside each recognition frame, with a maximum text size of 3 µm and smaller sizes for short devices. `1/11 PinRecM` and `81/0 FbrTgt` are defined but contain no geometry in this release.

<a id="layout"></a>
## 版图与放置 / Layout and placement

从 **JNU_MWP_TFLN_PDK V1.0 → 版图 / Layout** 执行：

| 菜单 / Action | 用途 / Behavior |
|---|---|
| 新建 TFLN 版图 / New Layout | 新建使用本 Technology 的版图，DBU 为 0.0001 µm / Create a layout using this Technology |
| 插入 TFLN 器件 / Insert Device | 选择黑盒与 X/Y 坐标，插入真实 Library 实例，可撤销 / Place a library instance at X/Y with undo |
| 应用 TFLN 技术与图层 / Apply Technology & Layers | 将当前视图绑定本技术及图层颜色 / Apply the Technology and layer styles |
| 器件参数与端口 / Device & Port Info | 选择器件实例，查询文件名、端口坐标、宽度及方向 / Inspect selected device and port information |

<a id="layers"></a>
## 图层定义 / Layer definitions

| Layer/Datatype | 名称 / Name | 定义 / Definition |
|---|---|---|
| 1/0 | Waveguide | 公开版为矩形占位；白盒采用上表面宽度 / Public rectangle placeholder; whitebox uses top width |
| 3/0 | SiO2_Open | SiO₂ 湿法刻蚀开窗，边缘缓坡 / SiO₂ wet-etch opening with a sloped edge |
| 4/0 | NiCr | 200 nm NiCr 电极 / electrode |
| 5/0 | Au | 1 µm Au 电极 / electrode |
| 7/0 | Dicing | 划片标记 / dicing marks |
| 10/0 | Text | 作者与器件文字 / author and device labels |
| 1/10 | PinRec | 光学端口 / optical ports |
| 68/0 | DevRec | 器件识别框 / device recognition frame |
| 1/11 | PinRecM | 仅定义金属端口辅助层 / metal-port auxiliary definition |
| 81/0 | FbrTgt | 仅定义光纤目标辅助层 / fiber-target auxiliary definition |

`2/0 Waveguide_Step` 已删除。Waveguide 使用红色 `#ff80a8`；无设计图形的开窗、电极与划片层只保留定义。
`2/0 Waveguide_Step` is removed. Waveguide uses `#ff80a8`; openings, electrodes and dicing layers remain definitions when no design geometry is available.

<a id="index"></a>
## 文件与总览 / Files and overviews

**器件库 / Libraries** 子菜单提供四组工艺总览及黑盒 GDS 文件夹。**说明 / Help** 提供器件索引、使用说明和版本署名。公开的 [器件索引](DEVICE_INDEX.md) 只链接黑盒文件；完整原始工程记录留在实验室本地。

The **Libraries** submenu opens four process overviews and the blackbox GDS folder. **Help** opens the device index, guide and version information. The public [device index](DEVICE_INDEX.md) links only to blackbox files; original project records remain local.

<a id="installation"></a>
## 安装与维护 / Installation and maintenance

下载 [Install_JNU_TFLN_PDK.lym](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/releases/download/installer-macro/Install_JNU_TFLN_PDK.lym)，拖入正在使用的 KLayout，在 Macro Development 选择 **Install JNU TFLN PDK**，点击绿色 Run，再点击“安装 / 更新”。完成后重启。

Download [Install_JNU_TFLN_PDK.lym](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/releases/download/installer-macro/Install_JNU_TFLN_PDK.lym), drag it into KLayout, select **Install JNU TFLN PDK** in Macro Development, click Run, then Install / Update. Restart when complete.

安装宏自动读取当前 KLayout 配置目录，Git 任务在后台运行。重复运行可安全更新干净 main；遇到本地修改、开发分支、未发布提交、错误 origin 或旧版手动安装时停止并保留原文件。手动克隆用户仍可使用根目录 `Install_Cloned_PDK.ps1`。
The macro reads the current KLayout user directory and runs Git in a background thread. Re-running safely updates a clean main; local edits, development branches, unpublished commits, wrong remotes and legacy installations are preserved. Manual Git-clone users can still use the root `Install_Cloned_PDK.ps1`.

干净的 Git 克隆可使用 `git pull --ff-only origin main` 更新。Technology、启动宏或安装路径有变更时重启 KLayout；仅 Python 运行文件变更时可尝试 **重新加载 TFLN PDK / Reload TFLN PDK**。

Update a clean Git clone with `git pull --ff-only origin main`. Restart KLayout after Technology, startup-macro or installation-path changes. **Reload TFLN PDK** supports runtime Python changes.

本版本有 13 个菜单动作，不含 SOI PDK 的波导 PCell 或 DRC 功能。白盒尚未提供公开在线安装器；保留已有授权安装，不用公开黑盒覆盖。

This version has 13 menu actions and does not include the SOI PDK waveguide PCells or DRC tools. There is no public online whitebox installer; preserve existing authorized installations.
