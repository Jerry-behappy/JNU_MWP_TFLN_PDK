<p align="center"><img src="docs/assets/readme/jinan-university-logo.png" alt="暨南大学" width="340"></p>

# JNU_MWP_TFLN_PDK V1.1

暨南大学光电混合集成实验室 KLayout 薄膜铌酸锂 PDK。本分支仅保留膜厚 600 nm、刻蚀深度 300 nm、实际侧壁角 63° 的 24 个固定黑盒，共 108 个光学端口，另有九个独立 PCell。

本次工艺范围调整位于开发分支 `V1.2`。使用本次器件集合时，克隆命令选择 `--branch V1.2`；稳定版 `main` 在合并发布后获取这些调整。

[English](README.en.md) · [器件参数与文件索引](docs/DEVICE_INDEX.md) · [使用说明](docs/USER_GUIDE.md) · [更新说明](CHANGELOG.md)

## 安装稳定版 V1.1

```powershell
git clone --branch main https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK.git JNU_MWP_TFLN_PDK
powershell -ExecutionPolicy Bypass -File .\JNU_MWP_TFLN_PDK\Install_Cloned_PDK.ps1
```

完成后重启 KLayout，选择 JNU_MWP_TFLN_PDK。若已有安装，脚本会保留原目录并提示。稳定版及拖入式安装宏均跟踪 `main`；干净的稳定版克隆可执行 `git pull --ff-only origin main` 更新。

版本开发分支每次通过 PR 合入 `main` 后，小版本号自动加一，例如 `V1.4 → V1.5`、`V1.9 → V1.10`。当前版本分支见[分支列表](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/branches)。已有开发克隆先保留本地修改，再执行 `git fetch origin --prune`，按实际新旧名称执行 `git branch -m 旧分支 新分支` 和 `git branch --set-upstream-to=origin/新分支 新分支`。新开发克隆的 `--branch` 使用分支列表中的当前名称。

[稳定分支完整提交记录](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/commits/main) · [V1.2 开发分支完整提交记录](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/commits/V1.2)

## 器件库

| Library | 膜厚/刻蚀 nm | 器件 / Devices | 数量 |
|---|---:|---|---:|
| `JNULib_TFLN_600_300` | 600/300，侧壁角 63° | EC / MMI / PSR | 24 |
| `JNULib_TFLN_BlackBox` | 600/300，侧壁角 63° | 上述同一批固定黑盒的汇总库 | 24 |
| `JNULib_TFLN_pcell` | 参数化 / Parametric | TFLN 公开 PCell / Public TFLN PCells | 9 |

## 轮廓和待核对项

公开固定器件仅包含 998/0 占位主体、0.2 µm 端口直段、PinRec、DevRec 和框内署名。完整制造轮廓、FSP、补录源表留在本地。MMI-04 偏振和 EC-04-TM 包层仍待确认，端面耦合器低台阶仍待处理。逐项状态见器件索引。

[许可证 / License](LICENSE.md) · [相关 SOI PDK](https://github.com/Jerry-behappy/JNU-MWP-SOI-PDK)
