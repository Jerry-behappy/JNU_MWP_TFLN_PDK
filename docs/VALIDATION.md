# 验证记录 / Validation

2026-10-26 · 固定器件：600/300 nm、实际侧壁角 63°

- 当前清单仅包含 24 个固定器件、108 个光学端口；工艺记录全部满足膜厚 600 nm、刻蚀深度 300 nm、sidewall_angle_deg=63。
- 工艺分组库、独立黑盒库和九个 PCell 构成三个 TFLN Technology 限定的 Library。其他工艺库在新启动的原生 KLayout 中不注册；更新后的旧会话需重启以清除缓存库。
- 原生 KLayout 与 SiEPIC 对公开黑盒和本地完整器件分别通过 24 个器件、108 个端口的识别、旋转/镜像、重载、24 项插入选择及 23 项中英菜单检查。旧工艺总览菜单的清理通过。
- 对照本地保存的上一版，24 个保留器件的独立 GDS 文件内容未改变，轮廓、端口及文字保持原样。工艺总览重新生成，只引用这 24 个器件；其原生图像已核对。
- 公开包只包含当前 24 个独立黑盒和一份工艺总览，共 25 个 GDS；31 个不符合工艺范围的器件及四份其他工艺总览从活动包移除。公开包检查逐文件核对清单和目录，防止遗留资源重新进入发行包。
- 独立 PCell 参数编辑及保存重开通过；授权 GDS 导入继续覆盖旋转为竖直方向的真实端口、无效端口拒绝和本地目录边界。

[公开版原生逐器件结果](validation/native_public.json)。本地完整器件报告和旧版本备份保留在本地，未随公开仓库分发。

Only 600 nm film / 300 nm etch / actual 63-degree sidewalls remain: 24 fixed devices, 108 optical ports, three libraries, 23 menu actions and one overview. Native KLayout/SiEPIC checks passed for both editions. Every retained individual GDS is unchanged from its previous version. Public files match the selected catalog; full contours and original projects remain local.

MMI-04 偏振、EC-04-TM 包层仍待确认；端面耦合器低台阶仍待处理。结构与文件检查不代替光学性能或工艺验收。
