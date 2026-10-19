# -*- coding: utf-8 -*-
# 时间: 2026-10
"""TFLN 版图、器件库及只读参数菜单动作。"""
import json
import sys
from pathlib import Path
import pya
from tfln_library import PDK_ROOT, TECHNOLOGY_NAME, register_all, load_technology
_RELOAD_TIMER = globals().get("_RELOAD_TIMER")


def value(obj, name):
    v = getattr(obj, name)
    return v() if callable(v) else v


def manifest():
    return json.loads((PDK_ROOT / "manifest.json").read_text(encoding="utf-8"))


def layer_map(layout):
    # Si 别名用于 SiEPIC 通用识别；实体仍是 TFLN Waveguide 1/0。
    return {"technology_name": TECHNOLOGY_NAME, "dbu": layout.dbu,
            **{n: pya.LayerInfo(l, d) for n, l, d in (("Waveguide", 1, 0), ("Si", 1, 0),
             ("SiO2_Open", 3, 0), ("NiCr", 4, 0), ("Au", 5, 0), ("Dicing", 7, 0),
             ("Text", 10, 0), ("PinRec", 1, 10), ("DevRec", 68, 0), ("PinRecM", 1, 11), ("FbrTgt", 81, 0))}}


def context():
    view = pya.Application.instance().main_window().current_view()
    if view is None or not view.active_cellview().is_valid():
        raise RuntimeError("请先打开或新建 TFLN 版图。")
    cv = view.active_cellview()
    if cv.cell is None:
        raise RuntimeError("请先选择顶层 Cell。")
    return view, cv, cv.layout(), cv.cell


def apply_style(view=None):
    load_technology()
    view = view or context()[0]
    cv = view.active_cellview()
    cv.technology = TECHNOLOGY_NAME
    cv.layout().TECHNOLOGY = layer_map(cv.layout())
    view.load_layer_props(str(PDK_ROOT / "layers.lyp"))


def new_layout():
    load_technology()
    window = pya.Application.instance().main_window()
    cv = window.create_layout(TECHNOLOGY_NAME, 1)
    layout = cv.layout()
    layout.dbu = 0.0001
    cv.cell = layout.create_cell("TFLN_TOP")
    view = window.current_view()
    apply_style(view)
    view.zoom_fit()
    return view


def open_overview(process):
    record = next(o for o in manifest()["overviews"] if o["process"] == process)
    load_technology()
    window = pya.Application.instance().main_window()
    cv = window.load_layout(str(PDK_ROOT / record["gds_relative"]), TECHNOLOGY_NAME, 1)
    view = window.current_view()
    apply_style(view)
    view.max_hier()
    view.zoom_fit()
    return cv


def insert_into(layout, cell, record, x=0.0, y=0.0):
    register_all()
    library = pya.Library.library_by_name("JNULib_TFLN_" + record["process"])
    source = library.layout().cell(record["cell_name"])
    index = layout.add_lib_cell(library, source.cell_index())
    return cell.insert(pya.CellInstArray(index, pya.Trans(round(x / layout.dbu), round(y / layout.dbu))))


def placement_dialog():
    window = pya.Application.instance().main_window()
    dialog = pya.QDialog(window)
    dialog.setWindowTitle("插入 TFLN 器件 / Insert TFLN Device")
    dialog.resize(800, 300)
    form = pya.QVBoxLayout(dialog)
    combo = pya.QComboBox(dialog)
    records = manifest()["devices"]
    for r in records:
        combo.addItem(r["id"] + " | " + r["process"] + " | " + r["cell_name"].split("_")[0])
    form.addWidget(combo)
    details = pya.QLabel(dialog)
    details.wordWrap = True
    form.addWidget(details)
    def update_details(*args):
        r = records[value(combo, "currentIndex")]
        details.setText(r["cell_name"] + "\n" + r["geometry_status"] + "；光学端口 " + str(len(r["pins"])))
    combo.currentIndexChanged(update_details)
    update_details()
    edits = []
    for name in ("X (µm)", "Y (µm)"):
        row = pya.QHBoxLayout()
        row.addWidget(pya.QLabel(name, dialog))
        edit = pya.QLineEdit("0", dialog)
        row.addWidget(edit)
        form.addLayout(row)
        edits.append(edit)
    form.addWidget(pya.QLabel("端口与识别层随实例放置；实例可继续用 KLayout 旋转、镜像。", dialog))
    buttons = pya.QHBoxLayout()
    ok, cancel = pya.QPushButton("OK", dialog), pya.QPushButton("Cancel", dialog)
    ok.clicked(lambda checked=False: dialog.accept())
    cancel.clicked(lambda checked=False: dialog.reject())
    buttons.addWidget(ok)
    buttons.addWidget(cancel)
    form.addLayout(buttons)
    return dialog, combo, edits, records


