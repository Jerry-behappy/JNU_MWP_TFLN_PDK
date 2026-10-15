# -*- coding: utf-8 -*-
# 时间: 2026-10
"""独立顶层功能菜单；稳定 ID、回调引用与快捷键保存在模块中。"""
import importlib
import pya
from . import actions

ROOT_MENU = "jnu_mwp_tfln_pdk_menu"
MENU_TITLE = "JNU_MWP_TFLN_PDK V1.0"
_ACTIONS = globals().get("_ACTIONS", {})


def run(callback):
    try:
        callback()
    except Exception as error:
        pya.MessageBox.warning(MENU_TITLE, str(error), pya.MessageBox.Ok)


def tool(module, function):
    """点击时导入功能实现，使重载后的菜单调用最新代码。"""
    return lambda: getattr(importlib.import_module("tfln_layout_tools.actions." + module), function)()


def update_pdk():
    from .install_pdk import show_installer
    return show_installer()


def install_whitebox():
    from .authorized_gds import install_whitebox_dialog
    return install_whitebox_dialog()


def register_menu():
    window = pya.Application.instance().main_window()
    if window is None:
        return
    menu = window.menu()
    if not menu.is_menu(ROOT_MENU):
        menu.insert_menu("help_menu", ROOT_MENU, MENU_TITLE)
    menu.action(ROOT_MENU).title = MENU_TITLE
    for item, title in (("waveguides", "波导 / Waveguides"), ("layout", "版图 / Layout"),
                        ("drc", "设计规则检查 / DRC"), ("libraries", "器件库 / Libraries"), ("help", "说明 / Help")):
        path = ROOT_MENU + "." + item
        if not menu.is_menu(path):
            menu.insert_menu(ROOT_MENU + ".end", item, title)
    specs = [
             ("waveguides", "path_to_waveguide", "路径转波导 / Path to Waveguide", tool("path_to_waveguide", "path_to_waveguide")),
             ("waveguides", "waveguide_to_path", "波导转路径 / Waveguide to Path", tool("waveguide_to_path", "waveguide_to_path")),
             ("waveguides", "waveguide_length", "计算波导长度 / Calculate Waveguide Length", tool("calculate_waveguide_length", "calculate_waveguide_length")),
             ("waveguides", "waveguide_length_difference", "计算波导长度差 / Calculate Waveguide Length Difference", tool("calculate_waveguide_length_difference", "calculate_waveguide_length_difference")),
             ("waveguides", "cell_connect", "通过波导连接器件 / Cell Connect by Waveguide", tool("cell_connect_by_waveguide", "cell_connect_by_waveguide")),
             ("layout", "make_pins", "为单元生成端口 / Make Pins for Cell", tool("make_pins_for_cell", "make_pins_for_cell")),
             ("layout", "layer_exclude", "排除图层 / Layer Exclude", tool("layer_exclude", "layer_exclude")),
             ("layout", "numerical_text", "数字文本阵列 / Numerical text array", tool("numerical_text_array", "numerical_text_array")),
             ("layout", "snap_components", "吸附器件 / Snap components", tool("snap_components", "snap_components")),
             ("drc", "edit_rules", "编辑 TFLN 设计规则 / JNU_MWP_TFLN_DRC", tool("drc", "open_drc_macro_editor")),
             ("drc", "run_rules", "运行 TFLN 设计规则检查 / Run JNU_MWP_TFLN_DRC", tool("drc", "run_current_cell_drc")),
             ("layout", "new_layout", "新建 TFLN 版图 / New Layout", actions.new_layout),
             ("layout", "insert_device", "插入 TFLN 器件 / Insert Device…", actions.insert_device),
             ("layout", "apply_layers", "应用 TFLN 技术与图层 / Apply Technology & Layers", actions.apply_style),
             ("layout", "device_info", "器件参数与端口 / Device & Port Info", actions.device_information)]
    for process in ("300_125", "400_200", "600_300", "600_600"):
        specs.append(("libraries", "overview_" + process, process.replace("_", "/") + " nm 总览 / Overview", lambda p=process: actions.open_overview(p)))
    specs.extend([("libraries", "open_gds", "打开器件 GDS 文件夹 / Open GDS Folder", lambda: actions.open_local("pymacros/tfln_blackbox_gds")),
                  ("help", "inventory", "器件清单 / Device Index", lambda: actions.open_local("docs/DEVICE_INDEX.md")),
                  ("help", "readme", "使用说明 / User Guide", lambda: actions.open_local("docs/USER_GUIDE.md")),
                  ("help", "about", "关于 / About", actions.about),
                  ("", "reload", "重新加载 TFLN PDK / Reload TFLN PDK", actions.schedule_reload),
                  ("", "update", "检查 PDK 更新 / Check for PDK Updates", update_pdk),
                  ("", "install_whitebox", "安装／更新白盒器件库 / Install / Update Whitebox Library", install_whitebox)])
    for parent, name, title, callback in specs:
        path = ROOT_MENU + ("." + parent if parent else "")
        key = path + ".tfln_" + name
        shortcut = actions.value(_ACTIONS[key], "shortcut") if key in _ACTIONS else ""
        if key not in _ACTIONS:
            # 同一进程中由其他宏先建菜单时，读取原生 Action 而不覆盖其绑定。
            try:
                shortcut = actions.value(menu.action(key), "shortcut")
            except Exception:
                pass
        try:
            menu.delete_item(key)
        except Exception:
            pass
        action = pya.Action()
        action.title = title
        action.shortcut = shortcut
        action.on_triggered(lambda checked=False, fn=callback: run(fn))
        menu.insert_item(path + ".end", "tfln_" + name, action)
        _ACTIONS[key] = action
