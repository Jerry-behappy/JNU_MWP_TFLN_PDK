# 使用说明 / User guide

## 器件与 Library / Devices

V1.1 提供五组固定 Library，数量为 1/2/1/49/2，以及 JNULib_TFLN_pcell 的九个公开 PCell。Technology 保持 JNU_MWP_TFLN_PDK。菜单保留中英文并列，共 27 个动作。
V1.1 provides five fixed libraries with 1/2/1/49/2 devices and nine independent PCells. The technology name stays stable and the 27 menu actions show Chinese and English together.

通过 Instance 选择工艺 Library 和器件，或使用“插入 TFLN 器件 / Insert Device”。固定器件带 PinRec 1/10、DevRec 68/0 和框内作者署名。交叉器件包含四向端口；偏振器件的交错终端保留实际坐标。
Place fixed cells from Instance or Insert Device. PinRec, DevRec, in-frame attribution and staggered/polarization interfaces are preserved.

## 公开黑盒与授权器件 / Blackboxes and local contours

公开固定器件的主体为 998/0 BlackBox，1/0 只保留端口向内 0.2 µm 直段。黑盒不含内部制造轮廓。完整 GDS 在本地独立保管，可通过“安装／更新白盒器件库”导入；导入时验证全部水平和竖直 PinRec。
Public fixed cells contain a 998/0 placeholder and 0.2 µm inward port stubs on 1/0. The SOI blackbox style is shared: orange diagonal hatching and a centered full cell name. Staggered facets use placeholder extensions so every original port still touches its straight. Authorized local contours can be imported independently after horizontal/vertical port validation.

黑盒显示与当前 SOI PDK 一致：998/0 橙色斜线，完整器件名居中，端口向内保留 0.2 µm。交错终端仅延伸占位主体以连接直段，保持端口坐标。原生 KLayout 使用 Basic TEXT；独立 Python 使用相同字体的矢量文字。旧默认配色在重载或打开视图时自动迁移，自定义配色保留。

在全新目录重新导出 55 个独立黑盒：`python tools/export_blackboxes.py --output NEW_DIRECTORY`。脚本仅读取公开接口清单，不读取制造轮廓。五份总览由已交付的分组 GDS 提供。

## 版图工具 / Layout tools

波导互转、器件连接、端口生成、图层排除、数字文本阵列、吸附、长度及长度差功能保留。五组总览均从当前清单生成。结构 DRC 只检查连接和识别结构，不包含 foundry 线宽/间距规则。
Waveguide conversion, connection, pin creation, layer exclusion, text arrays, snapping and length tools remain available. The DRC is structural, not a fabrication width/spacing deck.

## 图层与参数 / Layers and parameters

Waveguide 1/0 为上表面宽度；SiO2_Open 3/0；NiCr 4/0（200 nm）；Au 5/0（1 µm）；Dicing 7/0；Text 10/0；PinRec 1/10；DevRec 68/0；BlackBox 998/0。数据库单位为 0.0001 µm。低台阶待处理，不生成 2/0。

PCell 的几何实现和默认尺寸沿用此前版本，TFLN 光学性能需按实际工艺验证。未知参数、原始 GDS 回退和膜厚差异均列于[当前器件索引](DEVICE_INDEX.md)。
PCell geometry/defaults retain the previous implementation. The [device index](DEVICE_INDEX.md) lists unknown fields and source discrepancies.

## 安装与更新 / Installation and updates

V1.1 通过其 Git 分支安装和更新，参见仓库 README。拖入式安装宏继续跟踪稳定 main，不会自动切换到开发分支。更新开发分支时先保留本地修改，再运行 git pull --ff-only origin V1.1，重启 KLayout。
Install the V1.1 Git branch as described in the README. The existing drag-in installer follows stable main. Preserve local changes before fast-forwarding the development branch and restarting KLayout.
