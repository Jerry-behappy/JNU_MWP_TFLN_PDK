# 器件参数与文件索引 / Device index

2026-10-26 · 600/300 nm · 63°

固定器件仅保留膜厚 600 nm、刻蚀深度 300 nm、实际侧壁角 63° 的 24 个器件，共 108 个光学端口。角度依据 sidewall_angle_deg，不按目录标称值代替。
Only 600 nm film / 300 nm etch / actual 63° sidewall designs are retained: 24 fixed devices, 108 optical ports. Independent TE/TM designs remain separate records.

文件名保留 ASCII x、thickness、etchDepth、sidewallAngle、MFD 和 Unknow。九个独立 PCell 不参与固定工艺记录筛选。

| 编号 / ID | Library | 晶向/传播 | 厚度/刻蚀 nm | 侧壁角 ° | MFD µm / 包层 | 偏振 | 端口 | GDS | 状态 |
|---|---|---|---:|---:|---|---|---:|---|---|
| EC-01 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / AIR | TE | 2 | [EC01_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_AIR_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC01_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_AIR_TE_v01.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| MMI-01 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE、TM | 3 | [MMI1x2_01_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x2_01_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM_v01.gds) | 已生成 / Generated |
| MMI-02 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE | 5 | [MMI1x4_02_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_02_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE_v01.gds) | 已生成 / Generated |
| MMI-03 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / AIR | TE | 5 | [MMI1x4_03_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_03_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE_v01.gds) | 已生成 / Generated |
| MMI-04 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE、TM（待确认） | 4 | [MMI2x2_04_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_polUnknow_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI2x2_04_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_polUnknow_v01.gds) | 清单参数仍有待确认字段 |
| MMI-05 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE | 8 | [MMI4x4_05_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_05_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE_v01.gds) | 已生成 / Generated |
| MMI-06 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / AIR | TE、TM | 8 | [MMI4x4_06_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_06_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_AIR_TE-TM_v01.gds) | 已生成 / Generated |
| EC-03 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiO₂ | TE | 2 | [EC03_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SIO2_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC03_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SIO2_TE_v01.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| EC-04 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiO₂ | TE | 2 | [EC04_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SIO2_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC04_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SIO2_TE_v01.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| EC-04-TM | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / 待确认 | TM | 2 | [EC04TM_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_cladUnknow_TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC04TM_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_cladUnknow_TM_v01.gds) | 清单参数仍有待确认字段; 低台阶待处理 / lower step pending |
| EC-05 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiO₂ | TE | 2 | [EC05_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SIO2_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC05_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SIO2_TE_v01.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| EC-06 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 10.4 / SiO₂ | TE | 2 | [EC06_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD10.4um_SIO2_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC06_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD10.4um_SIO2_TE_v01.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| MMI-07 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiO₂ | TE、TM | 3 | [MMI1x2_07_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x2_07_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds) | 已生成 / Generated |
| MMI-08 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiO₂ | TE | 5 | [MMI1x4_08_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_08_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE_v01.gds) | 已生成 / Generated |
| MMI-09 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiO₂ | TE、TM | 5 | [MMI1x4_09_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_09_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds) | 已生成 / Generated |
| MMI-12 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiO₂ | TE | 8 | [MMI4x4_12_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_12_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE_v01.gds) | 已生成 / Generated |
| MMI-13 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiO₂ | TE、TM | 8 | [MMI4x4_13_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_13_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds) | 已生成 / Generated |
| PSR-02 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiO₂ | TE、TM | 3 | [PSR02_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/PSR02_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SIO2_TE-TM_v01.gds) | 已生成 / Generated |
| EC-07 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiON | TE | 2 | [EC07_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SION_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/EC07_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_MFD3.2um_SION_TE_v01.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| MMI-14 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiON | TE、TM | 3 | [MMI1x2_14_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x2_14_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE-TM_v01.gds) | 已生成 / Generated |
| MMI-15 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiON | TE | 5 | [MMI1x4_15_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_15_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE_v01.gds) | 已生成 / Generated |
| MMI-16 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiON | TE、TM | 5 | [MMI1x4_16_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_16_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE-TM_v01.gds) | 已生成 / Generated |
| MMI-17 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiON | TE | 8 | [MMI4x4_17_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_17_Xcut_Yprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE_v01.gds) | 已生成 / Generated |
| MMI-18 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiON | TE、TM | 8 | [MMI4x4_18_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE-TM_v01.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_18_Xcut_Zprop_thickness600nm_etchDepth300nm_sidewallAngle63deg_SION_TE-TM_v01.gds) | 已生成 / Generated |

## 待确认项 / Pending items

- MMI-04 的偏振支持仍待确认；EC-04-TM 的包层仍待确认。 / MMI-04 polarization and EC-04-TM cladding remain unconfirmed.
- 端面耦合器低台阶轮廓尚未导出，不创建或合并至 2/0。 / Edge-coupler lower steps remain deferred.
- 本次保留器件的上表面轮廓、名称、端口坐标、方向、宽度及署名保持不变。 / Retained contours and interfaces are unchanged.
- 原始源工程及旧版备份留在本地，不随公开包分发。

## 工艺总览 / Process overview

[600/300 nm · 63° · 24 devices](../overviews/JNU_MWP_TFLN_PDK_600_300_V1.1.gds)
