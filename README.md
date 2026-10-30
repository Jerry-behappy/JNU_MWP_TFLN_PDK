<p align="center"><img src="docs/assets/readme/jinan-university-logo.png" alt="暨南大学" width="340"></p>

# JNU_MWP_TFLN_PDK V1.1

暨南大学光电混合集成实验室 KLayout 薄膜铌酸锂 PDK。本分支仅保留膜厚 600 nm、刻蚀深度 300 nm、实际侧壁角 63° 的 24 个固定黑盒，共 108 个光学端口，另有九个独立 PCell。

稳定版 `main` 提供当前 600/300 nm、63° 器件集合及以下芯片层栈参数。

[English](README.en.md) · [器件参数与文件索引](docs/DEVICE_INDEX.md) · [使用说明](docs/USER_GUIDE.md) · [更新说明](CHANGELOG.md)

## LN 芯片参数

晶向、传播方向和侧壁角依据当前 PDK 器件清单。加工需求中的沉积层与各器件的仿真包层标签分别列出。

| 参数 | 规格 | 说明 |
|---|---|---|
| LN 薄膜厚度 | **600 nm** | 300 nm slab + 300 nm 结构层 |
| 刻蚀深度 / Etch depth | **300 nm** | 当前固定器件工艺 |
| 剩余平板层 / Slab | **300 nm** | 波导外保留的 LN 层 |
| 埋氧层 / BOX | **2 µm** | 加工需求明确的 BOX 厚度；材料未单独注明 |
| 上包层 / Top cladding | **SiO₂，1 µm** | 参考加工流程的沉积层，兼作电极与波导之间的隔离层 |
| 晶向 / Crystal cut | **X-cut（x 切）** | 所保留固定器件的共同晶向 |
| 传播方向 / Propagation | **Y 或 Z** | 按器件分别登记，见器件索引 |
| 侧壁角 / Sidewall angle | **63°** | 当前器件库的筛选条件 |
| 波导宽度基准 | **上表面宽度** | GDS 波导图形采用该宽度 |
| NiCr 电极厚度 | **200 nm** | 对应当前 PDK 的 4/0 图层 |
| Au 电极厚度 | **1 µm** | 对应当前 PDK 的 5/0 图层 |
| 支撑衬底 / Handle substrate | **待确认** | 加工需求未注明材料及厚度 |
| 芯片尺寸 / Die size | **待确认** | 加工需求中的尺寸仍为空缺 |

### 器件包层版本

| Top cladding 标签 | 固定器件数量 | 参数状态 |
|---|---:|---|
| AIR | 7 | 空气上包层设计 |
| SiO₂ | 10 | SiO₂ 上包层设计；参考加工流程给出 1 µm 沉积厚度，逐器件仿真采用的厚度需另行核对 |
| SiON | 6 | SiON 上包层设计；该加工需求未给出 SiON 厚度及折射率 |
| 待确认 | 1 | EC-04-TM 的包层尚未确认 |

**1 µm SiO₂ 是上述加工需求指定的沉积层，不代表 AIR、SiON 等设计版本采用同一上包层。**各版本的器件归属见器件索引；这里记录的是参考加工要求，尚不代表已完成制造或验收。

## 安装稳定版 V1.1

```powershell
git clone --branch main https://github.com/Jinan-Photonics-Integration-Center/JNU_MWP_TFLN_PDK.git JNU_MWP_TFLN_PDK
powershell -ExecutionPolicy Bypass -File .\JNU_MWP_TFLN_PDK\Install_Cloned_PDK.ps1
```

完成后重启 KLayout，选择 JNU_MWP_TFLN_PDK。若已有安装，脚本会保留原目录并提示。稳定版及拖入式安装宏均跟踪 `main`；干净的稳定版克隆可执行 `git pull --ff-only origin main` 更新。

组织成员可通过“安装／更新白盒器件库 / Install / Update Whitebox Library”克隆或更新组织的[私有白盒库](https://github.com/Jinan-Photonics-Integration-Center/JNU_MWP_TFLN_Library)。认证使用本机 Git；也可选择“本地导入 / Import local folder”导入已下载的器件目录。白盒独立保存在用户私有目录。

版本开发分支每次通过 PR 合入 `main` 后，小版本号自动加一，例如 `V1.4 → V1.5`、`V1.9 → V1.10`。当前版本分支见[分支列表](https://github.com/Jinan-Photonics-Integration-Center/JNU_MWP_TFLN_PDK/branches)。已有开发克隆先保留本地修改，再执行 `git fetch origin --prune`，按实际新旧名称执行 `git branch -m 旧分支 新分支` 和 `git branch --set-upstream-to=origin/新分支 新分支`。新开发克隆的 `--branch` 使用分支列表中的当前名称。

[稳定分支完整提交记录](https://github.com/Jinan-Photonics-Integration-Center/JNU_MWP_TFLN_PDK/commits/main) · [开发分支列表](https://github.com/Jinan-Photonics-Integration-Center/JNU_MWP_TFLN_PDK/branches)

## 器件库

| Library | 膜厚/刻蚀 nm | 器件 / Devices | 数量 |
|---|---:|---|---:|
| `JNULib_TFLN_600_300` | 600/300，侧壁角 63° | EC / MMI / PSR | 24 |
| `JNULib_TFLN_BlackBox` | 600/300，侧壁角 63° | 上述同一批固定黑盒的汇总库 | 24 |
| `JNULib_TFLN_pcell` | 参数化 / Parametric | TFLN 公开 PCell / Public TFLN PCells | 9 |

## 轮廓和待核对项

公开固定器件仅包含 998/0 占位主体、0.2 µm 端口直段、PinRec、DevRec 和框内署名。完整制造轮廓、FSP、补录源表留在本地。MMI-04 偏振和 EC-04-TM 包层仍待确认，端面耦合器低台阶仍待处理。逐项状态见器件索引。

[许可证 / License](LICENSE.md) · [相关 SOI PDK](https://github.com/Jerry-behappy/JNU-MWP-SOI-PDK)
