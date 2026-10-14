# -*- coding: utf-8 -*-
# 时间: 2026-10
"""加载公开 TFLN 固定黑盒；不包含内部制造轮廓。"""
import json
from pathlib import Path
import pya

PDK_ROOT = Path(__file__).resolve().parents[1]
TECHNOLOGY_NAME = "JNU_MWP_TFLN_PDK"
VERSION = "V1.0"
PROCESSES = ("300_125", "400_200", "600_300", "600_600")
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


class FixedTFLNLibrary(pya.Library):
    def __init__(self, process, records):
        super().__init__()
        self.description = "JNU_MWP_TFLN_PDK %s | BLACKBOX | thickness/etch %s nm | %d devices | By Songliang Chen" % (VERSION, process.replace("_", "/"), len(records))
        self.layout().dbu = 0.0001
        self.source_root = str(PDK_ROOT)
        for record in records:
            source = pya.Layout()
            source.read(str(PDK_ROOT / record["gds_relative"]))
            roots = [source.cell(t) if isinstance(t, int) else t for t in source.each_top_cell()]
            if len(roots) != 1 or roots[0].name != record["cell_name"]:
                raise RuntimeError("器件顶层与清单不一致: " + record["id"])
            if self.layout().cell(record["cell_name"]) is not None:
                raise RuntimeError("器件名称重复: " + record["cell_name"])
            target = self.layout().create_cell(record["cell_name"])
            target.copy_tree(roots[0])
        # 保持全局可见，选用 TFLN Technology 时也能直接调用四个库。
        self.register("JNULib_TFLN_" + process)


def register_all(force_reload=False):
    """幂等注册四个库，避免启动宏及手动加载产生重复条目。"""
    load_technology()
    manifest = json.loads((PDK_ROOT / "manifest.json").read_text(encoding="utf-8"))
    result = []
    for process in PROCESSES:
        name = "JNULib_TFLN_" + process
        existing = pya.Library.library_by_name(name)
        if existing is not None:
            if getattr(existing, "source_root", None) != str(PDK_ROOT):
                raise RuntimeError("已有同名库来自不同位置: " + name)
            if not force_reload:
                result.append(existing)
                continue
        records = [d for d in manifest["devices"] if d["process"] == process]
        library = FixedTFLNLibrary(process, records)
        _LIBRARIES.append(library)
        if force_reload:
            library.refresh()
        result.append(library)
    return result
