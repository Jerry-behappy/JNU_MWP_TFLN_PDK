<p align="center"><img src="docs/assets/readme/jinan-university-logo.png" alt="暨南大学" width="340"></p>

# JNU_MWP_TFLN_PDK V1.1

KLayout thin-film lithium-niobate PDK. This branch registers 55 fixed blackboxes, 216 optical ports, five film/etch libraries and nine independent PCells.

[简体中文](README.md) · [Device index](docs/DEVICE_INDEX.md) · [User guide](docs/USER_GUIDE.md) · [Changes](CHANGELOG.en.md)

## Install stable V1.1

```powershell
git clone --branch main https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK.git JNU_MWP_TFLN_PDK
powershell -ExecutionPolicy Bypass -File .\JNU_MWP_TFLN_PDK\Install_Cloned_PDK.ps1
```

Restart KLayout and select JNU_MWP_TFLN_PDK. The installer preserves an existing installation instead of replacing it. Both stable installs and the drag-in macro follow `main`. To update a clean stable checkout, run `git pull --ff-only origin main`.

After a version branch merges into `main` through a PR, its minor number advances automatically, for example `V1.4 → V1.5` or `V1.9 → V1.10`. Find the current development branch in the [branch list](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/branches). Preserve local changes, run `git fetch origin --prune`, then use the actual names in `git branch -m OLD_BRANCH NEW_BRANCH` and `git branch --set-upstream-to=origin/NEW_BRANCH NEW_BRANCH`. New development checkouts use the current name with `--branch`.

[Stable branch commit history](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/commits/main) · [V1.2 development commit history](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/commits/V1.2)

## Libraries

| Library | 膜厚/刻蚀 nm | 器件 / Devices | 数量 |
|---|---:|---|---:|
| `JNULib_TFLN_300_125` | 300/125 | EC-08 | 1 |
| `JNULib_TFLN_300_300` | 300/300 | MMI-11, PSR-03 | 2 |
| `JNULib_TFLN_400_200` | 400/200 | EC-09 | 1 |
| `JNULib_TFLN_600_300` | 600/300 | EC / MMI / PSR / PDMC / PBS / DC / CROSS / GC | 49 |
| `JNULib_TFLN_600_600` | 600/600 | EC-02, EC-02-TM | 2 |
| `JNULib_TFLN_BlackBox` | 全部工艺 / All processes | Aggregate of the same 55 fixed blackboxes | 55 |
| `JNULib_TFLN_pcell` | 参数化 / Parametric | TFLN 公开 PCell / Public TFLN PCells | 9 |

## Geometry and pending fields

The public fixed library contains 998/0 placeholders, 0.2 µm port stubs, PinRec, DevRec and in-frame attribution. Manufacturing contours, FSPs and the completed source workbook stay local. MMI-10 uses its existing GDS pending top-width verification; MMI-11 and PSR-03 retain a catalog/source film-thickness discrepancy. Four records still contain Unknow fields. Lower edge-coupler steps remain deferred. See the device index for each record.

By Songliang Chen, 2026/10/13 — GDS 框内署名 / in-frame GDS attribution.

## 预览 / Previews

![300_125 nm](salt/JNU_MWP_TFLN_PDK/previews/300_125.png)

![300_300 nm](salt/JNU_MWP_TFLN_PDK/previews/300_300.png)

![400_200 nm](salt/JNU_MWP_TFLN_PDK/previews/400_200.png)

![600_300 nm](salt/JNU_MWP_TFLN_PDK/previews/600_300.png)

![600_600 nm](salt/JNU_MWP_TFLN_PDK/previews/600_600.png)

[许可证 / License](LICENSE.md) · [相关 SOI PDK](https://github.com/Jerry-behappy/JNU-MWP-SOI-PDK)
