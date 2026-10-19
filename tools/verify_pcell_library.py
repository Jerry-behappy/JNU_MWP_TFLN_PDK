# -*- coding: utf-8 -*-
# 时间: 2026-10
"""验证独立安装的公开 PCell 声明、几何、端口、参数编辑和保存重开。"""
import json
import sys
import tempfile
from pathlib import Path
import pya

ROOT = Path(globals().get("pdk_root", Path(__file__).resolve().parents[1] / "salt/JNU_MWP_TFLN_PDK")).resolve()
sys.path.insert(0, str(ROOT / "pymacros"))
import tfln_library
from tfln_pcell_library import FACTORIES, LIBRARY_NAME


def verify():
    import tfln_pcells
    assert all(hasattr(tfln_pcells, name) for name in tfln_pcells.__all__)
    libraries = tfln_library.register_all()
    assert len(libraries) == len(tfln_library.PROCESSES) + 1
    library = pya.Library.library_by_name(LIBRARY_NAME)
    assert library is not None
    assert list(library.layout().pcell_names()) == sorted(name for name, _ in FACTORIES)
    assert not any(n == "JNU_MWP_pcells" or n == "JNU_MWP_tools" for n in sys.modules), "运行时依赖 SOI 安装"
    layout = pya.Layout()
    layout.dbu = 0.0001
    top = layout.create_cell("TFLN_PCELL_VERIFICATION")
    rows = []
    cells = []
    for index, (name, _) in enumerate(FACTORIES):
        cell = layout.create_cell(name, LIBRARY_NAME, {})
        assert cell is not None and cell.is_pcell_variant() and cell.is_library_cell(), name
        wave = pya.Region(cell.begin_shapes_rec(layout.layer(1, 0))).merged()
        assert not wave.is_empty(), "PCell 生成空图形: " + name
        assert not pya.Region(cell.begin_shapes_rec(layout.layer(68, 0))).is_empty(), name
        pins = [s for s in cell.shapes(layout.layer(1, 10)).each() if s.is_path()]
        labels = [s.text.string for s in cell.shapes(layout.layer(1, 10)).each() if s.is_text()]
        assert len(pins) >= 2 and len(pins) == len(labels), name
        for pin in pins:
            assert abs(pin.path.length() * layout.dbu - 0.02) <= layout.dbu, name
            assert not (wave & pya.Region(pin.path.polygon())).is_empty(), name
        top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans((index % 3) * 30000000, -(index // 3) * 30000000)))
        cells.append(cell)
        rows.append({"pcell": name, "pins": len(pins), "parameters": len(cell.pcell_parameters_by_name())})
    # 参数变化必须进入真实 PCell 变体并改变几何，而不是固定图形拷贝。
    edited = layout.create_cell("Pcell_Straight_Waveguide", LIBRARY_NAME, {"length": 137.0, "width": 1.2})
    params = edited.pcell_parameters_by_name()
    # 采用声明实际字段，兼容其参数名使用 wg_width 的版本。
    if "wg_width" in params:
        edited = layout.create_cell("Pcell_Straight_Waveguide", LIBRARY_NAME, {"length": 137.0, "wg_width": 1.2})
    box = pya.Region(edited.begin_shapes_rec(layout.layer(1, 0))).bbox()
    assert abs(box.width() * layout.dbu - 137.0) <= layout.dbu
    assert abs(box.height() * layout.dbu - 1.2) <= layout.dbu
    top.insert(pya.CellInstArray(edited.cell_index(), pya.Trans(0, -100000000)))
    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary) / "pcells.gds"
        options = pya.SaveLayoutOptions()
        options.gds2_max_cellname_length = 256
        options.gds2_max_vertex_count = 2000
        options.gds2_write_cell_properties = True
        options.gds2_write_file_properties = True
        layout.write(str(target), options)
        reopened = pya.Layout()
        reopened.read(str(target))
        restored = reopened.cell(top.name)
        assert sum(1 for _ in restored.each_inst()) == 10
        for instance in restored.each_inst():
            assert instance.cell.is_pcell_variant() and instance.cell.is_library_cell(), "保存重开丢失 PCell 身份"
        for layer, datatype in ((1, 0), (1, 10), (68, 0)):
            before = pya.Region(top.begin_shapes_rec(layout.layer(layer, datatype)))
            after = pya.Region(restored.begin_shapes_rec(reopened.layer(layer, datatype)))
            assert (before ^ after).is_empty(), "保存重开改变几何或接口"
        # 同名重载后客户布局实例保持有效。
        tfln_library.register_all(force_reload=True)
        assert sum(1 for _ in top.each_inst()) == 10
        assert all(not pya.Region(i.cell.begin_shapes_rec(layout.layer(1, 0))).is_empty() for i in top.each_inst())
    print("PCELL_VERIFY_PASS: 9 declarations, independent imports, ports, parameter edits, native save/reopen and reload")
    print(json.dumps(rows, ensure_ascii=False))


if __name__ == "__main__":
    verify()
