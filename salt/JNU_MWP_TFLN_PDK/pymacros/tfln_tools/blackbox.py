# -*- coding: utf-8 -*-
"""SOI-compatible blackbox body, inward port straights and centered label."""
import pya

PORT_STRAIGHT_LENGTH_UM = 0.2


def port_geometry(footprint, pins, dbu):
    length = max(1, round(PORT_STRAIGHT_LENGTH_UM / dbu))
    left, bottom, right, top = footprint.left, footprint.bottom, footprint.right, footprint.top
    straights = []
    for pin in pins:
        x, y = [round(v / dbu) for v in pin["center_um"]]
        width = round(pin["width_um"] / dbu)
        low, high = width // 2, width - width // 2
        direction = pin["direction_deg"]
        if direction == 180:
            box = pya.Box(x, y - low, x + length, y + high)
            left = max(left, x + length)
        elif direction == 0:
            box = pya.Box(x - length, y - low, x, y + high)
            right = min(right, x - length)
        elif direction == 270:
            box = pya.Box(x - low, y, x + high, y + length)
            bottom = max(bottom, y + length)
        elif direction == 90:
            box = pya.Box(x - low, y - length, x + high, y)
            top = min(top, y - length)
        else:
            raise ValueError("Blackbox ports must be horizontal or vertical")
        straights.append((direction, box))
    if not straights or left >= right or bottom >= top:
        raise ValueError("Blackbox cannot accommodate the port straights")
    center = pya.Box(left, bottom, right, top)
    body, stubs = pya.Region(center), pya.Region()
    for direction, box in straights:
        stubs.insert(box)
        # TFLN polarization devices can have staggered facets. Extend only the
        # placeholder, preserving each original port and its 0.2 um straight.
        if not center.touches(box):
            connector = {
                0: pya.Box(center.right, box.bottom, box.left, box.top),
                180: pya.Box(box.right, box.bottom, center.left, box.top),
                90: pya.Box(box.left, center.top, box.right, box.bottom),
                270: pya.Box(box.left, box.top, box.right, center.bottom),
            }[direction]
            body.insert(connector)
    body.merge()
    if body.count() != 1 or not (body & stubs).is_empty():
        raise ValueError("Invalid placeholder or overlapping port straights")
    if any(not (body + pya.Region(box)).merged().count() == 1 for _, box in straights):
        raise ValueError("Disconnected blackbox port straight")
    return body, stubs.merged(), center


def insert_label(cell, target_box, label):
    layout = cell.layout()
    dbu = layout.dbu
    mag = max(0.02, min(target_box.height() * dbu * 0.45 / 0.7,
                        target_box.width() * dbu / (max(1, len(label)) * 0.75)))
    text_cell = layout.create_cell("TEXT", "Basic", {
        "text": label, "layer": pya.LayerInfo(10, 0), "mag": mag})
    if text_cell is None or text_cell.bbox().empty():
        # Standalone Python has no Basic library. Use the same font as editable
        # vector geometry; native KLayout exports use the Basic TEXT PCell.
        text_cell = layout.create_cell("BLACKBOX_LABEL_" + str(cell.cell_index()))
        text_cell.shapes(layout.layer(10, 0)).insert(
            pya.TextGenerator.default_generator().text(label, dbu, mag))
    box = text_cell.bbox()
    if box.empty():
        raise ValueError("Empty blackbox label")
    dx = (target_box.left + target_box.right - box.left - box.right) // 2
    dy = (target_box.bottom + target_box.top - box.bottom - box.top) // 2
    cell.insert(pya.CellInstArray(text_cell.cell_index(), pya.Trans(dx, dy)))
    return text_cell


def draw_blackbox(layout, record):
    """Rebuild from public interfaces only; never copy source manufacturing shapes."""
    dbu = layout.dbu
    cell = layout.create_cell(record["cell_name"])
    footprint = pya.Box(*[round(v / dbu) for v in record["physical_bbox_um"]])
    body, stubs, center = port_geometry(footprint, record["pins"], dbu)
    cell.shapes(layout.layer(998, 0)).insert(body)
    cell.shapes(layout.layer(1, 0)).insert(stubs)
    for pin in record["pins"]:
        x, y = [round(v / dbu) for v in pin["center_um"]]
        half = max(1, round(pin.get("path_length_um", 0.02) / 2 / dbu))
        dx, dy = {0: (half, 0), 90: (0, half), 180: (-half, 0), 270: (0, -half)}[pin["direction_deg"]]
        cell.shapes(layout.layer(1, 10)).insert(pya.Path(
            [pya.Point(x - dx, y - dy), pya.Point(x + dx, y + dy)], round(pin["width_um"] / dbu)))
        label = cell.shapes(layout.layer(1, 10)).insert(pya.Text(pin["name"], pya.Trans(x, y)))
        label.text_dsize = min(0.7, max(0.2, pin["width_um"] / 2))
    cell.shapes(layout.layer(68, 0)).insert(pya.Box(*[round(v / dbu) for v in record["devrec_bbox_um"]]))
    x, y = [round(v / dbu) for v in record["author_layout"]["anchor_um"]]
    author = cell.shapes(layout.layer(10, 0)).insert(pya.Text(record["author"], pya.Trans(x, y)))
    author.text_dsize = record["author_layout"]["height_um"]
    author.text_halign, author.text_valign = 0, 0
    insert_label(cell, center, record["cell_name"] + " (black box)")
    return cell, body.bbox(), center
