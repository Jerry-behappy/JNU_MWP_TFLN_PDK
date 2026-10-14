# V1.0 公开版验收 / Public Edition Validation

本地使用原生 KLayout 0.30.9 验证，2026-10-14：

- 四个真实 Library 的器件数量为 1、1、10、1；13 个黑盒均可实例化并保存重开。
- 17 份 GDS（13 个独立器件与 4 个总览）中的 Waveguide 只包含矩形占位；没有内部轮廓、FSP 或原始工程清单。
- 全部 55 个光学端口保留坐标、宽度和方向；原生 SiEPIC 识别得到 13 个器件，并通过旋转、镜像验证。
- 13 项菜单动作可加载、执行并重复重载；作者署名位于 DevRec 框内。
- 隔离的公开安装在没有 SOI PDK、没有白盒器件库时可启动和使用。安装器重复运行会保留同一目录联接。

Validated locally with native KLayout 0.30.9 on 2026-10-14: four libraries (1/1/10/1), 13 placeable blackboxes, 55 preserved optical ports, save/reopen, SiEPIC recognition, rotation/mirroring, 13 menu actions and author text inside DevRec. The standalone public installation runs without the SOI PDK or whitebox data.

公开回归入口 / Public regression command:

```shell
python -m pip install 'klayout>=0.30,<0.31'
python tools/verify_public_pdk.py
```

GitHub Actions 在 main 推送和 PR 时运行同一公开目录与黑盒接口检查；原生 GUI 与 SiEPIC 的本地验收单独完成。
GitHub Actions runs the public-file and blackbox-interface checks on main pushes and pull requests. Native GUI and SiEPIC checks were completed separately on the local installation.
