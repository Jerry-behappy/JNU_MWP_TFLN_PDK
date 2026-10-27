# 器件参数与文件索引 / Device index

2026-10-27 · 600/300 nm · 63°

固定器件仅保留膜厚 600 nm、刻蚀深度 300 nm、实际侧壁角 63° 的 24 个器件，共 108 个光学端口。角度依据 sidewall_angle_deg，不按目录标称值代替。
Only 600 nm film / 300 nm etch / actual 63° sidewall designs are retained: 24 fixed devices, 108 optical ports. Independent TE/TM designs remain separate records.

器件名与 GDS 文件名保留器件类型、晶向、传播方向、MFD、包层和偏振；省略膜厚、刻蚀、侧壁角、版本及流水编号。工艺参数和追溯编号见下表；三款同参数 SiO₂ 端面耦合器按实际长度 L120um、L130um、L48.9647um 区分。九个独立 PCell 不参与固定工艺记录筛选。

| 编号 / ID | Library | 晶向/传播 | 厚度/刻蚀 nm | 侧壁角 ° | MFD µm / 包层 | 偏振 | 端口 | GDS | 状态 |
|---|---|---|---:|---:|---|---|---:|---|---|
| EC-01 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / AIR | TE | 2 | [EC_Xcut_Yprop_MFD3.2um_AIR_TE.gds](../pymacros/tfln_blackbox_gds/600_300/EC_Xcut_Yprop_MFD3.2um_AIR_TE.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| MMI-01 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE、TM | 3 | [MMI1x2_Xcut_Yprop_AIR_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x2_Xcut_Yprop_AIR_TE-TM.gds) | 已生成 / Generated |
| MMI-02 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE | 5 | [MMI1x4_Xcut_Yprop_AIR_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Yprop_AIR_TE.gds) | 已生成 / Generated |
| MMI-03 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / AIR | TE | 5 | [MMI1x4_Xcut_Zprop_AIR_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Zprop_AIR_TE.gds) | 已生成 / Generated |
| MMI-04 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE、TM（待确认） | 4 | [MMI2x2_Xcut_Yprop_AIR_polUnknow.gds](../pymacros/tfln_blackbox_gds/600_300/MMI2x2_Xcut_Yprop_AIR_polUnknow.gds) | 清单参数仍有待确认字段 |
| MMI-05 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / AIR | TE | 8 | [MMI4x4_Xcut_Yprop_AIR_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Yprop_AIR_TE.gds) | 已生成 / Generated |
| MMI-06 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / AIR | TE、TM | 8 | [MMI4x4_Xcut_Zprop_AIR_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Zprop_AIR_TE-TM.gds) | 已生成 / Generated |
| EC-03 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiO₂ | TE | 2 | [EC_L120um_Xcut_Yprop_MFD3.2um_SIO2_TE.gds](../pymacros/tfln_blackbox_gds/600_300/EC_L120um_Xcut_Yprop_MFD3.2um_SIO2_TE.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| EC-04 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiO₂ | TE | 2 | [EC_L130um_Xcut_Yprop_MFD3.2um_SIO2_TE.gds](../pymacros/tfln_blackbox_gds/600_300/EC_L130um_Xcut_Yprop_MFD3.2um_SIO2_TE.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| EC-04-TM | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / 待确认 | TM | 2 | [EC_Xcut_Yprop_MFD3.2um_cladUnknow_TM.gds](../pymacros/tfln_blackbox_gds/600_300/EC_Xcut_Yprop_MFD3.2um_cladUnknow_TM.gds) | 清单参数仍有待确认字段; 低台阶待处理 / lower step pending |
| EC-05 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiO₂ | TE | 2 | [EC_L48.9647um_Xcut_Yprop_MFD3.2um_SIO2_TE.gds](../pymacros/tfln_blackbox_gds/600_300/EC_L48.9647um_Xcut_Yprop_MFD3.2um_SIO2_TE.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| EC-06 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 10.4 / SiO₂ | TE | 2 | [EC_Xcut_Yprop_MFD10.4um_SIO2_TE.gds](../pymacros/tfln_blackbox_gds/600_300/EC_Xcut_Yprop_MFD10.4um_SIO2_TE.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| MMI-07 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiO₂ | TE、TM | 3 | [MMI1x2_Xcut_Yprop_SIO2_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x2_Xcut_Yprop_SIO2_TE-TM.gds) | 已生成 / Generated |
| MMI-08 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiO₂ | TE | 5 | [MMI1x4_Xcut_Yprop_SIO2_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Yprop_SIO2_TE.gds) | 已生成 / Generated |
| MMI-09 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiO₂ | TE、TM | 5 | [MMI1x4_Xcut_Zprop_SIO2_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Zprop_SIO2_TE-TM.gds) | 已生成 / Generated |
| MMI-12 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiO₂ | TE | 8 | [MMI4x4_Xcut_Yprop_SIO2_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Yprop_SIO2_TE.gds) | 已生成 / Generated |
| MMI-13 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiO₂ | TE、TM | 8 | [MMI4x4_Xcut_Zprop_SIO2_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Zprop_SIO2_TE-TM.gds) | 已生成 / Generated |
| PSR-02 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiO₂ | TE、TM | 3 | [PSR_Xcut_Zprop_SIO2_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/PSR_Xcut_Zprop_SIO2_TE-TM.gds) | 已生成 / Generated |
| EC-07 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | 3.2 / SiON | TE | 2 | [EC_Xcut_Yprop_MFD3.2um_SION_TE.gds](../pymacros/tfln_blackbox_gds/600_300/EC_Xcut_Yprop_MFD3.2um_SION_TE.gds) | 已生成 / Generated; 低台阶待处理 / lower step pending |
| MMI-14 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiON | TE、TM | 3 | [MMI1x2_Xcut_Yprop_SION_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x2_Xcut_Yprop_SION_TE-TM.gds) | 已生成 / Generated |
| MMI-15 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiON | TE | 5 | [MMI1x4_Xcut_Yprop_SION_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Yprop_SION_TE.gds) | 已生成 / Generated |
| MMI-16 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiON | TE、TM | 5 | [MMI1x4_Xcut_Zprop_SION_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI1x4_Xcut_Zprop_SION_TE-TM.gds) | 已生成 / Generated |
| MMI-17 | `JNULib_TFLN_600_300` | x切/y传 | 600/300 | 63 | — / SiON | TE | 8 | [MMI4x4_Xcut_Yprop_SION_TE.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Yprop_SION_TE.gds) | 已生成 / Generated |
| MMI-18 | `JNULib_TFLN_600_300` | x切/z传 | 600/300 | 63 | — / SiON | TE、TM | 8 | [MMI4x4_Xcut_Zprop_SION_TE-TM.gds](../pymacros/tfln_blackbox_gds/600_300/MMI4x4_Xcut_Zprop_SION_TE-TM.gds) | 已生成 / Generated |

## 待确认项 / Pending items

- MMI-04 的偏振支持仍待确认；EC-04-TM 的包层仍待确认。 / MMI-04 polarization and EC-04-TM cladding remain unconfirmed.
- 端面耦合器低台阶轮廓尚未导出，不创建或合并至 2/0。 / Edge-coupler lower steps remain deferred.
- 本次保留器件的上表面轮廓、名称、端口坐标、方向、宽度及署名保持不变。 / Retained contours and interfaces are unchanged.
- 原始源工程及旧版备份留在本地，不随公开包分发。

## 工艺总览 / Process overview

[600/300 nm · 63° · 24 devices](../overviews/JNU_MWP_TFLN_PDK_600_300_V1.1.gds)
