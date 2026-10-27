# 使用说明 / User guide

## 工艺与器件库 / Process and libraries

固定器件工艺范围为膜厚 600 nm、刻蚀深度 300 nm、实际侧壁角 63°。共 24 个固定器件、108 个光学端口，包括 7 个端面耦合器、16 个 MMI 和 1 个 PSR；独立 TE/TM 工程保留独立记录。其他组合及角度的固定器件已退出本分支器件库。
Only 600 nm film, 300 nm etch and an actual 63° sidewall angle are retained: 24 fixed devices and 108 optical ports, comprising seven edge couplers, sixteen MMIs and one PSR. Independent TE/TM designs retain separate records.

- JNULib_TFLN_600_300：24 个固定器件，600/300 nm，侧壁角 63°。
- JNULib_TFLN_BlackBox：同一批 24 个固定器件的独立黑盒汇总库。
- JNULib_TFLN_pcell：九个公开参数化器件，几何实现和默认尺寸保持不变。

三个 Library 仅在选择 JNU_MWP_TFLN_PDK Technology 时显示。更新后保存当前工作并重启 KLayout，清除旧会话缓存的其他工艺库。菜单保留中英文并列，共 23 项动作，只有一个工艺总览入口。
All three libraries are scoped to JNU_MWP_TFLN_PDK. Save work and restart KLayout after updating to clear old process libraries cached in the session. The 23 menu actions remain bilingual and offer one process overview.

## 放置与端口 / Placement and ports

通过 Instance 选择相应 Library，或使用“插入 TFLN 器件 / Insert Device”。器件与文件采用简名，工艺参数及追溯编号保留在清单中；上表面轮廓、PinRec、DevRec、端口坐标/方向/宽度及框内作者文字不改变。PSR 交错终端保留实际位置。旋转及镜像随实例变换。
Place cells through Instance or Insert Device. Cell and file names are shortened; process parameters and traceability IDs remain in the catalog. Geometry, PinRec/DevRec, port positions, directions and widths are unchanged. Staggered PSR facets retain their coordinates.

## 黑盒与授权完整器件 / Blackboxes and authorized contours

公开包的主体为 998/0 BlackBox，橙色斜线填充，完整器件名居中；1/0 只保留端口向内 0.2 µm 直段。制造轮廓、FSP 和源表留在本地。授权导入只匹配当前清单中的 24 个器件；导入验证水平和竖直 PinRec。
Public cells contain 998/0 placeholders and 0.2 µm inward port straights on 1/0. Manufacturing contours and source files remain local. Authorized imports match the current catalog and validate horizontal/vertical ports.

通过 `python tools/export_blackboxes.py --output NEW_DIRECTORY` 可在新目录重新导出当前 24 个独立黑盒，输入仅为公开接口清单。当前包另含一份 600/300 nm、63° 总览 GDS。

## 版图工具与图层 / Tools and layers

波导互转、器件连接、端口生成、图层排除、数字文本阵列、吸附、长度及长度差功能保留。结构 DRC 检查连接和识别结构，不包含 foundry 线宽/间距规则。
Waveguide conversion, connection, pin creation, layer exclusion, numerical text, snapping and length tools remain available. DRC is structural rather than a foundry rule deck.

Waveguide 1/0 使用上表面宽度；SiO2_Open 3/0；NiCr 4/0（200 nm）；Au 5/0（1 µm）；Dicing 7/0；Text 10/0；PinRec 1/10；DevRec 68/0；BlackBox 998/0。数据库单位为 0.0001 µm。不生成 2/0，端面耦合器低台阶仍待处理。

MMI-04 偏振和 EC-04-TM 包层待确认，详见[器件索引](DEVICE_INDEX.md)。PCell 和固定器件仍需按实际工艺进行光学性能验证。

## 安装与更新 / Installation and updates

稳定 main 已包含当前 600/300 nm、63° 器件集合和芯片层栈说明，按仓库 README 安装。版本开发分支每次合入 main 后自动递增小版本号，当前开发分支见分支列表。更新前保留本地修改，更新完成后重启 KLayout。
Stable main includes the current 600/300 nm, 63-degree device set and chip-stack documentation. Follow the repository README for installation. Version development branches advance after merging into main; use the branch list to find the current name. Preserve local changes and restart KLayout after updating.
