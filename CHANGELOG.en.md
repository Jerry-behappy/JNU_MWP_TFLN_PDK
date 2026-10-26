# Changelog

## 2026-10-26 — Waveguide output-layer selection

- Add a shared output-layer dropdown to Path to Waveguide for single-width, composite-width and user-defined modes. It lists technology and custom layout layers and defaults to 1/0.
- Store the layer in the actual PCell and recovery metadata, preserve it after GDS reopen and distinguish variants on different layers. Waveguide to Path restores each instance to its waveguide layer; legacy data defaults to 1/0.

## 2026-10-26 — Fixed-device process scope

- Publish the V1.2 process-scope and chip-parameter updates to main. After merging, automation advances the development branch to V1.3 without changing the internal PDK version.
- Document the reference chip stack in both READMEs and the package README: 600 nm LN, 300 nm etch/slab, 2 µm BOX, 1 µm deposited SiO₂ and electrode thicknesses. Distinguish AIR/SiO₂/SiON design tags and retain unconfirmed substrate/die-size fields.
- Retain only 600 nm film / 300 nm etch / actual 63-degree sidewall designs: 24 fixed devices and 108 optical ports. Remove unsupported process/angle resources.
- Align the process library, independent blackbox library and single overview; keep nine PCells across three TFLN-scoped libraries.
- Retained geometry, names, interfaces and in-frame text are unchanged. Keep source projects/backups local and update the device index, bilingual documentation, 23 menu actions and checks.

## 2026-10-19 — V1.1

- Remove device image sections and personal attribution lines from both READMEs; enforce the presentation policy through repository guidance and CI.
- Automatically advance the minor number of a version branch after merging it into main (for example, V1.4 to V1.5). CI matches all version branches; existing target branches and concurrent work are preserved. The internal PDK release version is unchanged.
- Publish V1.1 to stable `main` and rename the development branch from `V1.1` to `V1.2`; update installation instructions and CI branch selection while retaining the V1.1 release version.
- Add the independent `JNULib_TFLN_BlackBox` with all 55 fixed blackboxes, alongside the five process libraries and nine PCells. All seven libraries are scoped to `JNU_MWP_TFLN_PDK`; reload migrates old global associations.
- Register 55 fixed devices and 216 optical ports from the completed catalog, with fixed groups 1/2/1/49/2 and nine independent PCells.
- Keep separate TE/TM designs, four-direction crossing ports and staggered polarization interfaces.
- Publish 998/0 placeholders and 1/0 port stubs only; keep full contours local.
- Match current SOI blackboxes: orange diagonal hatching, centered full cell names and 0.2 um port straights. Preserve staggered facets with placeholder extensions; add interface-only export and legacy default-color migration.
- Retain MMI-10 top-width verification, MMI-11/PSR-03 film-thickness discrepancies and four unknown parameter records.
- Add the fifth process overview, 27 bilingual actions and V1.1 branch CI.

## 2026-10-15 — V1.0

- Update fixed-device filenames and top cells from the completed parameter sheet; EC01/EC02 keep unknown MFD.
- Remove MMI07: fixed groups are 1/1/9/1, totaling 12 devices and 47 optical ports.
- Add independent JNULib_TFLN_pcell with nine public SOI PCells and original default dimensions.
- Add matching JNU PDK tools with 26 simultaneous Chinese/English actions and TFLN structural DRC.
- Remove By Songliang Chen from Library descriptions; preserve author text inside fixed-device frames.

## 2026-10-14 — V1.0 Public Edition

- Added the standalone `Install_JNU_TFLN_PDK.lym`: drag into KLayout, detect its user directory, clone/link or safely fast-forward in the background, and preserve existing installations and local edits.
- Published four process libraries with 13 fixed blackboxes and 55 optical ports.
- Retained the Technology, red Waveguide style, PinRec, DevRec and 13 menu actions.
- Blackboxes contain rectangles, interfaces, recognition frames and text. Whiteboxes, FSP projects, internal geometry and original project indexes remain local.
- Author text stays inside recognition frames and scales down for short devices.
- Added Git clone installation, bilingual documentation, a device index and blackbox overviews.
- Updates to main require pull requests; direct pushes, force pushes and deletion are blocked.

Lower steps of EC01–EC03 remain pending. Unknown parameters and source discrepancies are retained.
