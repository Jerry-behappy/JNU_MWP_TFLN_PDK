# -*- coding: utf-8 -*-
# 时间: 2026-10
"""验证独立黑盒库、技术筛选和旧会话库关联迁移。"""
import json
import sys
from pathlib import Path
import pya

ROOT = Path(globals().get("pdk_root", Path(__file__).resolve().parents[1] / "salt/JNU_MWP_TFLN_PDK")).resolve()
sys.path.insert(0, str(ROOT / "pymacros"))
import tfln_library


def verify():
    data = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
    libraries = tfln_library.register_all()
    names = ["JNULib_TFLN_" + p for p in data["processes"]] + [tfln_library.BLACKBOX_LIBRARY_NAME, "JNULib_TFLN_pcell"]
    assert data["processes"] == ["600_300"]
    assert len(libraries) == len(names) == 3
    for retired in ("300_125", "300_300", "400_200", "600_600"):
        assert pya.Library.library_by_name("JNULib_TFLN_" + retired, tfln_library.TECHNOLOGY_NAME) is None
    for library in libraries:
        assert library.technologies() == [tfln_library.TECHNOLOGY_NAME]
        assert library.is_for_technology(tfln_library.TECHNOLOGY_NAME)
        for other in ("", "JNU_MWP_SOI_PDK", "GSiP", "EBeam"):
            assert not library.is_for_technology(other)
            assert pya.Library.library_by_name(library.name(), other) is None
    blackbox = pya.Library.library_by_name(tfln_library.BLACKBOX_LIBRARY_NAME, tfln_library.TECHNOLOGY_NAME)
    assert "黑盒库 / Blackbox Library" in blackbox.description
    assert sum(1 for _ in blackbox.layout().each_top_cell()) == len(data["devices"]) == 24
    placed = pya.Layout()
    placed.dbu = data["dbu_um"]
    placed.technology_name = tfln_library.TECHNOLOGY_NAME
    top = placed.create_cell("BLACKBOX_LIBRARY_TEST")
    for i, record in enumerate(data["devices"]):
        cell = placed.create_cell(record["cell_name"], tfln_library.BLACKBOX_LIBRARY_NAME)
        assert cell is not None and cell.is_library_cell()
        top.insert(pya.CellInstArray(cell.cell_index(), pya.Trans(i * 10000000, 0)))
        source = pya.Layout()
        path = ROOT / "pymacros/tfln_blackbox_gds" / record["process"] / (record["cell_name"] + ".gds")
        source.read(str(path))
        for layer, datatype in ((1, 0), (998, 0), (1, 10), (68, 0), (10, 0)):
            expected = pya.Region(source.top_cell().begin_shapes_rec(source.layer(layer, datatype)))
            actual = pya.Region(cell.begin_shapes_rec(placed.layer(layer, datatype)))
            assert (actual ^ expected).is_empty(), (record["id"], layer)
    # 重载前的全局注册库也应在普通幂等注册时迁移到 TFLN 技术。
    for library in libraries:
        library.clear_technologies()
    migrated = tfln_library.register_all()
    assert len(migrated) == 3 and all(l.technologies() == [tfln_library.TECHNOLOGY_NAME] for l in migrated)
    print("LIBRARY_SCOPE_PASS: three TFLN-only libraries; 24 unchanged blackboxes; unsupported process libraries absent")


if __name__ == "__main__":
    verify()
