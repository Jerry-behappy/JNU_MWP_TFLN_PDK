# -*- coding: utf-8 -*-
# 时间: 2026-10
"""把用户提供的授权 GDS 安装到独立私有目录，不写入公开克隆。"""
import json
import math
import os
import shutil
import tempfile
from pathlib import Path
import pya


def private_root():
    try:
        location = pya.Application.instance().application_data_path()
    except AttributeError:
        location = os.environ.get("KLAYOUT_HOME") or Path.home() / "KLayout"
    return Path(str(location)) / "jnu_private" / "JNU_MWP_TFLN_PDK"


def private_source(record):
    root = private_root()
    try:
        mapping = json.loads((root / "active.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    # 简名发布后继续接受本机已安装的旧名索引，不改写原始授权文件。
    relative = next((mapping[name] for name in
                     [record["cell_name"]] + record.get("legacy_cell_names", []) if mapping.get(name)), None)
    if not relative:
        return None
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise RuntimeError("授权器件索引无效 / Invalid authorized device index")
    return path


def validate_ports(layout, cell, record):
    paths = [s.path for s in cell.shapes(layout.layer(1, 10)).each() if s.is_path()]
    labels = {s.text.string for s in cell.shapes(layout.layer(1, 10)).each() if s.is_text()}
    expected = record["pins"]
    assert len(paths) == len(expected) and labels == {p["name"] for p in expected}, "PinRec 端口数量或名称不匹配"
    actual = set()
    for path in paths:
        points = list(path.each_point())
        assert len(points) == 2 and (points[0].y == points[1].y or points[0].x == points[1].x)
        direction = round(math.degrees(math.atan2(points[1].y - points[0].y, points[1].x - points[0].x))) % 360
        actual.add(((points[0].x + points[1].x) // 2, (points[0].y + points[1].y) // 2,
                    path.width, direction))
    wanted = {(*[round(v / layout.dbu) for v in pin["center_um"]], round(pin["width_um"] / layout.dbu), pin["direction_deg"]) for pin in expected}
    assert actual == wanted, "PinRec 坐标、宽度或朝向不匹配"


def install_directory(directory, records):
    directory = Path(directory).resolve()
    by_name = {name: r for r in records for name in
               [r["cell_name"]] + r.get("legacy_cell_names", [])}
    accepted = {}
    for path in directory.rglob("*.gds"):
        layout = pya.Layout()
        layout.read(str(path))
        tops = list(layout.each_top_cell())
        if len(tops) != 1:
            continue
        cell = layout.cell(tops[0]) if isinstance(tops[0], int) else tops[0]
        if cell.name not in by_name:
            continue
        record = by_name[cell.name]
        name = record["cell_name"]
        assert name not in accepted, "同一器件存在多个候选文件: " + name
        assert not pya.Region(cell.begin_shapes_rec(layout.layer(1, 0))).is_empty()
        validate_ports(layout, cell, record)
        accepted[name] = path
    if not accepted:
        raise RuntimeError("未找到与当前名称和端口相符的器件 GDS / No matching device GDS found")
    root = private_root()
    root.mkdir(parents=True, exist_ok=True)
    # 每次安装使用新目录；旧版本和原始文件始终保留。
    destination = Path(tempfile.mkdtemp(prefix="library_", dir=str(root)))
    current = root / "active.json"
    previous = json.loads(current.read_text(encoding="utf-8")) if current.exists() else {}
    for name, source in accepted.items():
        target = destination / (name + ".gds")
        layout = pya.Layout()
        layout.read(str(source))
        tops = list(layout.each_top_cell())
        cell = layout.cell(tops[0]) if isinstance(tops[0], int) else tops[0]
        if cell.name == name:
            shutil.copy2(source, target)
        else:
            # 仅在新的安装副本内统一顶层名，来源文件和旧版本保持原样。
            cell.name = name
            options = pya.SaveLayoutOptions()
            options.gds2_max_cellname_length = 256
            layout.write(str(target), options)
        previous[name] = target.relative_to(root).as_posix()
    temporary = root / "active.tmp.json"
    temporary.write_text(json.dumps(previous, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(current)
    return len(accepted)


def install_whitebox_dialog():
    directory = pya.QFileDialog.getExistingDirectory(pya.Application.instance().main_window(),
        "选择授权 TFLN GDS 文件夹 / Select authorized TFLN GDS folder", "")
    if not directory:
        return
    from .actions import manifest, reload_pdk
    count = install_directory(str(directory), manifest()["devices"])
    reload_pdk()
    pya.MessageBox.info("TFLN 白盒器件库 / Whitebox Library",
        "已安装 %d 个器件，原始文件和旧版本已保留。\nInstalled %d devices; original files and previous versions retained." % (count, count), pya.MessageBox.Ok)
