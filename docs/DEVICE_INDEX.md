# TFLN 器件索引 / Device Index

V1.0 · 2026-10-15 · 12 个固定器件 / fixed devices · 47 个固定端口 / fixed optical ports · 9 PCells。

公开固定 GDS 为矩形黑盒；PCell 另以可编辑参数化源码提供。 / Fixed GDS are blackboxes; PCells are editable source.

| ID | 器件 / Device | 晶向 / Cut | 传播 / Prop. | 膜厚 / Thickness (nm) | 刻蚀 / Etch (nm) | 实际侧壁角 / Angle (°) | MFD (µm) | 包层 / Cladding | 偏振 / Pol. | Pins | 文件 / File |
|---|---|---|---|---:|---:|---:|---|---|---|---:|---|
| EC01 | 端面耦合器 EC | x切 | y传 | 300 | 125 | 70 | Unknow | SiO₂包层 | TE、TM | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/300_125/EC_Xcut_Yprop_thickness300nm_etchDepth125nm_sidewallAngle70deg_MFDUnknowum_SIO2_TE-TM.gds) |
| EC02 | 端面耦合器 EC | x切 | y传 | 400 | 200 | 90 | Unknow | SiO₂包层 | TE、TM | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/400_200/EC_Xcut_Yprop_thickness400nm_etchDepth200nm_sidewallAngle90deg_MFDUnknowum_SIO2_TE-TM.gds) |
| EC03 | 端面耦合器 EC | x切 | y传 | 600 | 300 | 63 | 3.2 | 空气包层 | TE | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/EC_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_AIR_TE.gds) |
| EC04 | 端面耦合器 EC | x切 | y传 | 600 | 600 | 63 | 3.2 | 空气包层 | TE、TM | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_600/EC_Xcut_Yprop_thickness600nm_etchDepth600nm_sidewallAngle63deg_MFD3.2um_AIR_TE-TM.gds) |
| MMI01 | 1×2 MMI | x切 | y传 | 600 | 300 | 63 | — | 空气包层 | TE、TM | 3 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI1x2_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM.gds) |
| MMI02 | 2×2 MMI | x切 | y传 | 600 | 300 | 63 | — | 空气包层 | TE | 4 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI2x2_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI03 | 1×4 MMI | x切 | y传 | 600 | 300 | 63 | — | 空气包层 | TE | 5 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI04 | 1×4 MMI | x切 | z传 | 600 | 300 | 63 | — | 空气包层 | TE | 5 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI05 | 4×4 MMI | x切 | y传 | 600 | 300 | 63 | — | 空气包层 | TE | 8 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI06 | 4×4 MMI | x切 | z传 | 600 | 300 | 63 | — | 空气包层 | TE、TM | 8 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM.gds) |
| POL01 | PSR | x切 | z传 | 600 | 300 | 62 | — | 空气包层 | TE、TM | 3 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/PSR_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle62deg_AIR_TE-TM.gds) |
| POL02 | PDMC/DMPS | x切 | z传 | 600 | 300 | 62 | — | 空气包层 | TE、TM | 3 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/PDMC_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle62deg_AIR_TE-TM.gds) |

四组固定库 / Fixed libraries：`JNULib_TFLN_300_125` (1)、`JNULib_TFLN_400_200` (1)、`JNULib_TFLN_600_300` (9)、`JNULib_TFLN_600_600` (1)。

MMI07 已从当前库和索引移除。EC01、EC02 保留 `MFDUnknowum`。EC01–EC03 低台阶待处理，不合并到波导层。
MMI07 was removed. EC01/EC02 keep `MFDUnknowum`. Lower steps of EC01–EC03 remain deferred.

命名 / Naming：`Xcut` 晶向；`Yprop` / `Zprop` 传播方向；`thickness` 薄膜厚度；`etchDepth` 刻蚀深度；`sidewallAngle` 侧壁角；`MFD` 模场直径。未知值使用 `Unknow`。

侧壁角沿用代表工程实际上表面轮廓：EC01 70°、EC02 90°（工程集合有 65°/90°）、POL01/POL02 62°；目录名 63 表示目录侧壁角标记。MMI02 使用目录 63°，原始工程差异仍保留。
Angles follow the selected geometry: EC01 70°, EC02 90° (source variants 65°/90°), POL01/POL02 62°. MMI02 retains the directory value 63°; discrepancies remain recorded.

## 参数化器件 / PCells

`JNULib_TFLN_pcell` 独立包含 SOI PDK 的以下 9 个公开 PCell。几何算法和默认尺寸保留；TFLN 光学性能需另行设计验证。
The independent library copies nine public SOI PCells, retaining geometry and default dimensions. TFLN optical performance requires separate validation.

- `Pcell_Bend_90deg`
- `Pcell_Microring_DoubleBus`
- `Pcell_Archimedean_Spiral`
- `Pcell_Paperclip_Spiral`
- `Pcell_Paperclip_Spiral_with_Composite_Waveguide`
- `Pcell_Taper`
- `Pcell_S_Bend`
- `Pcell_Straight_Waveguide`
- `Pcell_Waveguide_Bump`

## 分组总览 / Process overviews

- 300_125：[GDS](../salt/JNU_MWP_TFLN_PDK/overviews/JNU_MWP_TFLN_PDK_300_125_V1.0_BLACKBOX.gds) · [预览 / Preview](../salt/JNU_MWP_TFLN_PDK/previews/300_125.png)
- 400_200：[GDS](../salt/JNU_MWP_TFLN_PDK/overviews/JNU_MWP_TFLN_PDK_400_200_V1.0_BLACKBOX.gds) · [预览 / Preview](../salt/JNU_MWP_TFLN_PDK/previews/400_200.png)
- 600_300：[GDS](../salt/JNU_MWP_TFLN_PDK/overviews/JNU_MWP_TFLN_PDK_600_300_V1.0_BLACKBOX.gds) · [预览 / Preview](../salt/JNU_MWP_TFLN_PDK/previews/600_300.png)
- 600_600：[GDS](../salt/JNU_MWP_TFLN_PDK/overviews/JNU_MWP_TFLN_PDK_600_600_V1.0_BLACKBOX.gds) · [预览 / Preview](../salt/JNU_MWP_TFLN_PDK/previews/600_600.png)
