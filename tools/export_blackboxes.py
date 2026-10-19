# -*- coding: utf-8 -*-
"""Rebuild individual public blackboxes from the published interface manifest.

Run with Python/pya or native KLayout (-b -r ... -rd output=NEW_DIRECTORY).
The output directory must not exist. No private geometry is read.
"""
import argparse
import json
import sys
from pathlib import Path
import pya

PACKAGE = Path(__file__).resolve().parents[1] / "salt/JNU_MWP_TFLN_PDK"
sys.path.insert(0, str(PACKAGE / "pymacros"))
from tfln_tools.blackbox import draw_blackbox


def export(destination):
    data = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    destination = Path(destination).resolve()
    destination.mkdir(parents=True, exist_ok=False)
    for record in data["devices"]:
        layout = pya.Layout()
        layout.dbu = data["dbu_um"]
        draw_blackbox(layout, record)
        path = destination / record["process"] / (record["cell_name"] + ".gds")
        path.parent.mkdir(exist_ok=True)
        options = pya.SaveLayoutOptions()
        options.gds2_max_cellname_length = 256
        options.gds2_libname = "JNU_MWP_TFLN_PDK_V1_1"
        layout.write(str(path), options)
    print("BLACKBOX_EXPORT_PASS", len(data["devices"]))


if __name__ == "__main__":
    if "output" in globals():
        export(output)
    else:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument("--output", required=True)
        export(parser.parse_args().output)
