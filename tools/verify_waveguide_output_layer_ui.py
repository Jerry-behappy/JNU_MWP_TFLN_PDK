# -*- coding: utf-8 -*-
# 时间: 2026-10
"""在隔离的原生 KLayout 中操作下拉框并往返转换三个页签。"""
import builtins
import faulthandler
import os
import sys
import tempfile
import traceback
from pathlib import Path

import pya

faulthandler.enable()

PACKAGE = Path(globals().get("pdk_root", Path(__file__).resolve().parents[1] / "salt/JNU_MWP_TFLN_PDK"))
sys.path.insert(0, str(PACKAGE / "pymacros"))
from tfln_layout_tools.actions import path_to_waveguide as tool
from tfln_layout_tools.actions import waveguide_to_path as reverse
from tfln_pcell_core import ui_language
from tfln_pcell_core.common import _value


def verify():
    window = pya.Application.instance().main_window()
    cv = window.create_layout(1)
    layout = cv.layout()
    layout.dbu = 0.001
    top = layout.create_cell("OUTPUT_LAYER_UI")
    cv.cell = top
    view = window.current_view()
    layout.layer(pya.LayerInfo(42, 7, "Custom core"))
    original_file, original_message = tool._waveguide_params_file, tool._message
    original_reverse_message = reverse._message
    original_language = getattr(builtins, ui_language._SESSION_KEY, None)
    failures, messages = [], []
    with tempfile.TemporaryDirectory() as directory:
        tool._waveguide_params_file = lambda: str(Path(directory) / "settings.json")
        tool._message = reverse._message = lambda title, text: messages.append(text)
        try:
            settings = tool._default_waveguide_params()
            settings, _preset, _created = tool._add_user_preset(settings, tool.TAB_SINGLE, settings["single"])
            tool._save_waveguide_params(settings)
            for row, (language, tab, layer_spec) in enumerate((
                ("en", 1, "4/0"), ("zh_CN", 2, "5/0"), ("zh_CN", 0, "42/7"),
            )):
                print("UI_STAGE", tab, layer_spec, flush=True)
                setattr(builtins, ui_language._SESSION_KEY, language)
                y = row * 400000
                shape = top.shapes(layout.layer(45, 0)).insert(pya.Path([
                    pya.Point(0, y), pya.Point(200000, y), pya.Point(200000, y + 200000),
                ], 500))
                selected = pya.ObjectInstPath()
                selected.top = top.cell_index()
                selected.cv_index = _value(view, "active_cellview_index")
                selected.shape, selected.layer = shape, layout.layer(45, 0)
                view.object_selection = [selected]

                def choose_layer():
                    dialog = pya.QApplication.activeModalWidget()
                    try:
                        combo = dialog.findChild("jnu_waveguide_layer")
                        assert combo is not None and not combo.isEditable()
                        specs = [spec for _name, spec in tool._waveguide_layer_choices(tool._load_waveguide_params()["waveguide_layer"])]
                        assert {"1/0", "4/0", "5/0", "42/7"} <= set(specs)
                        labels = [str(label.text) for label in dialog.findChildren() if isinstance(label, pya.QLabel)]
                        assert tool._dialog_text("Waveguide Layer：") in labels
                        tabs = dialog.findChild("jnu_path_to_waveguide_tabs")
                        for index in range(3):
                            tabs.setCurrentIndex(index)
                            assert not combo.isHidden()
                        tabs.setCurrentIndex(tab)
                        combo.setCurrentIndex(specs.index(layer_spec))
                        next(button for button in dialog.findChildren() if isinstance(button, pya.QPushButton)
                             and str(button.text) == tool._dialog_text("OK")).click()
                    except BaseException:
                        failures.append(traceback.format_exc())
                        dialog.reject()

                timer = pya.QTimer()
                timer.setSingleShot(True)
                timer.timeout(choose_layer)
                timer.start(0)
                tool.path_to_waveguide()
                assert not failures, failures
                assert not messages, messages
                instances = list(top.each_inst())
                assert len(instances) == 1
                instance = instances[0]
                info = tool._parse_waveguide_layer(layer_spec)
                assert instance.cell.pcell_parameters_by_name()["waveguide_layer"] == info
                assert not instance.cell.shapes(layout.layer(info)).is_empty()
                assert instance.cell.shapes(layout.layer(1, 0)).is_empty()
                assert tool._load_waveguide_params()["waveguide_layer"] == layer_spec
                selected = pya.ObjectInstPath()
                selected.top = top.cell_index()
                selected.cv_index = _value(view, "active_cellview_index")
                selected.append_path(instance)
                view.object_selection = [selected]
                reverse.waveguide_to_path()
                print("REVERSED", tab, layer_spec, flush=True)
                assert not list(top.each_inst())
                paths = [s for s in top.shapes(layout.layer(info)).each() if s.is_path()]
                assert len(paths) == 1
                assert paths[0].path == pya.Path([
                    pya.Point(0, y), pya.Point(200000, y), pya.Point(200000, y + 200000),
                ], 2000 if tab == 2 else 500), paths[0].path.to_s()
                paths[0].delete()
            assert top.shapes(layout.layer(45, 0)).is_empty()
            assert not messages, messages
            # 重新打开记住上次选择，取消时也按既有设置保存规则保留图层。
            def cancel_dialog():
                dialog = pya.QApplication.activeModalWidget()
                try:
                    combo = dialog.findChild("jnu_waveguide_layer")
                    specs = [spec for _name, spec in tool._waveguide_layer_choices("42/7")]
                    assert specs[int(_value(combo, "currentIndex"))] == "42/7"
                    combo.setCurrentIndex(specs.index("1/0"))
                except BaseException:
                    failures.append(traceback.format_exc())
                dialog.reject()

            timer = pya.QTimer()
            timer.setSingleShot(True)
            timer.timeout(cancel_dialog)
            timer.start(0)
            assert tool._show_waveguide_dialog(layout.dbu) is None
            print("CANCELLED", flush=True)
            assert not failures, failures
            assert tool._load_waveguide_params()["waveguide_layer"] == "1/0"
        finally:
            tool._waveguide_params_file, tool._message = original_file, original_message
            reverse._message = original_reverse_message
            setattr(builtins, ui_language._SESSION_KEY, original_language)
    print("NATIVE_OUTPUT_LAYER_UI_PASS: bilingual dropdown, three tabs, custom layer, persistence, forward and reverse actions", flush=True)


if __name__ == "__main__":
    try:
        verify()
    except BaseException:
        traceback.print_exc()
        sys.stderr.flush()
        os._exit(1)
    # 隔离测试生成的临时版图无需保存，避免退出时弹出确认框。
    os._exit(0)