def insert_device():
    view, cv, layout, cell = context()
    dialog, combo, edits, records = placement_dialog()
    if dialog.exec_() == 0:
        return
    x, y = [float(str(value(edit, "text"))) for edit in edits]
    record = records[value(combo, "currentIndex")]
    # 库映射准备在事务外完成，事务内只插入可撤销的实例。
    register_all()
    library = pya.Library.library_by_name("JNULib_TFLN_" + record["process"])
    index = layout.add_lib_cell(library, library.layout().cell(record["cell_name"]).cell_index())
    view.transaction("Insert TFLN " + record["id"])
    try:
        cell.insert(pya.CellInstArray(index, pya.Trans(round(x / layout.dbu), round(y / layout.dbu))))
    finally:
        view.commit()
    apply_style(view)
    view.max_hier()
    view.zoom_fit()


def device_information():
    view, cv, layout, cell = context()
    selected = list(view.object_selection)
    names = {s.inst().cell.name for s in selected if s.is_cell_inst()}
    if not names:
        names = {cell.name}
    records = [r for r in manifest()["devices"] if r["cell_name"] in names]
    if not records:
        raise RuntimeError("请选中 TFLN 器件实例，或进入该器件 Cell。")
    lines = []
    for r in records:
        lines.extend([r["id"] + " | " + r["cell_name"], r["geometry_status"], r["port_geometry_status"]])
        for pin in r["pins"]:
            lines.append("%s: (%g, %g) µm, width=%g µm, direction=%d°%s" %
                         (pin["name"], *pin["center_um"], pin["width_um"], pin["direction_deg"], "；多细指包络" if pin["kind"] == "multi_rail_facet" else ""))
        lines.append("")
    pya.MessageBox.info("TFLN 器件参数与端口", "\n".join(lines), pya.MessageBox.Ok)


def open_local(relative):
    path = PDK_ROOT / relative
    if not path.exists():
        raise RuntimeError("文件不存在: " + str(path))
    pya.QDesktopServices.openUrl(pya.QUrl.fromLocalFile(str(path)))


def open_gds_folder():
    return open_local(Path(manifest()["devices"][0]["gds_relative"]).parents[1])


def about():
    data = manifest()
    total = sum(len(r["pins"]) for r in data["devices"])
    groups = len({r["process"] for r in data["devices"]})
    pya.MessageBox.info("JNU_MWP_TFLN_PDK " + data["version"], "%d Libraries / %d fixed devices / %d optical ports\nJNULib_TFLN_pcell: 9 PCells\nWaveguide: 1/0 (top width)\nPinRec: 1/10; DevRec: 68/0\n低台阶及待核验轮廓见器件清单 / See device index for geometry limits\nBy Songliang Chen, 2026/10/13" % (groups + 1, len(data["devices"]), total), pya.MessageBox.Ok)


def reload_pdk():
    for module in list(sys.modules):
        if module.startswith("tfln_layout_tools.actions."):
            sys.modules.pop(module, None)
    register_all(force_reload=True)
    from tfln_pcell_core.internal_waveguide_registry import install_internal_waveguide_registration
    install_internal_waveguide_registration()
    window = pya.Application.instance().main_window()
    for i in range(window.views()):
        view = window.view(i)
        cv = view.active_cellview()
        if cv.is_valid() and cv.technology == TECHNOLOGY_NAME:
            apply_style(view)
            cv.layout().refresh()
    from .menu import register_menu
    register_menu()


def schedule_reload():
    """延迟到当前菜单回调结束后重载，保留计时器和用户快捷键。"""
    global _RELOAD_TIMER
    if _RELOAD_TIMER is not None and _RELOAD_TIMER.isActive():
        return
    _RELOAD_TIMER = pya.QTimer(pya.Application.instance().main_window())
    _RELOAD_TIMER.setSingleShot(True)
    _RELOAD_TIMER.timeout(reload_pdk)
    _RELOAD_TIMER.start(0)
