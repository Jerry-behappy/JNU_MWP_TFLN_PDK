# TFLN 黑盒器件索引 / Blackbox Device Index

V1.0 · 13 个固定黑盒 / fixed blackboxes · 55 个光学端口 / optical ports · DBU 0.0001 µm。

GDS 只含矩形占位、端口、识别框和文字，内部制造轮廓由独立授权提供。
Files contain rectangular placeholders, ports, recognition frames and text. Internal fabrication geometry requires separate authorization.

| ID | 器件 / Device | Library | 晶向 / Cut | 传播 / Propagation | 偏振 / Polarization | Pins | 文件 / File |
|---|---|---|---|---|---|---:|---|
| EC01 | 端面耦合器 EC | JNULib_TFLN_300_125 | Unknow | Unknow | TE、TM | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/300_125/EC_cutUnknow_propUnknow_thickness300nm_etchDepth125nm_sidewallAngle70deg_MFDUnknowum_SIO2_TE-TM.gds) |
| EC02 | 端面耦合器 EC | JNULib_TFLN_400_200 | Unknow | Unknow | 未明确 | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/400_200/EC_cutUnknow_propUnknow_thickness400nm_etchDepth200nm_sidewallAngle90deg_MFDUnknowum_SIO2.gds) |
| EC03 | 端面耦合器 EC | JNULib_TFLN_600_300 | Unknow | Unknow | 未明确 | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/EC_cutUnknow_propUnknow_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_AIR.gds) |
| EC04 | 端面耦合器 EC | JNULib_TFLN_600_600 | Unknow | Unknow | TE、TM | 2 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_600/EC_cutUnknow_propUnknow_thickness600nm_etchDepth600nm_sidewallAngle63deg_MFD3.2um_AIR_TE-TM.gds) |
| MMI01 | 1×2 MMI | JNULib_TFLN_600_300 | x切 | y传 | TE、TM | 3 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI1x2_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM.gds) |
| MMI02 | 2×2 MMI | JNULib_TFLN_600_300 | Unknow | Unknow | 未明确 | 4 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI2x2_cutUnknow_propUnknow_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR.gds) |
| MMI03 | 1×4 MMI | JNULib_TFLN_600_300 | x切 | y传 | TE | 5 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI04 | 1×4 MMI | JNULib_TFLN_600_300 | x切 | z传 | TE | 5 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI05 | 4×4 MMI | JNULib_TFLN_600_300 | x切 | y传 | TE | 8 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE.gds) |
| MMI06 | 4×4 MMI | JNULib_TFLN_600_300 | x切 | z传 | TE、TM | 8 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM.gds) |
| MMI07 | 4×4 MMI（按文件名） | JNULib_TFLN_600_300 | Unknow | Unknow | 未明确 | 8 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/MMI4x4_cutUnknow_propUnknow_thickness600nm_etchDepth300nm_sidewallAngleUnknowdeg_cladUnknow.gds) |
| POL01 | PSR（偏振分束旋转器，按命名） | JNULib_TFLN_600_300 | x切 | z传 | TE、TM | 3 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/PSR_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle62deg_AIR_TE-TM.gds) |
| POL02 | PDMC/DMPS（缩写待确认） | JNULib_TFLN_600_300 | x切 | z传 | TE、TM | 3 | [GDS](../salt/JNU_MWP_TFLN_PDK/pymacros/tfln_blackbox_gds/600_300/PDMC_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle62deg_AIR_TE-TM.gds) |

每个文件名与顶层 Cell 使用 `thickness`、`etchDepth`、`sidewallAngle`；端面耦合器还含 `MFD` 和包层，未知值使用 `Unknow`。
Names encode film thickness, etch depth, sidewall angle, crystal cut and propagation direction. Edge couplers also encode MFD and cladding; unknown values use `Unknow`.

EC01–EC03 的低台阶待处理。参数差异记录在 `../manifest.json`，不包含原始工程路径。
Lower steps of EC01–EC03 remain pending. Parameter discrepancies are recorded in `../manifest.json` without original project paths.
