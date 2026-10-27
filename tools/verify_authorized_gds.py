# -*- coding: utf-8 -*-
# 时间: 2026-10
"""验证本地授权库导入的版本保留、端口拒绝和目录隔离。"""
import json
import shutil
import sys
import tempfile
from pathlib import Path
import pya

PACKAGE = Path(__file__).resolve().parents[1] / 'salt/JNU_MWP_TFLN_PDK'
sys.path.insert(0, str(PACKAGE / 'pymacros'))
from tfln_tools import authorized_gds as store


def verify():
    records = json.loads((PACKAGE / 'manifest.json').read_text(encoding='utf-8'))['devices']
    record = records[0]
    # 用保留器件的真实端口整体旋转，继续覆盖竖直端口验证。
    rotated = json.loads(json.dumps(record))
    rotated_layout = pya.Layout()
    rotated_layout.read(str(PACKAGE / record['gds_relative']))
    transform = pya.Trans(pya.Trans.R90)
    rotated_layout.cell(record['cell_name']).transform(transform)
    for pin in rotated['pins']:
        x, y = pin['center_um']
        pin['center_um'] = [-y, x]
        pin['direction_deg'] = (pin['direction_deg'] + 90) % 360
    store.validate_ports(rotated_layout, rotated_layout.cell(record['cell_name']), rotated)
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        source, private = base / 'source', base / 'private'
        source.mkdir()
        candidate = source / 'device.gds'
        shutil.copy2(PACKAGE / record['gds_relative'], candidate)
        original_root = store.private_root
        store.private_root = lambda: private
        try:
            assert store.install_directory(source, [record]) == 1
            first = store.private_source(record)
            assert first.is_relative_to(private) and first.is_file()
            assert store.install_directory(source, [record]) == 1
            second = store.private_source(record)
            assert first != second and first.is_file() and second.is_file()
            # 旧名授权文件仍能导入；仅安装副本改用简名，源文件保持旧名。
            if record.get('legacy_cell_names'):
                legacy_name = record['legacy_cell_names'][0]
                legacy_folder = base / 'legacy'
                legacy_folder.mkdir()
                legacy_file = legacy_folder / 'device.gds'
                legacy = pya.Layout()
                legacy.read(str(candidate))
                legacy.top_cell().name = legacy_name
                options = pya.SaveLayoutOptions()
                options.gds2_max_cellname_length = 256
                legacy.write(str(legacy_file), options)
                assert store.install_directory(legacy_folder, [record]) == 1
                installed = store.private_source(record)
                reread = pya.Layout()
                reread.read(str(installed))
                assert reread.top_cell().name == record['cell_name']
                reread = pya.Layout()
                reread.read(str(legacy_file))
                assert reread.top_cell().name == legacy_name
                from tfln_library import copy_gds
                library = pya.Library()
                copy_gds(library, record, legacy_file)
                assert library.layout().cell(record['cell_name']) is not None
                assert library.layout().cell(legacy_name) is None
                mapping = json.loads((private / 'active.json').read_text(encoding='utf-8'))
                mapping[legacy_name] = mapping.pop(record['cell_name'])
                (private / 'active.json').write_text(json.dumps(mapping), encoding='utf-8')
                assert store.private_source(record) == installed
            active = (private / 'active.json').read_text(encoding='utf-8')
            # 已知端口整体偏移必须拒绝，拒绝后保留当前映射和两个版本。
            layout = pya.Layout()
            layout.read(str(candidate))
            cell = layout.cell(record['cell_name'])
            cell.shapes(layout.layer(1, 10)).transform(pya.Trans(1000, 0))
            options = pya.SaveLayoutOptions()
            options.gds2_max_cellname_length = 256
            layout.write(str(candidate), options)
            try:
                store.install_directory(source, [record])
            except AssertionError:
                pass
            else:
                raise AssertionError('端口错位未被拒绝')
            assert (private / 'active.json').read_text(encoding='utf-8') == active
            assert first.is_file() and second.is_file() and candidate.is_file()
            (private / 'active.json').write_text(json.dumps({record['cell_name']: '../source/device.gds'}), encoding='utf-8')
            try:
                store.private_source(record)
            except RuntimeError:
                pass
            else:
                raise AssertionError('私有索引越界未被拒绝')
        finally:
            store.private_root = original_root
    print('AUTHORIZED_GDS_PASS: local version retention, invalid-port rejection and path boundary')


if __name__ == '__main__':
    verify()
