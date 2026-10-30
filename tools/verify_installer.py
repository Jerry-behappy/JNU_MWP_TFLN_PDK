# -*- coding: utf-8 -*-
# 时间: 2026-10
"""用临时 Git 仓库验证安装、更新和保留原文件；原生 KLayout 再验收 Qt 后台任务。"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import threading
import time
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "salt/JNU_MWP_TFLN_PDK/pymacros/tfln_tools/install_pdk.py"
spec = importlib.util.spec_from_file_location("tfln_installer_fixture", SOURCE)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def reject(action, expected):
    try:
        action()
    except RuntimeError as error:
        assert expected in str(error), str(error)
    else:
        raise AssertionError("安装器未保护应保留的内容: " + expected)


def verify_private(git, base):
    """通过真实临时 Git 仓库验证私有克隆、旧地址迁移和拒绝错误端口。"""
    import pya
    record = json.loads((ROOT / "salt/JNU_MWP_TFLN_PDK/manifest.json").read_text(encoding="utf-8"))["devices"][0]
    seed = base / "private seed.git"
    seed.mkdir()
    installer._run([git, "init", "-b", "main", seed])
    installer._git(git, seed, "config", "user.name", "Installer Fixture")
    installer._git(git, seed, "config", "user.email", "fixture@example.invalid")
    source_dir = seed / "JNU_MWP_TFLN_gds"
    source_dir.mkdir()
    source_file = source_dir / (record["cell_name"] + ".gds")
    layout = pya.Layout()
    layout.read(str(ROOT / "salt/JNU_MWP_TFLN_PDK" / record["gds_relative"]))
    cell = layout.cell(record["cell_name"])
    # 测试用完整矩形轮廓，端口使用实际清单；不读取任何本机白盒。
    cell.shapes(layout.layer(998, 0)).clear()
    cell.shapes(layout.layer(1, 0)).clear()
    cell.shapes(layout.layer(1, 0)).insert(pya.Box(*[round(v / layout.dbu) for v in record["physical_bbox_um"]]))
    options = pya.SaveLayoutOptions()
    options.gds2_max_cellname_length = 256
    layout.write(str(source_file), options)
    catalog = {"edition": "private-whitebox", "devices": [dict(record, gds_relative="JNU_MWP_TFLN_gds/" + source_file.name)]}
    (seed / "manifest.json").write_text(json.dumps(catalog), encoding="utf-8")
    installer._git(git, seed, "add", ".")
    installer._git(git, seed, "commit", "-m", "Private initial")
    installer.PRIVATE_URL = str(seed)
    home = base / "私有 GUI 配置"
    package = home / installer.PDK_RELATIVE
    (package / "pymacros/tfln_tools").mkdir(parents=True)
    (package / "manifest.json").write_text(json.dumps({"devices": [record]}), encoding="utf-8")
    shutil.copy2(SOURCE.parent / "authorized_gds.py", package / "pymacros/tfln_tools/authorized_gds.py")
    repository = Path(installer.install_private(home))
    assert not repository.resolve().is_relative_to(package.resolve())
    assert "1 个器件" in installer.activate_private(home, repository)
    active = home / "jnu_private/JNU_MWP_TFLN_PDK/active.json"
    original = active.read_bytes()
    # 用本地可读取的旧地址模拟转移：验证后才将 origin 改为规范地址。
    alias = base / "old private remote"
    installer._run([git, "clone", "--bare", seed, alias])
    installer._TRANSFERRED_REPOSITORIES[str(alias)] = str(seed).removesuffix(".git")
    installer._git(git, repository, "remote", "set-url", "origin", str(alias))
    installer.install_private(home)
    assert installer._git(git, repository, "remote", "get-url", "origin") == str(seed)
    assert installer._repo_identity("git@github.com:Jerry-behappy/JNU_MWP_TFLN_Library.git") == installer._repo_identity("https://github.com/Jinan-Photonics-Integration-Center/JNU_MWP_TFLN_Library.git")
    installer.activate_private(home, repository)
    assert active.read_bytes() != original
    # 清单不完整或端口错位均不得改变正在使用的版本。
    current = active.read_bytes()
    wrong = dict(catalog, devices=[])
    (seed / "manifest.json").write_text(json.dumps(wrong), encoding="utf-8")
    installer._git(git, seed, "add", ".")
    installer._git(git, seed, "commit", "-m", "Invalid catalog")
    reject(lambda: installer.install_private(home), "有效的 TFLN 白盒")
    assert active.read_bytes() == current
    (seed / "manifest.json").write_text(json.dumps(catalog), encoding="utf-8")
    cell.shapes(layout.layer(1, 10)).transform(pya.Trans(1000, 0))
    layout.write(str(source_file), options)
    installer._git(git, seed, "add", ".")
    installer._git(git, seed, "commit", "-m", "Invalid ports")
    installer.install_private(home)
    try:
        installer.activate_private(home, repository)
    except AssertionError:
        pass
    else:
        raise AssertionError("错误端口未被拒绝")
    assert active.read_bytes() == current
    cell.shapes(layout.layer(1, 10)).transform(pya.Trans(-1000, 0))
    layout.write(str(source_file), options)
    installer._git(git, seed, "add", ".")
    installer._git(git, seed, "commit", "-m", "Restore ports")
    print("PRIVATE_INSTALLER_PASS: isolated clone, old-origin migration, version retention and invalid catalog/port rejection", flush=True)
    return home


def main():
    assert ET.parse(ROOT / "Install_JNU_TFLN_PDK.lym").getroot().findtext("text") == SOURCE.read_text(encoding="utf-8")
    git = installer.find_git()
    with tempfile.TemporaryDirectory(prefix="tfln-installer-") as temporary:
        base = Path(temporary).resolve()
        assert base.parent == Path(tempfile.gettempdir()).resolve()
        links = []
        try:
            remote = base / "remote seed"
            remote.mkdir()
            installer._run([git, "init", "-b", "main", remote])
            installer._git(git, remote, "config", "user.name", "Installer Fixture")
            installer._git(git, remote, "config", "user.email", "fixture@example.invalid")
            package = remote / installer.PDK_RELATIVE
            package.mkdir(parents=True)
            (package / "JNU_MWP_TFLN_PDK.lyt").write_text("fixture technology", encoding="utf-8")
            (package / "manifest.json").write_text('{"version":"V1.0"}', encoding="utf-8")
            (remote / "version.txt").write_text("one", encoding="utf-8")
            installer._git(git, remote, "add", ".")
            installer._git(git, remote, "commit", "-m", "Fixture initial")
            installer.PUBLIC_URL = str(remote)
            home = base / "用户 配置"
            linked = home / installer.PDK_RELATIVE
            links.append(linked)
            installer.install_public(home)
            checkout = home / "jnu_repositories/JNU_MWP_TFLN_PDK"
            assert linked.resolve() == (checkout / installer.PDK_RELATIVE).resolve()
            installer.install_public(home)
            (remote / "version.txt").write_text("two", encoding="utf-8")
            installer._git(git, remote, "add", ".")
            installer._git(git, remote, "commit", "-m", "Fixture update")
            installer.install_public(home)
            assert (checkout / "version.txt").read_text() == "two"
            (checkout / "version.txt").write_text("user edit", encoding="utf-8")
            reject(lambda: installer.install_public(home), "本地修改")
            assert (checkout / "version.txt").read_text() == "user edit"
            (checkout / "version.txt").write_text("two", encoding="utf-8")
            installer._git(git, checkout, "switch", "-c", "work")
            reject(lambda: installer.install_public(home), "main 分支")
            installer._git(git, checkout, "switch", "main")
            installer._git(git, checkout, "remote", "set-url", "origin", str(base / "different remote"))
            reject(lambda: installer.install_public(home), "origin")
            installer._git(git, checkout, "remote", "set-url", "origin", str(remote))
            installer._git(git, checkout, "config", "user.name", "Installer Fixture")
            installer._git(git, checkout, "config", "user.email", "fixture@example.invalid")
            installer._git(git, checkout, "commit", "--allow-empty", "-m", "Unpublished fixture")
            reject(lambda: installer.install_public(home), "未发布提交")
            legacy = base / "legacy"
            original = legacy / installer.PDK_RELATIVE
            original.mkdir(parents=True)
            keep = original / "keep.txt"
            keep.write_text("keep original", encoding="utf-8")
            reject(lambda: installer.install_public(legacy), "已有 TFLN 安装")
            assert keep.read_text() == "keep original"
            print("INSTALLER_PASS: install/reinstall/fast-forward; dirty/branch/remote/ahead/legacy guards", flush=True)
            private_home = verify_private(git, base)

            import pya
            if hasattr(pya, "Application"):
                app = pya.Application.instance()
                gui_home = base / "GUI 配置"
                links.append(gui_home / installer.PDK_RELATIVE)
                observed = []
                real_install = installer.install_public

                def gui_task(actual_home, notify):
                    observed.append(actual_home)
                    return real_install(gui_home, notify)

                installer.install_public = gui_task
                dialog = installer.show_installer(execute=False, auto_start=True)
                dialog.show()
                deadline = time.monotonic() + 20
                while dialog.busy and time.monotonic() < deadline:
                    app.process_events()
                    time.sleep(0.02)
                assert not dialog.busy and "安装/更新完成" in dialog.output.toPlainText()
                assert observed == [str(app.application_data_path())]
                assert (gui_home / installer.PDK_RELATIVE).resolve() == (gui_home / "jnu_repositories/JNU_MWP_TFLN_PDK" / installer.PDK_RELATIVE).resolve()
                dialog.close()
                print("INSTALLER_GUI_PASS: native KLayout directory detection, real Git worker and Qt timer", flush=True)
                real_private, real_activate = installer.install_private, installer.activate_private
                activation_threads = []
                installer.install_private = lambda actual_home, notify: real_private(private_home, notify)

                def activate(actual_home, repository):
                    activation_threads.append(threading.current_thread() is threading.main_thread())
                    return real_activate(private_home, repository)

                installer.activate_private = activate
                private_dialog = installer.show_installer(execute=False, auto_start=True, mode="private")
                private_dialog.show()
                deadline = time.monotonic() + 20
                while private_dialog.busy and time.monotonic() < deadline:
                    app.process_events()
                    time.sleep(0.02)
                assert not private_dialog.busy and "白盒器件库安装/更新完成" in private_dialog.output.toPlainText()
                assert activation_threads == [True]
                assert private_dialog.local_button.isEnabled()
                private_dialog.close()
                print("PRIVATE_INSTALLER_GUI_PASS: Git worker, main-thread GDS validation and local-import option", flush=True)
        finally:
            # 仅移除测试临时目录中的联接，先核验目标，防止递归清理跨入别处。
            for linked in links:
                if os.path.lexists(linked):
                    assert linked.parent.resolve().is_relative_to(base)
                    assert linked.resolve().is_relative_to(base)
                    if os.name == "nt":
                        os.rmdir(linked)
                    else:
                        linked.unlink()


if __name__ == "__main__":
    main()
