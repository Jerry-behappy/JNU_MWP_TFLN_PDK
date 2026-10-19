# -*- coding: utf-8 -*-
"""Migrate previous default BlackBox styles without resetting other layers."""
def refresh_blackbox_display(view):
    iterator = view.begin_layers()
    while not iterator.at_end():
        properties = iterator.current()
        style = (properties.fill_color & 0xffffff, properties.dither_pattern)
        if (properties.source_layer == 998 and properties.source_datatype == 0
                and style in ((0x004080, 0), (0xdce8f2, 1), (0xe5c8c8, 6))):
            updated = properties.dup()
            updated.frame_color = 0xffae00
            updated.fill_color = 0xffae00
            updated.dither_pattern = 5
            updated.transparent = False
            view.set_layer_properties(iterator, updated)
        iterator.next()
