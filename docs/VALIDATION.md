# 验证记录 / Validation

2026-10-19 · V1.1

- 55 个固定器件、216 个光学端口，五组数量 1/2/1/49/2，另有九个独立 PCell。
- 新增独立 `JNULib_TFLN_BlackBox`，共七个 Library。原生 KLayout 验证全部库仅匹配 TFLN Technology；默认、SOI、GSiP 和 EBeam 技术均不匹配。55 个黑盒实例与磁盘 GDS 的全部相关图层一致，旧全局关联可迁移；PCell 在读取前选用 TFLN 技术时保存重开正常。复验脚本为 `tools/verify_library_scope.py`。
- 原生 KLayout 0.30.9 与 SiEPIC 实测本地完整器件和公开黑盒：端口及 DevRec 识别、旋转/镜像、五组总览、55 项插入选择、27 项中英菜单、快捷键保留及库重载均通过。
- 黑盒显示同步当前 SOI：998/0 橙色斜线、完整器件名居中、端口向内 0.2 µm。交错终端的占位主体延伸至直段，端口保持原位。旧默认配色迁移通过。
- 55 组本地/公开接口一致。公开导出脚本重新生成的全部几何与交付 GDS 一致；实例化后保存重开保持接口与主体。
- 独立 PCell 参数编辑、端口及保存重开、授权 GDS 导入与无效端口拒绝、安装器保护检查通过。55 个独立 GDS 和五个总览均已原生渲染预览。
- 公开文件检查拒绝 FSP、源表、白盒目录和内部制造轮廓。

[公开版原生逐器件结果](validation/native_public.json)。完整本地结果保存在授权安装的 evidence/v11 中。公开验证脚本为 tools/verify_public_pdk.py、tools/verify_pcell_library.py、tools/verify_authorized_gds.py 和 tools/verify_installer.py。

Native KLayout and SiEPIC recognized all 55 devices and 216 optical pins in both editions, including rotation, mirroring, reloading, five overviews and 27 bilingual menu actions. All 55 interface pairs match, and the interface-only blackbox exporter reproduces the delivered geometry. Fixed-cell save/reopen, nine independent PCells and local authorized imports passed. Manufacturing contours remain local.

原生 UI 复验脚本 tools/verify_native_ui.py 需在独立 KLayout 进程运行，并安装 SiEPIC；可通过 siepic_python 指定其 Python 目录，通过 report_path 指定结果。脚本退出该测试进程，不应在用户正在编辑的会话中运行。CI 使用独立 Python API 检查结构，不替代原生 UI 记录。

MMI-10 为原 GDS 回退，上表面宽度未确认；MMI-11、PSR-03 的清单与源工程存在膜厚差异。四项参数和端面耦合器低台阶仍待处理，详见器件索引。结构验证不代表这些项已通过工艺或光学验收。
