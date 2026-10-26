# -*- coding: utf-8 -*-
# 时间: 2026-10
"""验证清单对应库、黑盒主体、四向端口、保存重开及公开来源边界。"""
import json
import re
import sys
import tempfile
from pathlib import Path
from xml.etree import ElementTree as ET
import pya

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "salt/JNU_MWP_TFLN_PDK"
DATA = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
sys.path.insert(0, str(PACKAGE / "pymacros"))
import tfln_library
from tfln_tools.authorized_gds import validate_ports


def top_cell(layout):
    item = list(layout.each_top_cell())[0]
    return layout.cell(item) if isinstance(item, int) else item


def expected_stubs(record, dbu):
    output = pya.Region()
    length = round(0.2 / dbu)
    for pin in record["pins"]:
        x, y = [round(v / dbu) for v in pin["center_um"]]
        width = round(pin["width_um"] / dbu)
        low, high = width // 2, width - width // 2
        box = {180: (x, y - low, x + length, y + high), 0: (x - length, y - low, x, y + high),
               270: (x - low, y, x + high, y + length), 90: (x - low, y - length, x + high, y)}[pin["direction_deg"]]
        output.insert(pya.Box(*box))
    return output.merged()


def verify():
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        if path.name.lower().startswith("readme") and path.suffix.lower() in (".md", ".markdown", ".rst", ".txt", ""):
            readme = path.read_text(encoding="utf-8")
            assert not re.search(r"预览|\bpreviews?\b|By\s+Songliang\s+Chen", readme, re.IGNORECASE), "README 内容违反展示规则: " + str(relative)
        assert path.suffix.lower() not in {".fsp", ".h5", ".mat", ".xlsx", ".zip"}, relative
        assert not any(part.lower() in ("gds", "evidence", "source_inventory") or "whitebox" in part.lower() for part in relative.parts), relative
        if path.suffix in (".py", ".json", ".md", ".lym", ".lyt", ".ps1", ".xml", ".yml"):
            content = path.read_text(encoding="utf-8")
            assert not re.search(r"[A-Z]:[\\/]", content) and ("::model" + "::") not in content, relative
        if path.suffix == ".py":
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        if path.suffix == ".lym":
            compile(ET.parse(path).getroot().findtext("text"), str(path), "exec")
    assert DATA["edition"] == "public-blackbox" and DATA["version"] == "V1.1"
    style = next(p for p in ET.parse(PACKAGE / "layers.lyp").getroot().findall("properties")
                 if p.findtext("source") == "998/0@*")
    assert style.findtext("frame-color") == style.findtext("fill-color") == "#ffae00"
    assert style.findtext("dither-pattern") == "I5" and style.findtext("transparent") == "false"
    counts = {"600_300": 24}
    assert DATA["processes"] == ["600_300"]
    assert DATA["process_scope"] == dict(film_thickness_nm=600, etch_depth_nm=300, sidewall_angle_deg=63)
    assert all(tuple(d["parameters"].get(k) for k in ("film_thickness_nm", "etch_depth_nm", "sidewall_angle_deg")) == (600, 300, 63) for d in DATA["devices"])
    assert len(DATA["devices"]) == 24 and sum(len(d["pins"]) for d in DATA["devices"]) == 108
    assert len(list(PACKAGE.rglob("*.gds"))) == 25
    assert len(list((PACKAGE / "previews").glob("*.png"))) == 25
    assert len({d["cell_name"] for d in DATA["devices"]}) == 24
    expected_files = {d["gds_relative"] for d in DATA["devices"] + DATA["overviews"]}
    assert {p.relative_to(PACKAGE).as_posix() for p in PACKAGE.rglob("*.gds")} == expected_files
    tfln_library.register_all()
    for process, count in counts.items():
        records = [d for d in DATA["devices"] if d["process"] == process]
        assert len(records) == count
        library = pya.Library.library_by_name("JNULib_TFLN_" + process, tfln_library.TECHNOLOGY_NAME)
        assert library is not None and sum(1 for _ in library.layout().each_top_cell()) == count
        assert "By Songliang Chen" not in library.description
        layout = pya.Layout()
        layout.dbu = DATA["dbu_um"]
        layout.technology_name = tfln_library.TECHNOLOGY_NAME
        top = layout.create_cell("PUBLIC_PLACEMENT_" + process)
        for i, record in enumerate(records):
            assert record["cell_name"].isascii() and len(record["cell_name"]) <= 256
            index = layout.add_lib_cell(library, library.layout().cell(record["cell_name"]).cell_index())
            instance = top.insert(pya.CellInstArray(index, pya.Trans(i % 4, bool(i % 2), i * 10000000, 0)))
            assert instance.cell.is_library_cell()
            cell = instance.cell
            body = pya.Region(cell.begin_shapes_rec(layout.layer(998, 0))).merged()
            expected = pya.Box(*[round(v / layout.dbu) for v in record["blackbox_body_bbox_um"]])
            assert body.count() == 1 and body.bbox() == expected, record["id"]
            physical = pya.Region(cell.begin_shapes_rec(layout.layer(1, 0))).merged()
            assert (physical ^ expected_stubs(record, layout.dbu)).is_empty(), "公开黑盒包含非端口制造轮廓: " + record["id"]
            assert (physical & body).is_empty(), record["id"]
            for stub in expected_stubs(record, layout.dbu).each():
                assert (body + pya.Region(stub)).merged().count() == 1, "端口直段悬空: " + record["id"]
            label_region = pya.Region(cell.begin_shapes_rec(layout.layer(10, 0)))
            label_box = label_region.bbox()
            target = pya.Box(*[round(v / layout.dbu) for v in record["blackbox_label_box_um"]])
            placeholder = pya.Region(target)
            for pin in record["pins"]:
                x, y = [round(v / layout.dbu) for v in pin["center_um"]]
                width = round(pin["width_um"] / layout.dbu)
                lo, hi, length = width // 2, width - width // 2, round(0.2 / layout.dbu)
                direction = pin["direction_deg"]
                if direction == 0 and x - length > target.right:
                    placeholder.insert(pya.Box(target.right, y - lo, x - length, y + hi))
                elif direction == 180 and x + length < target.left:
                    placeholder.insert(pya.Box(x + length, y - lo, target.left, y + hi))
                elif direction == 90 and y - length > target.top:
                    placeholder.insert(pya.Box(x - lo, target.top, x + hi, y - length))
                elif direction == 270 and y + length < target.bottom:
                    placeholder.insert(pya.Box(x - lo, y + length, x + hi, target.bottom))
            assert (placeholder ^ body).is_empty(), "占位主体含非接口轮廓: " + record["id"]
            assert not label_region.is_empty() and (label_region - pya.Region(target)).is_empty()
            assert abs(label_box.center().x - target.center().x) <= 1
            assert abs(label_box.center().y - target.center().y) <= 1
            rec = pya.Region(cell.begin_shapes_rec(layout.layer(68, 0)))
            assert rec.count() == 1 and (physical - rec).is_empty() and (body - rec).is_empty()
            validate_ports(layout, cell, record)
            labels = [shape for shape in cell.shapes(layout.layer(10, 0)).each() if shape.is_text()]
            assert sum(shape.text.string == DATA["author"] for shape in labels) == 1
            envelope = pya.Region(pya.Box(*[round(v / layout.dbu) for v in record["author_layout"]["envelope_bbox_um"]]))
            assert (envelope - rec).is_empty() and (envelope & body).is_empty()
            assert pya.Region(cell.begin_shapes_rec(layout.layer(2, 0))).is_empty()
        with tempfile.TemporaryDirectory() as temporary:
            target = str(Path(temporary) / "placement.gds")
            options = pya.SaveLayoutOptions()
            options.gds2_max_cellname_length = 256
            layout.write(target, options)
            reopened = pya.Layout()
            reopened.read(target)
            restored = top_cell(reopened)
            assert sum(1 for _ in restored.each_inst()) == count
            for layer, datatype in ((1, 0), (998, 0), (1, 10), (68, 0)):
                before = pya.Region(top.begin_shapes_rec(layout.layer(layer, datatype)))
                after = pya.Region(restored.begin_shapes_rec(reopened.layer(layer, datatype)))
                assert (before ^ after).is_empty(), "变换或保存重开改变接口"
    for record in DATA["overviews"]:
        layout = pya.Layout()
        layout.read(str(PACKAGE / record["gds_relative"]))
        assert sum(1 for _ in top_cell(layout).each_inst()) == record["device_count"]
    for document in ROOT.rglob("*.md"):
        links = re.findall(r'\]\(([^)]+)\)|(?:href|src)="([^"]+)"', document.read_text(encoding="utf-8"))
        for entries in links:
            target = next(e for e in entries if e)
            if target.startswith(("http:", "https:", "#")):
                continue
            assert (document.parent / target.split("#", 1)[0]).exists(), (document, target)
    assert len(pya.Library.library_by_name("JNULib_TFLN_pcell", tfln_library.TECHNOLOGY_NAME).layout().pcell_names()) == 9
    print("PUBLIC_VERIFY_PASS: 24 fixed devices, 108 optical ports, 600/300 nm and 63 deg only; 9 PCells; no internal contours")


if __name__ == "__main__":
    verify()
