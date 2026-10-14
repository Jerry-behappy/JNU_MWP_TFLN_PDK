<p align="right">
  <a href="README.md"><img src="docs/assets/readme/lang-zh.svg" alt="简体中文" height="30"></a>
  <a href="README.en.md"><img src="docs/assets/readme/lang-en-active.svg" alt="English (current)" height="30"></a>
</p>

<p align="center"><img src="docs/assets/readme/jinan-university-logo.png" alt="Jinan University" width="340"></p>

# JNU_MWP_TFLN_PDK

A KLayout thin-film lithium niobate (TFLN) PDK from the Jinan University optoelectronic hybrid integration laboratory. V1.0 provides the `JNU_MWP_TFLN_PDK` Technology, four process libraries, 13 fixed blackboxes, 55 optical ports and a layout menu.

The public edition can be installed and used independently. Blackboxes retain rectangular placeholders, PinRec, DevRec, device labels and author text. Whitebox GDS, FSP projects and internal device geometry are distributed through separate authorization. Blackboxes support placement and port connections; fabrication requires authorized whitebox geometry.

## Installation and updates

### Windows: install a Git clone

Requires KLayout 0.30.x with Python macros and [Git](https://git-scm.com/downloads).

```powershell
git clone https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK.git
cd JNU_MWP_TFLN_PDK
powershell -ExecutionPolicy Bypass -File .\Install_Cloned_PDK.ps1 -KLayoutDataPath "YOUR_KLAYOUT_USER_DIRECTORY"
```

The installer links `salt/JNU_MWP_TFLN_PDK` into the KLayout user directory and preserves existing installations. Restart KLayout, select `JNU_MWP_TFLN_PDK`, and check the four libraries and the `JNU_MWP_TFLN_PDK V1.0` menu.

### Install or update with an AI agent

Copy these prompts to an agent with local file and command access.

**Installation prompt**

> Install https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK in the KLayout I normally use. Locate its actual user directory, clone the repository and run Install_Cloned_PDK.ps1 to create a directory junction. Preserve other PDKs, existing TFLN installations, whiteboxes and local edits. Verify the Technology, four libraries, 13 blackboxes and menu.

**Update prompt**

> Update my installed JNU_MWP_TFLN_PDK. Locate its actual Git clone and update the current branch only when the worktree is clean and a fast-forward is possible. Preserve local edits and authorized whiteboxes. Verify the libraries and menu and tell me whether KLayout needs to restart.

### Maintenance and whiteboxes

- Run `git pull --ff-only origin main` from a clean clone, then restart KLayout. The **Reload TFLN PDK** menu also supports Python-only changes.
- Whiteboxes and original simulation projects are stored and authorized separately. This repository has no whitebox download, automatic whitebox installation or credential configuration.
- Contributions use feature branches and pull requests. Direct pushes, force pushes and deletion of `main` are blocked.

## Process libraries

| Library | Film / etch depth (nm) | Devices | Count |
|---|---:|---|---:|
| `JNULib_TFLN_300_125` | 300 / 125 | EC01 | 1 |
| `JNULib_TFLN_400_200` | 400 / 200 | EC02 | 1 |
| `JNULib_TFLN_600_300` | 600 / 300 | EC03, MMI01–07, POL01–02 | 10 |
| `JNULib_TFLN_600_600` | 600 / 600 | EC04 | 1 |

See the [device index](docs/DEVICE_INDEX.md) for parameters, ports and file links. Lower steps of EC01–EC03 remain pending. Unknown parameters use `Unknow`; discrepancies are retained in the public manifest.

## Features and user guide

Click a feature card to open the [user guide](docs/USER_GUIDE.md). Menu labels show Chinese and English together. The database unit is **0.0001 µm**.

<table>
  <tr><th colspan="2">JNU_MWP_TFLN_PDK V1.0 · Features</th></tr>
  <tr>
    <td width="50%"><a href="docs/USER_GUIDE.md#devices"><img src="docs/assets/features/devices-en.svg" width="520" alt="Process libraries"></a></td>
    <td width="50%"><a href="docs/USER_GUIDE.md#ports"><img src="docs/assets/features/ports-en.svg" width="520" alt="Ports and recognition"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="docs/USER_GUIDE.md#layout"><img src="docs/assets/features/layout-en.svg" width="520" alt="Layout and placement"></a></td>
    <td width="50%"><a href="docs/USER_GUIDE.md#layers"><img src="docs/assets/features/layers-en.svg" width="520" alt="Process layers"></a></td>
  </tr>
  <tr>
    <td width="50%"><a href="docs/USER_GUIDE.md#index"><img src="docs/assets/features/index-en.svg" width="520" alt="Files and overviews"></a></td>
    <td width="50%"><a href="docs/USER_GUIDE.md#installation"><img src="docs/assets/features/setup-en.svg" width="520" alt="Installation and maintenance"></a></td>
  </tr>
</table>

![600/300 nm public blackbox overview](salt/JNU_MWP_TFLN_PDK/previews/600_300.png)

Native author text inside each recognition frame: **By Songliang Chen, 2026/10/13**.

[Changelog](CHANGELOG.en.md) · [Issues](https://github.com/Jerry-behappy/JNU_MWP_TFLN_PDK/issues) · [License](LICENSE.md) · [Related SOI PDK](https://github.com/Jerry-behappy/JNU-MWP-SOI-PDK)
