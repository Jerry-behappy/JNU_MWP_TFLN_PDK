# -*- coding: utf-8 -*-
# 时间: 2026-10
"""用临时 Git 仓库验证安装、更新和保留原文件；原生 KLayout 再验收 Qt 后台任务。"""
import importlib.util
import os
from pathlib import Path
import tempfile
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
