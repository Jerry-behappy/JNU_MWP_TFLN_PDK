# -*- coding: utf-8 -*-
# 时间: 2026-10
"""从唯一安装器源码生成可独立下载和拖入 KLayout 的宏。"""
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "salt/JNU_MWP_TFLN_PDK/pymacros/tfln_tools/install_pdk.py"


def build():
    macro = ET.Element("klayout-macro")
    fields = {"description": "Install JNU TFLN PDK", "version": "1.0", "category": "pymacros",
              "prolog": "", "epilog": "", "doc": "", "autorun": "false", "autorun-early": "false",
              "shortcut": "", "show-in-menu": "false", "group-name": "", "menu-path": "",
              "interpreter": "python", "dsl-interpreter-name": "", "text": SOURCE.read_text(encoding="utf-8")}
    for name, value in fields.items():
        ET.SubElement(macro, name).text = value
    ET.indent(macro, space=" ")
    destination = ROOT / "Install_JNU_TFLN_PDK.lym"
    ET.ElementTree(macro).write(destination, encoding="utf-8", xml_declaration=True)
    assert ET.parse(destination).getroot().findtext("text") == SOURCE.read_text(encoding="utf-8")
    print("INSTALL_MACRO_PASS:", destination.name)


if __name__ == "__main__":
    build()
