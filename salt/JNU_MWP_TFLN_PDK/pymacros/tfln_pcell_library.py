# -*- coding: utf-8 -*-
# 时间: 2026-10
"""独立注册从 SOI PDK 移植的九个公开参数化器件。"""
from pathlib import Path
import pya

from tfln_pcells import (Bend90deg, MicroringDoubleBus, ArchimedeanSpiral,
                         PaperclipSpiral, PaperclipSpiralWithCompositeWaveguide,
                         Taper, SBendWaveguide, StraightWaveguide, WaveguideBump)
from tfln_pcell_core.ui_language import localize_pcell_declaration

LIBRARY_NAME = "JNULib_TFLN_pcell"
FACTORIES = (
    ("Pcell_Bend_90deg", Bend90deg),
    ("Pcell_Microring_DoubleBus", MicroringDoubleBus),
    ("Pcell_Archimedean_Spiral", ArchimedeanSpiral),
    ("Pcell_Paperclip_Spiral", PaperclipSpiral),
    ("Pcell_Paperclip_Spiral_with_Composite_Waveguide", PaperclipSpiralWithCompositeWaveguide),
    ("Pcell_Taper", Taper),
    ("Pcell_S_Bend", SBendWaveguide),
    ("Pcell_Straight_Waveguide", StraightWaveguide),
    ("Pcell_Waveguide_Bump", WaveguideBump),
)
_LIBRARIES = globals().get("_LIBRARIES", [])
SOURCE_ROOT = str(Path(__file__).resolve().parents[1])


class TFLNPCellLibrary(pya.Library):
    def __init__(self):
        super().__init__()
        self.description = "JNU_MWP_TFLN_PDK V1.0 | 9 PCells | Waveguide 1/0, PinRec 1/10, DevRec 68/0"
        self.source_root = SOURCE_ROOT
        self.layout().dbu = 0.0001
        for name, factory in FACTORIES:
            self.layout().register_pcell(name, localize_pcell_declaration(factory()))
        self.register(LIBRARY_NAME)


def register_pcell_library(force_reload=False):
    existing = pya.Library.library_by_name(LIBRARY_NAME)
    if existing is not None:
        if getattr(existing, "source_root", None) != SOURCE_ROOT:
            raise RuntimeError("已有同名库来自不同位置: " + LIBRARY_NAME)
        if not force_reload:
            return existing
    library = TFLNPCellLibrary()
    _LIBRARIES.append(library)
    if force_reload:
        library.refresh()
    return library
