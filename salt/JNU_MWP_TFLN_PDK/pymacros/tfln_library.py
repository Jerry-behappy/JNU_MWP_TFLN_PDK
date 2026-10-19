# -*- coding: utf-8 -*-
# 时间: 2026-10
"""加载便携式 TFLN 固定器件库；不依赖源 FSP 或其他 PDK。"""
import json
import sys
from pathlib import Path
import pya

PDK_ROOT = Path(__file__).resolve().parents[1]
TECHNOLOGY_NAME = "JNU_MWP_TFLN_PDK"
_MANIFEST = json.loads((PDK_ROOT / "manifest.json").read_text(encoding="utf-8"))
VERSION = _MANIFEST["version"]
PROCESSES = tuple(_MANIFEST.get("processes") or sorted({d["process"] for d in _MANIFEST["devices"]}))
BLACKBOX_LIBRARY_NAME = "JNULib_TFLN_BlackBox"
_LIBRARIES = globals().get("_LIBRARIES", [])


def load_technology():
    """仅注册本包技术，不改变当前视图、默认技术及其他技术。"""
    if pya.Technology.has_technology(TECHNOLOGY_NAME):
        technology = pya.Technology.technology_by_name(TECHNOLOGY_NAME)
    else:
        technology = pya.Technology.create_technology(TECHNOLOGY_NAME)
    technology.load(str(PDK_ROOT / (TECHNOLOGY_NAME + ".lyt")))
    technology.name = TECHNOLOGY_NAME
    return technology


def copy_gds(library, record, path):
    """保留 GDS 层级及端口，禁止在加载时重画器件。"""
    source = pya.Layout()
    source.read(str(path))
    roots = [source.cell(t) if isinstance(t, int) else t for t in source.each_top_cell()]
    if len(roots) != 1 or roots[0].name != record["cell_name"]:
        raise RuntimeError("器件顶层与清单不一致: " + record["id"])
    if library.layout().cell(record["cell_name"]) is not None:
        raise RuntimeError("器件名称重复: " + record["cell_name"])
    target = library.layout().create_cell(record["cell_name"])
    target.copy_tree(roots[0])


class FixedTFLNLibrary(pya.Library):
    def __init__(self, process, records):
        super().__init__()
        kind = "黑盒库 / Blackbox Library" if _MANIFEST.get("edition") == "public-blackbox" else "授权器件库 / Authorized Device Library"
        self.description = "%s | JNU_MWP_TFLN_PDK %s | thickness/etch %s nm | %d devices" % (kind, VERSION, process.replace("_", "/"), len(records))
        self.layout().dbu = 0.0001
        self.add_technology(TECHNOLOGY_NAME)
        self.source_root = str(PDK_ROOT)
        for record in records:
            from tfln_tools.authorized_gds import private_source
            copy_gds(self, record, private_source(record) or PDK_ROOT / record["gds_relative"])
        # 固定库按当前清单的工艺组合注册，兼容新增的膜厚/刻蚀组合。
        self.register("JNULib_TFLN_" + process)


class BlackboxTFLNLibrary(pya.Library):
    def __init__(self, records):
        super().__init__()
        self.description = "黑盒库 / Blackbox Library | JNU_MWP_TFLN_PDK %s | %d devices" % (VERSION, len(records))
        self.layout().dbu = 0.0001
        self.source_root = str(PDK_ROOT)
        self.add_technology(TECHNOLOGY_NAME)
        for record in records:
            # 独立黑盒库始终读取公开黑盒，不被授权完整轮廓覆盖。
            source = PDK_ROOT / "pymacros/tfln_blackbox_gds" / record["process"] / (record["cell_name"] + ".gds")
            copy_gds(self, record, source)
        self.register(BLACKBOX_LIBRARY_NAME)


def register_all(force_reload=False):
    """幂等注册清单中的固定库和独立 PCell 库。"""
    load_technology()
    manifest = json.loads((PDK_ROOT / "manifest.json").read_text(encoding="utf-8"))
    result = []
    for process in PROCESSES:
        name = "JNULib_TFLN_" + process
        existing = pya.Library.library_by_name(name, TECHNOLOGY_NAME)
        if existing is not None:
            if getattr(existing, "source_root", None) != str(PDK_ROOT):
                raise RuntimeError("已有同名库来自不同位置: " + name)
            if not force_reload:
                # 将旧会话中全局可见的库迁移为仅在 TFLN 技术下可选。
                existing.clear_technologies()
                existing.add_technology(TECHNOLOGY_NAME)
                result.append(existing)
                continue
        records = [d for d in manifest["devices"] if d["process"] == process]
        library = FixedTFLNLibrary(process, records)
        _LIBRARIES.append(library)
        if force_reload:
            library.refresh()
        result.append(library)
    existing = pya.Library.library_by_name(BLACKBOX_LIBRARY_NAME, TECHNOLOGY_NAME)
    if existing is not None and getattr(existing, "source_root", None) != str(PDK_ROOT):
        raise RuntimeError("已有同名库来自不同位置: " + BLACKBOX_LIBRARY_NAME)
    if existing is not None and not force_reload:
        existing.clear_technologies()
        existing.add_technology(TECHNOLOGY_NAME)
        result.append(existing)
    else:
        library = BlackboxTFLNLibrary(manifest["devices"])
        _LIBRARIES.append(library)
        if force_reload:
            library.refresh()
        result.append(library)
    if force_reload:
        # 先刷新独立几何模块，再用相同 Library 名称替换声明并刷新已有实例。
        for module in list(sys.modules):
            if module == "tfln_pcell_library" or module.startswith(("tfln_pcells", "tfln_pcell_core")):
                sys.modules.pop(module, None)
    from tfln_pcell_library import register_pcell_library
    result.append(register_pcell_library(force_reload=force_reload))
    return result
