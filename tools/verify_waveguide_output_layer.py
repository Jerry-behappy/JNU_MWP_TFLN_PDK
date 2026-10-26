# -*- coding: utf-8 -*-
# 时间: 2026-10
"""验证输出层进入真实 PCell、variant 身份和 GDS 恢复属性。"""
import json
import sys
import tempfile
from pathlib import Path
import pya

PACKAGE = Path(__file__).resolve().parents[1] / "salt/JNU_MWP_TFLN_PDK"
sys.path.insert(0, str(PACKAGE / "pymacros"))
from tfln_layout_tools.actions import path_to_waveguide as tool
from tfln_layout_tools.actions import waveguide_to_path as reverse
from tfln_pcell_core.internal_waveguide_registry import ensure_internal_waveguide_pcells
from tfln_pcell_core.common import RAW_PATH_PROPERTY


def verify():
    with tempfile.TemporaryDirectory() as temporary:
        settings_file = str(Path(temporary) / "settings.json")
        original_file = tool._waveguide_params_file
        tool._waveguide_params_file = lambda: settings_file
        try:
            old = tool._default_waveguide_params()
            old.pop("waveguide_layer")
            tool._save_waveguide_params(old)
            assert tool._load_waveguide_params()["waveguide_layer"] == "1/0"
            saved = tool._load_waveguide_params()
            saved["waveguide_layer"] = "42/7"
            saved, preset, _created = tool._add_user_preset(saved, tool.TAB_SINGLE, saved["single"])
            assert "waveguide_layer" not in preset["params"]
            tool._save_waveguide_params(saved)
            assert tool._load_waveguide_params()["waveguide_layer"] == "42/7"
            for invalid in ("1", "-1/0", "65536/0", "1/0/2"):
                try:
                    tool._parse_waveguide_layer(invalid)
                except ValueError:
                    pass
                else:
                    raise AssertionError(invalid)

            layout = pya.Layout()
            layout.dbu = 0.0001
            # 热更新遇到旧声明时必须补齐图层参数，而非静默退回默认层。
            class LegacyWaveguide(pya.PCellDeclarationHelper):
                def __init__(self):
                    super().__init__()
                    self.param("width", self.TypeDouble, "Width", default=0.5)

            old_id = layout.register_pcell("TFLN_Waveguide", LegacyWaveguide())
            declaration, new_id = tool._ensure_local_waveguide_pcell(layout, "TFLN_Waveguide")
            assert old_id == new_id
            assert "waveguide_layer" in {p.name for p in declaration.get_parameters()}
            top = layout.create_cell("OUTPUT_LAYERS")
            path = pya.DPath([pya.DPoint(0, 0), pya.DPoint(200, 0), pya.DPoint(200, 200)], 0.5)
            variants = []
            for mode, layer in ((tool.TAB_SINGLE, "4/0"), (tool.TAB_COMPOSITE, "5/0"), (tool.TAB_SINGLE, "42/7")):
                params = tool._result_from_editable_params(mode, saved[mode], layout.dbu)
                baseline = tool._create_waveguide_cell(layout, path, params, 1)
                params["waveguide_layer"] = layer
                cell = tool._create_waveguide_cell(layout, path, params, 2)
                again = tool._create_waveguide_cell(layout, path, params, 3)
                info = tool._parse_waveguide_layer(layer)
                assert cell.cell_index() != baseline.cell_index()
                assert cell.cell_index() == again.cell_index()
                assert cell.pcell_parameters_by_name()["waveguide_layer"] == info
                geometry = pya.Region(cell.begin_shapes_rec(layout.layer(info)))
                assert not geometry.is_empty()
                assert (geometry ^ pya.Region(baseline.begin_shapes_rec(layout.layer(1, 0)))).is_empty()
                assert cell.shapes(layout.layer(1, 0)).is_empty()
                assert sum(1 for s in cell.shapes(layout.layer(1, 10)).each() if s.is_path()) == 2
                assert not cell.shapes(layout.layer(68, 0)).is_empty()
                assert cell.shapes(layout.layer(1, 99)).is_empty()
                assert reverse._waveguide_output_layer(cell) == info
                assert json.loads(str(cell.property(RAW_PATH_PROPERTY)))["waveguide_layer"] == layer
                assert reverse._path_from_waveguide_cell(cell, layout) is not None
                top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans(len(variants) * 3000000, 0)))
                variants.append(cell)

            output = str(Path(temporary) / "layers.gds")
            options = pya.SaveLayoutOptions()
            options.gds2_max_cellname_length = 256
            options.gds2_write_cell_properties = True
            layout.write(output, options)
            restored = pya.Layout()
            ensure_internal_waveguide_pcells(restored)
            restored.read(output)
            for cell in variants:
                info = cell.pcell_parameters_by_name()["waveguide_layer"]
                other = restored.cell(cell.name)
                assert other is not None and other.is_pcell_variant()
                assert other.pcell_parameters_by_name()["waveguide_layer"] == info
                assert (pya.Region(cell.begin_shapes_rec(layout.layer(info))) ^ pya.Region(other.begin_shapes_rec(restored.layer(info)))).is_empty()
                assert reverse._waveguide_output_layer(other) == info

            # 丢失 PCell 声明的缓存图形也能从无图形属性找回输出层。
            flat = pya.Layout()
            flat.dbu = layout.dbu
            cached = flat.create_cell("CACHED")
            cached.copy_tree(variants[-1])
            # copy_tree 仅复制图形；显式模拟 GDS 缓存携带的数字属性。
            from tfln_pcell_core.common import RAW_PATH_GDS_PROPERTY
            cached.set_property(RAW_PATH_GDS_PROPERTY, variants[-1].property(RAW_PATH_PROPERTY))
            assert not cached.is_pcell_variant()
            assert reverse._waveguide_output_layer(cached) == pya.LayerInfo(42, 7)
            empty = flat.create_cell("LEGACY_WITHOUT_LAYER")
            assert reverse._waveguide_output_layer(empty) == pya.LayerInfo(1, 0)
        finally:
            tool._waveguide_params_file = original_file
    print("WAVEGUIDE_OUTPUT_LAYER_PASS: single/composite geometry, custom layers, variant reuse, settings migration, GDS reopen and cached recovery")


if __name__ == "__main__":
    verify()
