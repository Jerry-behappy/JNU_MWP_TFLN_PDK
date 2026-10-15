# -*- coding: utf-8 -*-
# 时间: 2026-10
"""检查公开目录、矩形黑盒、真实库实例及保存重开的接口。"""
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


def roots(layout):
    return [layout.cell(c) if isinstance(c, int) else c for c in layout.each_top_cell()]


def verify():
    forbidden_suffixes = {".fsp", ".h5", ".mat", ".xlsx", ".zip"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        assert path.suffix.lower() not in forbidden_suffixes, "不允许发布原始工程或完整制品: " + str(relative)
        assert not any(part.lower() in ("gds", "evidence", "source_inventory") or "whitebox" in part.lower() for part in relative.parts), relative
        if path.suffix in (".py", ".json", ".md", ".lym", ".lyt", ".ps1", ".xml", ".yml"):
            content = path.read_text(encoding="utf-8")
            assert not re.search(r"[A-Z]:[\\/]", content) and ("::model" + "::") not in content, "存在本地来源路径: " + str(relative)
        if path.suffix == ".py":
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        if path.suffix == ".lym":
            compile(ET.parse(path).getroot().findtext("text"), str(path), "exec")
    assert DATA["edition"] == "public-blackbox"
    assert len(DATA["devices"]) == 12 and sum(len(d["pins"]) for d in DATA["devices"]) == 47
    assert all(d["id"] != "MMI07" for d in DATA["devices"])
    assert len(list(PACKAGE.rglob("*.gds"))) == 16
    assert len(list((PACKAGE / "previews").glob("*.png"))) == 16
    tfln_library.register_all()
    total = 0
    for process, count in zip(tfln_library.PROCESSES, (1, 1, 9, 1)):
        library = pya.Library.library_by_name("JNULib_TFLN_" + process)
        assert library is not None and library.layout().cells() == count
        assert "By Songliang Chen" not in library.description
        layout = pya.Layout()
        layout.dbu = DATA["dbu_um"]
        top = layout.create_cell("PUBLIC_PLACEMENT_" + process)
        records = [d for d in DATA["devices"] if d["process"] == process]
        for i, record in enumerate(records):
            index = layout.add_lib_cell(library, library.layout().cell(record["cell_name"]).cell_index())
            inst = top.insert(pya.CellInstArray(index, pya.Trans(i * 10000000, 0)))
            assert inst.cell.is_library_cell()
            cell = inst.cell
            wave = pya.Region(cell.begin_shapes_rec(layout.layer(1, 0))).merged()
            expected = pya.Box(*[round(v / layout.dbu) for v in record["physical_bbox_um"]])
            assert wave.count() == 1 and (wave ^ pya.Region(expected)).is_empty(), "黑盒泄漏内部图形"
            recs = list(cell.shapes(layout.layer(68, 0)).each())
            assert len(recs) == 1 and recs[0].is_box()
            rec = recs[0].box
            assert rec.left == expected.left and rec.right == expected.right
            assert (wave - pya.Region(rec)).is_empty()
            labels = [s for s in cell.shapes(layout.layer(10, 0)).each() if s.is_text()]
            authors = [s for s in labels if s.text.string == DATA["author"]]
            assert len(authors) == 1 and authors[0].text_valign == int(pya.VAlign.VAlignTop)
            author_box = pya.Box(*[round(v / layout.dbu) for v in record["author_layout"]["envelope_bbox_um"]])
            assert (pya.Region(author_box) - pya.Region(rec)).is_empty()
            assert (pya.Region(author_box) & wave).is_empty()
            paths = [s.path for s in cell.shapes(layout.layer(1, 10)).each() if s.is_path()]
            pins = [s.text for s in cell.shapes(layout.layer(1, 10)).each() if s.is_text()]
            assert len(paths) == len(pins) == len(record["pins"])
            for path, metadata in zip(paths, record["pins"]):
                points = list(path.each_point())
                center = pya.Point((points[0].x + points[1].x) // 2, (points[0].y + points[1].y) // 2)
                assert center == pya.Point(*[round(v / layout.dbu) for v in metadata["center_um"]])
                assert path.width == round(metadata["width_um"] / layout.dbu)
                assert abs(points[1].x - points[0].x) == round(0.02 / layout.dbu)
                assert (points[1].x > points[0].x) == (metadata["direction_deg"] == 0)
                assert any(t.string == metadata["name"] and t.trans.disp == center for t in pins)
            total += len(paths)
        with tempfile.TemporaryDirectory() as temporary:
            target = str(Path(temporary) / "placement.gds")
            options = pya.SaveLayoutOptions()
            options.gds2_max_cellname_length = 256
            layout.write(target, options)
            reopened = pya.Layout()
            reopened.read(target)
            restored = roots(reopened)[0]
            assert sum(1 for _ in restored.each_inst()) == count
            for layer, datatype in ((1, 0), (1, 10), (68, 0)):
                before = pya.Region(top.begin_shapes_rec(layout.layer(layer, datatype)))
                after = pya.Region(restored.begin_shapes_rec(reopened.layer(layer, datatype)))
                assert (before ^ after).is_empty(), "保存重开改变了占位或接口"
    for record in DATA["overviews"]:
        layout = pya.Layout()
        layout.read(str(PACKAGE / record["gds_relative"]))
        assert sum(1 for _ in roots(layout)[0].each_inst()) == record["device_count"]
        for cell in layout.each_cell():
            wave = pya.Region(cell.shapes(layout.layer(1, 0)))
            if not wave.is_empty():
                assert (wave ^ pya.Region(wave.bbox())).is_empty(), "总览包含内部图形"
    # 文档中的相对链接必须指向实际文件，外部 URL 与锚点由 GitHub 处理。
    for document in ROOT.rglob("*.md"):
        text = document.read_text(encoding="utf-8")
        links = re.findall(r'\]\(([^)]+)\)|(?:href|src)="([^"]+)"', text)
        for entries in links:
            target = next(e for e in entries if e)
            if target.startswith(("http:", "https:", "#")):
                continue
            file = target.split("#", 1)[0]
            assert (document.parent / file).exists(), "文档文件链接失效: " + str(document) + " -> " + file
    assert len(pya.Library.library_by_name("JNULib_TFLN_pcell").layout().pcell_names()) == 9
    print("PUBLIC_VERIFY_PASS: fixed libraries (1/1/9/1), 12 rectangles, 47 ports, 9 PCells, instances/save-reopen, 16 GDS; no fixed whitebox source")


if __name__ == "__main__":
    verify()
