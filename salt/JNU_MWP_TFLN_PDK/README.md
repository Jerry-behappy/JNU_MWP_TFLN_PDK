<p align="right">
  <a href="../../README.md"><img src="../../docs/assets/readme/lang-zh-active.svg" alt="简体中文（当前）" height="30"></a>
  <a href="../../README.en.md"><img src="../../docs/assets/readme/lang-en.svg" alt="English" height="30"></a>
</p>

<p align="center"><img src="../../docs/assets/readme/jinan-university-logo.png" alt="暨南大学校徽与校名" width="340"></p>

# JNU_MWP_TFLN_PDK

暨南大学光电混合集成实验室的 KLayout 薄膜铌酸锂（TFLN）PDK。V1.0 提供 `JNU_MWP_TFLN_PDK` Technology、四组工艺器件库、13 个固定黑盒、55 个光学端口及版图功能菜单。

公开版可独立安装和放置黑盒器件。黑盒保留矩形占位、PinRec、DevRec、器件标签和作者署名；白盒 GDS、FSP 及内部器件轮廓由独立授权提供，不随公开仓库发布。黑盒用于布局和端口连接，最终制造需使用获授权的白盒轮廓。

## 安装与更新

### Windows：Git 克隆安装

需要 KLayout 0.30.x、Python 宏支持及 [Git](https://git-scm.com/downloads)。在希望保存源码的目录运行：

```powershell
git clone https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK.git
cd JNU_MWP_TFLN_PDK
powershell -ExecutionPolicy Bypass -File .\Install_Cloned_PDK.ps1 -KLayoutDataPath "你的KLayout用户目录"
```

安装脚本将 `salt/JNU_MWP_TFLN_PDK` 联接到 KLayout 用户目录，不覆盖已有安装。重启 KLayout 后选择 `JNU_MWP_TFLN_PDK` Technology，确认四个 Library 和 `JNU_MWP_TFLN_PDK V1.0` 顶部菜单出现。

### 用 AI 代理安装或更新

将以下文字复制给能够访问本机文件并执行命令的 AI 代理。

**安装提示词**

> 请在我平时使用的 KLayout 中安装 https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK 。确认实际使用的 KLayout 用户目录，Git 克隆后运行 Install_Cloned_PDK.ps1，通过目录联接安装。保留其他 PDK、现有 TFLN 安装、白盒和本地修改。完成后检查 Technology、四个 Library、13 个黑盒和功能菜单。

**更新提示词**

> 请更新我当前 KLayout 安装的 JNU_MWP_TFLN_PDK。找到实际使用的 Git 克隆，只在工作树干净且可快进时更新当前分支，保留本地修改及授权白盒。更新后检查器件库和菜单，并说明是否需要重启 KLayout。

### 更新与白盒

- 在干净的克隆目录执行 `git pull --ff-only origin main`，然后重启 KLayout。仅修改 Python 功能时也可运行菜单中的 **重新加载 TFLN PDK**。
- 白盒与原始仿真工程单独保存和授权；公开仓库没有白盒下载、自动白盒安装或凭据配置。
- 贡献者通过功能分支与 PR 提交更新；`main` 禁止直接推送、强推和删除。

## 器件库

| Library | 薄膜厚度 / 刻蚀深度（nm） | 黑盒器件 | 数量 |
|---|---:|---|---:|
| `JNULib_TFLN_300_125` | 300 / 125 | EC01 | 1 |
| `JNULib_TFLN_400_200` | 400 / 200 | EC02 | 1 |
| `JNULib_TFLN_600_300` | 600 / 300 | EC03、MMI01–07、POL01–02 | 10 |
| `JNULib_TFLN_600_600` | 600 / 600 | EC04 | 1 |

完整参数、端口和文件索引见 [器件清单](docs/DEVICE_INDEX.md)。EC01–EC03 的低台阶仍待处理；未知参数使用 `Unknow`，参数差异保留在公开清单中。

## 功能与使用说明

点击功能框进入[详细使用说明](docs/USER_GUIDE.md)。菜单名称使用中英文并列，数据库单位为 **0.0001 µm**。

<table>
  <tr><th colspan="2">JNU_MWP_TFLN_PDK V1.0 · 功能框图</th></tr>
  <tr>
    <td width="50%"><a href="../../docs/USER_GUIDE.md#devices"><img src="../../docs/assets/features/devices-zh.svg" width="520" alt="工艺器件库"></a></td>
    <td width="50%"><a href="../../docs/USER_GUIDE.md#ports"><img src="../../docs/assets/features/ports-zh.svg" width="520" alt="端口与识别"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="../../docs/USER_GUIDE.md#layout"><img src="../../docs/assets/features/layout-zh.svg" width="520" alt="版图与放置"></a></td>
    <td width="50%"><a href="../../docs/USER_GUIDE.md#layers"><img src="../../docs/assets/features/layers-zh.svg" width="520" alt="工艺图层"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="../../docs/USER_GUIDE.md#index"><img src="../../docs/assets/features/index-zh.svg" width="520" alt="文件与总览"></a></td>
    <td width="50%"><a href="../../docs/USER_GUIDE.md#installation"><img src="../../docs/assets/features/setup-zh.svg" width="520" alt="安装与维护"></a></td>
  </tr>
</table>

![600/300 nm 公开黑盒器件总览](previews/600_300.png)

器件内原生文字署名：**By Songliang Chen, 2026/10/13**。

[更新说明](../../CHANGELOG.md) · [问题反馈](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/issues) · [许可证](../../LICENSE.md) · [相关 SOI PDK](https://github.com/Jerry-behappy/JNU-MWP-SOI-PDK)
