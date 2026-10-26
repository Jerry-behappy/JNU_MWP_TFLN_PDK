# -*- coding: utf-8 -*-
# 时间: 2026-10
import json
import sys
import os
import traceback
from pathlib import Path
import pya
import faulthandler
faulthandler.enable()

try:
    root = Path(globals().get("pdk_root", Path(__file__).resolve().parents[1] / "salt/JNU_MWP_TFLN_PDK"))
    sys.path.insert(0, str(root / "pymacros"))
    if "siepic_python" in globals(): sys.path.insert(0, str(siepic_python))
    # A deterministic offline import avoids unrelated SiEPIC update dialogs.
    import requests
    original_get = requests.get
    def offline_get(*args, **kwargs):
        raise requests.RequestException("offline verification")
    requests.get = offline_get
    try:
        print("STAGE SiEPIC import", flush=True)
        import SiEPIC
        import SiEPIC.scripts
    finally:
        requests.get = original_get
    from tfln_library import register_all, TECHNOLOGY_NAME
    from tfln_tools import actions, menu
    from SiEPIC.utils import get_technology_by_name
    print("STAGE register libraries", flush=True)
    libraries = register_all()
    print("STAGE menu", flush=True)
    menu.register_menu()
    data = actions.manifest()
    window = pya.Application.instance().main_window()
    assert window is not None
    assert len(libraries) == 3 and len(menu._ACTIONS) == 23
    assert all(l.technologies() == [TECHNOLOGY_NAME] for l in libraries)
    assert all(not l.is_for_technology(other) for l in libraries for other in ("", "JNU_MWP_SOI_PDK", "GSiP", "EBeam"))
    assert window.menu().action(menu.ROOT_MENU).title == "JNU_MWP_TFLN_PDK V1.1"
    key = menu.ROOT_MENU + ".layout.tfln_insert_device"
    menu._ACTIONS[key].shortcut = "Ctrl+Alt+T"
    # 模拟旧会话留下的工艺总览入口，重载后必须清理。
    retired_key = menu.ROOT_MENU + ".libraries.tfln_overview_300_125"
    retired_action = pya.Action()
    retired_action.title = "旧工艺总览"
    window.menu().insert_item(menu.ROOT_MENU + ".libraries.end", "tfln_overview_300_125", retired_action)
    menu._ACTIONS[retired_key] = retired_action
    menu.register_menu()
    assert retired_key not in menu._ACTIONS and len(menu._ACTIONS) == 23
    assert menu._ACTIONS[key].shortcut == "Ctrl+Alt+T"
    view = actions.new_layout()
    print("STAGE new layout", flush=True)
    assert view.active_cellview().technology == TECHNOLOGY_NAME
    dialog, combo, edits, records = actions.placement_dialog()
    assert actions.value(combo, "count") == 24
    dialog.reject()
    dialog.destroy()
    for overview in data["overviews"]:
        print("STAGE overview", overview["process"], flush=True)
        cv = actions.open_overview(overview["process"])
        assert sum(1 for _ in cv.cell.each_inst()) == overview["device_count"]
    view = actions.new_layout()
    cv = view.active_cellview()
    layout, top = cv.layout(), cv.cell
    technology = get_technology_by_name(TECHNOLOGY_NAME)
    layout.TECHNOLOGY = technology
    total, rows, instances = 0, [], []
    for i, record in enumerate(records):
        print("STAGE device", record["id"], flush=True)
        instance = actions.insert_into(layout, top, record, i * 700, 0)
        instances.append(instance)
        pins, errors = instance.cell.find_pins()
        assert not errors and len(pins) == len(record["pins"]), (record["id"], errors)
        component = top.find_components(inst=instance)
        assert len(component.pins) == len(pins), record["id"]
        for transform in (pya.Trans(pya.Trans.R90, 500000, -400000), pya.Trans(pya.Trans.M0, -500000, 400000)):
            check = pya.Layout()
            check.dbu = layout.dbu
            check.TECHNOLOGY = technology
            parent = check.create_cell("TRANSFORM")
            cell = check.create_cell(record["cell_name"])
            cell.copy_tree(instance.cell)
            moved = parent.insert(pya.CellInstArray(cell.cell_index(), transform))
            detected = parent.find_components(inst=moved)
            assert len(detected.pins) == len(pins)
            for pin in detected.pins:
                meta = next(p for p in record["pins"] if p["name"] == pin.pin_name)
                assert pin.center == transform * pya.Point(*[round(v / check.dbu) for v in meta["center_um"]]), record["id"]
                assert pin.path == next(p.path for p in pins if p.pin_name == pin.pin_name).transformed(transform)
        total += len(pins)
        rows.append({"id": record["id"], "ports": len(pins), "recognition_rotation_mirror": "PASS"})
    assert total == 108
    print("STAGE reload", flush=True)
    actions.reload_pdk()
    assert len(menu._ACTIONS) == 23 and menu._ACTIONS[key].shortcut == "Ctrl+Alt+T"
    # Native library refresh replaces instance handles; reacquire from layout.
    instances = list(top.each_inst())
    assert len(instances) == 24
    assert all(i.cell.is_library_cell() for i in instances)
    assert sum(len(i.cell.find_pins()[0]) for i in instances) == 108
    # Migration affects only known default BlackBox styles in a TFLN view.
    from tfln_tools.blackbox_display import refresh_blackbox_display
    iterator = view.begin_layers()
    found = False
    while not iterator.at_end():
        prop = iterator.current()
        if prop.source_layer == 998:
            old = prop.dup()
            old.fill_color, old.frame_color, old.dither_pattern = 0xe5c8c8, 0xa08080, 6
            view.set_layer_properties(iterator, old)
            found = True
            break
        iterator.next()
    assert found
    refresh_blackbox_display(view)
    iterator = view.begin_layers()
    while not iterator.at_end() and iterator.current().source_layer != 998:
        iterator.next()
    prop = iterator.current()
    print("DISPLAY", hex(prop.fill_color), prop.dither_pattern, flush=True)
    assert (prop.fill_color & 0xffffff) == 0xffae00 and prop.dither_pattern == 5
    report = {"status": "PASS", "engine": "native KLayout + SiEPIC", "edition": data["edition"],
              "devices": rows, "ports": total, "libraries": 3, "menus": 23,
              "process_scope": data["process_scope"],
              "checks": ["TFLN-only library filtering", "independent blackbox library", "single supported process overview", "placement dialog", "SiEPIC pins and components", "rotation and mirror", "reload", "legacy blackbox color migration"]}
    target = Path(globals().get("report_path", "native_ui_report.json"))
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("NATIVE_VERIFY_PASS", data["edition"], "24 devices, 108 pins, three libraries, 23 menus", flush=True)
    # Isolated verification layouts are intentionally unsaved; bypass save dialogs.
    os._exit(0)
except Exception:
    traceback.print_exc()
    sys.stderr.flush()
    os._exit(1)
