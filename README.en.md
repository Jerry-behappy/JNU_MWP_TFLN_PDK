<p align="center"><img src="docs/assets/readme/jinan-university-logo.png" alt="暨南大学" width="340"></p>

# JNU_MWP_TFLN_PDK V1.1

KLayout thin-film lithium-niobate PDK. This branch retains only 600 nm film thickness, 300 nm etch depth and an actual sidewall angle of 63 degrees: 24 fixed blackboxes, 108 optical ports and nine independent PCells.

This process-scope update is on development branch `V1.2`. To install this device set, use `--branch V1.2` in the clone command; stable `main` receives the update after release merging.

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
| `JNULib_TFLN_600_300` | 600/300, sidewall 63° | EC / MMI / PSR | 24 |
| `JNULib_TFLN_BlackBox` | 600/300, sidewall 63° | Aggregate of the same fixed blackboxes | 24 |
| `JNULib_TFLN_pcell` | 参数化 / Parametric | TFLN 公开 PCell / Public TFLN PCells | 9 |

## Geometry and pending fields

The public fixed library contains 998/0 placeholders, 0.2 µm port stubs, PinRec, DevRec and in-frame attribution. Manufacturing contours, FSPs and the completed source workbook stay local. MMI-04 polarization and EC-04-TM cladding remain unconfirmed. Lower edge-coupler steps remain deferred. See the device index for each record.

[许可证 / License](LICENSE.md) · [相关 SOI PDK](https://github.com/Jerry-behappy/JNU-MWP-SOI-PDK)
