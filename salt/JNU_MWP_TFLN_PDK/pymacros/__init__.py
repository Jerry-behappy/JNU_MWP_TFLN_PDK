# $autorun
# -*- coding: utf-8 -*-
# 时间: 2026-10
"""KLayout Salt 包启动入口。"""
from pathlib import Path
import sys

_directory = Path(__file__).resolve().parent
if str(_directory) not in sys.path:
    sys.path.insert(0, str(_directory))
from tfln_library import register_all
register_all()
from tfln_tools.menu import register_menu
register_menu()
