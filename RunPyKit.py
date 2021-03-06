# coding: utf-8

################################################################################
# MIT License

# Copyright (c) 2020-2021 hrp/hrpzcf <hrpzcf@foxmail.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################
# Formatted with black 21.9b0
################################################################################

import os
import sys
from platform import machine, platform

from chardet import detect
from fastpip.fastpip import parse_package_names
from PyQt5.QtCore import (
    QRegExp,
    QSize,
    Qt,
    pyqtSignal,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QIcon,
    QMovie,
    QRegExpValidator,
)
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from information import VERSION
from interface import *
from library import *
from library.libcip import ImportInspector
from library.libm import PyEnv
from library.libpyi import PyiTool
from library.libqt import QLineEditMod, QTextEditMod


class MainInterface(Ui_main_interface, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"AwesPyKit - {VERSION}")
        self.connect_signals_slots()

    def connect_signals_slots(self):
        self.action_about.triggered.connect(self._show_about)
        self.pb_pkg_mgr.clicked.connect(win_package_mgr.show)
        self.pb_pyi_tool.clicked.connect(win_pyi_tool.show)
        self.pb_index_mgr.clicked.connect(win_index_mgr.show)
        self.pb_pkg_dload.clicked.connect(win_dload_pkg.show)

    def closeEvent(self, event):
        if (
            win_package_mgr.repo.is_empty()
            and win_pyi_tool.repo.is_empty()
            and win_dload_pkg.repo.is_empty()
        ):
            event.accept()
        else:
            role = NewMessageBox(
                "??????",
                "?????????????????????...",
                QMessageBox.Warning,
                (("accept", "????????????"), ("reject", "??????")),
            ).exec_()
            if role == 0:
                win_package_mgr.repo.kill_all()
                win_pyi_tool.repo.kill_all()
                event.accept()
            else:
                event.ignore()

    @staticmethod
    def _show_about():
        try:
            with open("help/About.html", encoding="utf-8") as help_html:
                info = help_html.read().replace("0.0.0", VERSION)
                icon = QMessageBox.Information
        except Exception:
            info = '"??????"????????????(help/About.html)????????????'
            icon = QMessageBox.Critical
        about_panel = NewMessageBox("??????", info, icon)
        about_panel.exec_()


class PackageManagerWindow(Ui_package_manager, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_other_widgets()
        self.connect_signals_slots()
        self.env_list = get_pyenv_list(load_conf("pths"))
        self.path_list = [env.env_path for env in self.env_list]
        self.cur_pkgs_info = {}
        self._reverseds = [True, True, True, True]
        self.selected_env_index = 0
        self.repo = ThreadRepo(500)
        self._normal_size = self.size()

    def _setup_other_widgets(self):
        self.tw_installed_info.setColumnWidth(0, 220)
        horiz_head = self.tw_installed_info.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.Interactive)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(3, QHeaderView.Stretch)
        self.loading_mov = QMovie(os.path.join(resources_path, "loading.gif"))
        self.loading_mov.setScaledSize(QSize(18, 18))

    def show(self):
        self.resize(self._normal_size)
        super().show()
        self.list_widget_pyenvs_update()
        self.lw_env_list.setCurrentRow(self.selected_env_index)

    @staticmethod
    def _stop_before_close():
        return not NewMessageBox(
            "??????",
            "??????????????????????????????\n???????????????????????????????????????????????????????????????",
            QMessageBox.Question,
            (("accept", "?????????????????????"), ("reject", "??????")),
        ).exec_()

    def closeEvent(self, event):
        if not self.repo.is_empty():
            if self._stop_before_close():
                self.repo.stop_all()
                self._clear_pkgs_table_widget()
                save_conf(self.path_list, "pths")
                event.accept()
            else:
                event.ignore()

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def show_loading(self, text):
        self.lb_loading_tip.clear()
        self.lb_loading_tip.setText(text)
        self.lb_loading_gif.clear()
        self.lb_loading_gif.setMovie(self.loading_mov)
        self.loading_mov.start()

    def hide_loading(self):
        self.loading_mov.stop()
        self.lb_loading_gif.clear()
        self.lb_loading_tip.clear()

    def connect_signals_slots(self):
        self.btn_autosearch.clicked.connect(self.auto_search_env)
        self.btn_delselected.clicked.connect(self.del_selected_py_env)
        self.btn_addmanully.clicked.connect(self.add_py_path_manully)
        self.cb_check_uncheck_all.clicked.connect(self.select_all_or_cancel_all)
        self.lw_env_list.itemPressed.connect(lambda: self.get_pkgs_info(0))
        self.btn_check_for_updates.clicked.connect(self.check_cur_pkgs_for_updates)
        self.btn_install_package.clicked.connect(win_ins_pkg.show)
        self.btn_install_package.clicked.connect(self.set_win_install_package_envinfo)
        self.btn_uninstall_package.clicked.connect(self.uninstall_pkgs)
        self.btn_upgrade_package.clicked.connect(self.upgrade_pkgs)
        self.btn_upgrade_all.clicked.connect(self.upgrade_all_pkgs)
        self.tw_installed_info.horizontalHeader().sectionClicked[int].connect(
            self._sort_by_column
        )
        self.tw_installed_info.clicked.connect(self._show_tip_num_selected)
        self.cb_check_uncheck_all.clicked.connect(self._show_tip_num_selected)
        win_ins_pkg.pb_do_install.clicked.connect(self.install_pkgs)

    def set_win_install_package_envinfo(self):
        if self.env_list:
            win_ins_pkg.le_target_env.setText(
                str(self.env_list[self.selected_env_index])
            )

    def _show_tip_num_selected(self):
        self.lb_num_selected_items.setText(
            f"?????????????????????{len(self.indexs_of_selected_rows())}"
        )

    def list_widget_pyenvs_update(self):
        row_size = QSize(0, 28)
        cur_py_env_index = self.lw_env_list.currentRow()
        self.lw_env_list.clear()
        for env in self.env_list:
            item = QListWidgetItem(str(env))
            item.setSizeHint(row_size)
            self.lw_env_list.addItem(item)
        if cur_py_env_index != -1:
            self.lw_env_list.setCurrentRow(cur_py_env_index)

    def table_widget_pkgs_info_update(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(len(self.cur_pkgs_info))
        color_green = QColor(0, 170, 0)
        color_red = QColor(255, 0, 0)
        color_gray = QColor(243, 243, 243)
        for rowind, pkg_name in enumerate(self.cur_pkgs_info):
            even_num_row = rowind % 2
            item = QTableWidgetItem(pkg_name)
            self.tw_installed_info.setItem(rowind, 0, item)
            if not even_num_row:
                item.setBackground(color_gray)
            for colind, item_text in enumerate(
                self.cur_pkgs_info.get(pkg_name, ["", "", ""])
            ):
                item = QTableWidgetItem(item_text)
                if colind == 2:
                    if item_text in ("????????????", "????????????", "????????????"):
                        item.setForeground(color_green)
                    elif item_text in ("????????????", "????????????", "????????????"):
                        item.setForeground(color_red)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                if not even_num_row:
                    item.setBackground(color_gray)
                self.tw_installed_info.setItem(rowind, colind + 1, item)

    def _sort_by_column(self, colind):
        if colind == 0:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[0].lower(),
                    reverse=self._reverseds[colind],
                )
            )
        else:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[1][colind - 1],
                    reverse=self._reverseds[colind],
                )
            )
        self.table_widget_pkgs_info_update()
        self._reverseds[colind] = not self._reverseds[colind]

    def _clear_pkgs_table_widget(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def get_pkgs_info(self, no_connect):
        self.selected_env_index = self.lw_env_list.currentRow()
        if self.selected_env_index == -1:
            return None

        def do_get_pkgs_info():
            pkgs_info = self.env_list[self.selected_env_index].pkgs_info()
            self.cur_pkgs_info.clear()
            for pkg_info in pkgs_info:
                self.cur_pkgs_info[pkg_info[0]] = [pkg_info[1], "", ""]

        thread_get_pkgs_info = NewTask(do_get_pkgs_info)
        if not no_connect:
            thread_get_pkgs_info.at_start(
                self.lock_widgets,
                lambda: self.show_loading("?????????????????????..."),
            )
            thread_get_pkgs_info.at_finish(
                self.table_widget_pkgs_info_update,
                self.hide_loading,
                self.release_widgets,
            )
        thread_get_pkgs_info.start()
        self.repo.put(thread_get_pkgs_info, 1)
        return thread_get_pkgs_info

    def indexs_of_selected_rows(self):
        row_indexs = []
        for item in self.tw_installed_info.selectedItems():
            row_index = item.row()
            if row_index not in row_indexs:
                row_indexs.append(row_index)
        return row_indexs

    def select_all_or_cancel_all(self):
        if self.cb_check_uncheck_all.isChecked():
            self.tw_installed_info.selectAll()
        else:
            self.tw_installed_info.clearSelection()


    def auto_search_env(self):
        def search_env():
            for _path in all_py_paths():
                _path = _check_venv(_path)
                if _path.lower() in path_list_lower:
                    continue
                try:
                    env = PyEnv(_path)
                except Exception:
                    continue
                self.env_list.append(env)
                self.path_list.append(env.env_path)

        path_list_lower = [p.lower() for p in self.path_list]
        thread_search_envs = NewTask(search_env)
        thread_search_envs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("????????????Python????????????..."),
        )
        thread_search_envs.at_finish(
            self._clear_pkgs_table_widget,
            self.list_widget_pyenvs_update,
            self.hide_loading,
            self.release_widgets,
            lambda: save_conf(self.path_list, "pths"),
        )
        thread_search_envs.start()
        self.repo.put(thread_search_envs, 0)

    def del_selected_py_env(self):
        cur_index = self.lw_env_list.currentRow()
        if cur_index == -1:
            return
        del self.env_list[cur_index]
        del self.path_list[cur_index]
        self.lw_env_list.removeItemWidget(self.lw_env_list.takeItem(cur_index))
        self._clear_pkgs_table_widget()
        save_conf(self.path_list, "pths")

    def add_py_path_manully(self):
        input_dialog = NewInputDialog(
            self,
            560,
            0,
            "??????Python??????",
            "?????????Python???????????????",
        )
        _path, ok = input_dialog.get_text()
        if not (ok and _path):
            return
        if not check_py_path(_path):
            return NewMessageBox(
                "??????",
                "?????????Python???????????????",
                QMessageBox.Warning,
            ).exec_()
        _path = _check_venv(os.path.normpath(os.path.abspath(_path)))
        if _path.lower() in [p.lower() for p in self.path_list]:
            return NewMessageBox(
                "??????",
                "????????????Python??????????????????",
                QMessageBox.Warning,
            ).exec_()
        try:
            env = PyEnv(_path)
            self.env_list.append(env)
            self.path_list.append(env.env_path)
        except Exception:
            return NewMessageBox(
                "??????",
                "?????????????????????????????????????????????????????????????????????~",
                QMessageBox.Warning,
            ).exec_()
        self.list_widget_pyenvs_update()
        save_conf(self.path_list, "pths")

    def check_cur_pkgs_for_updates(self):
        if self.tw_installed_info.rowCount() == 0:
            return
        cur_row = self.lw_env_list.currentRow()
        if cur_row == -1:
            return
        thread_get_info = self.get_pkgs_info(no_connect=1)

        def do_get_outdated():
            thread_get_info.wait()
            outdateds = self.env_list[cur_row].outdated()
            for outdated_info in outdateds:
                self.cur_pkgs_info.setdefault(outdated_info[0], ["", "", ""])[
                    1
                ] = outdated_info[2]

        thread_get_outdated = NewTask(do_get_outdated)
        thread_get_outdated.at_start(
            self.lock_widgets,
            lambda: self.show_loading("??????????????????..."),
        )
        thread_get_outdated.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_get_outdated.start()
        self.repo.put(thread_get_outdated, 1)

    def lock_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_env_list,
            self.tw_installed_info,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_upgrade_package,
            self.btn_upgrade_all,
            self.lb_num_selected_items,
        ):
            widget.setEnabled(False)

    def release_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_env_list,
            self.tw_installed_info,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_upgrade_package,
            self.btn_upgrade_all,
            self.lb_num_selected_items,
        ):
            widget.setEnabled(True)

    def install_pkgs(self):
        if not self.env_list:
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        package_to_be_installed = win_ins_pkg.package_names
        if not package_to_be_installed:
            return
        conf = win_ins_pkg.conf_dict
        install_pre = conf.get("include_pre", False)
        user = conf.get("install_for_user", False)
        use_index_url = conf.get("use_index_url", False)
        index_url = conf.get("index_url", "") if use_index_url else ""

        def do_install():
            for name, code in loop_install(
                cur_env,
                package_to_be_installed,
                pre=install_pre,
                user=user,
                index_url=index_url,
            ):
                item = self.cur_pkgs_info.setdefault(name, ["", "", ""])
                if not item[0]:
                    item[0] = "- N/A -"
                item[2] = "????????????" if code else "????????????"

        thread_install_pkgs = NewTask(do_install)
        thread_install_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("????????????..."),
        )
        thread_install_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_install_pkgs.start()
        self.repo.put(thread_install_pkgs, 0)

    def uninstall_pkgs(self):
        pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        pkg_names = [pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        names_text = (
            "\n".join(pkg_names)
            if len(pkg_names) <= 10
            else "\n".join(("\n".join(pkg_names[:10]), "......"))
        )
        uninstall_msg_box = QMessageBox(
            QMessageBox.Question, "??????", f"???????????????\n{names_text}"
        )
        uninstall_msg_box.addButton("??????", QMessageBox.AcceptRole)
        reject = uninstall_msg_box.addButton("??????", QMessageBox.RejectRole)
        uninstall_msg_box.setDefaultButton(reject)
        if uninstall_msg_box.exec_() != 0:
            return

        def do_uninstall():
            for pkg_name, code in loop_uninstall(cur_env, pkg_names):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code:
                    item[0] = "- N/A -"
                item[2] = "????????????" if code else "????????????"

        thread_uninstall_pkgs = NewTask(do_uninstall)
        thread_uninstall_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("????????????..."),
        )
        thread_uninstall_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_uninstall_pkgs.start()
        self.repo.put(thread_uninstall_pkgs, 0)

    def upgrade_pkgs(self):
        pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        pkg_names = [pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        names_text = (
            "\n".join(pkg_names)
            if len(pkg_names) <= 10
            else "\n".join(("\n".join(pkg_names[:10]), "......"))
        )
        if (
            NewMessageBox(
                "??????",
                f"???????????????\n{names_text}",
                QMessageBox.Question,
                (("accept", "??????"), ("reject", "??????")),
            ).exec_()
            != 0
        ):
            return

        def do_upgrade():
            for pkg_name, code in loop_install(cur_env, pkg_names, upgrade=1):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code and item[1]:
                    item[0] = item[1]
                item[2] = "????????????" if code else "????????????"

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("????????????..."),
        )
        thread_upgrade_pkgs.at_finish(
            self.table_widget_pkgs_info_update, self.hide_loading, self.release_widgets
        )
        thread_upgrade_pkgs.start()
        self.repo.put(thread_upgrade_pkgs, 0)

    def upgrade_all_pkgs(self):
        upgradeable = [item[0] for item in self.cur_pkgs_info.items() if item[1][1]]
        if not upgradeable:
            NewMessageBox(
                "??????",
                "????????????????????????????????????????????????",
                QMessageBox.Information,
            ).exec_()
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        names_text = (
            "\n".join(upgradeable)
            if len(upgradeable) <= 10
            else "\n".join(("\n".join(upgradeable[:10]), "......"))
        )
        if (
            NewMessageBox(
                "????????????",
                f"???????????????\n{names_text}",
                QMessageBox.Question,
                (("accept", "??????"), ("reject", "??????")),
            ).exec_()
            != 0
        ):
            return

        def do_upgrade():
            for pkg_name, code in loop_install(cur_env, upgradeable, upgrade=1):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code and item[1]:
                    item[0] = item[1]
                item[2] = "????????????" if code else "????????????"

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("????????????..."),
        )
        thread_upgrade_pkgs.at_finish(
            self.table_widget_pkgs_info_update, self.hide_loading, self.release_widgets
        )
        thread_upgrade_pkgs.start()
        self.repo.put(thread_upgrade_pkgs, 0)


class AskFilePath:
    def load_from_text(self, last_path):
        text_path, _ = QFileDialog.getOpenFileName(
            self, "??????????????????", last_path, "???????????? (*.txt)"
        )
        if not text_path:
            return "", ""
        try:
            with open(text_path, "rb") as fobj:
                encoding = detect(fobj.read()).get("encoding", "utf-8")
            with open(text_path, "rt", encoding=encoding) as fobj:
                return fobj.read(), os.path.dirname(text_path)
        except Exception as reason:
            NewMessageBox(
                "??????",
                f"?????????????????????\n{str(reason)}",
                QMessageBox.Critical,
            ).exec_()
            return "", ""

    def save_as_text_file(self, data, last_path):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "????????????", last_path, "???????????? (*.txt)"
        )
        if not save_path:
            return ""
        try:
            with open(save_path, "wt", encoding="utf-8") as fobj:
                fobj.writelines(data)
        except Exception as reason:
            return NewMessageBox(
                "??????",
                f"?????????????????????\n{str(reason)}",
            ).exec_()
        return os.path.dirname(save_path)

    def get_dir_path(self, last_path):
        _path = QFileDialog.getExistingDirectory(self, "????????????", last_path)
        if _path:
            return os.path.normpath(_path)
        return ""


class InstallPackagesWindow(Ui_install_package, QWidget, AskFilePath):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_other_widgets()
        self.conf_dict = load_conf("insp")
        self.last_path = self.conf_dict.get("last_path", ".")
        self.package_names = None
        self.connect_signals_slots()

    def _setup_other_widgets(self):
        self.pte_package_names = QTextEditMod(
            file_filter={".whl"},
        )
        self.splitter.replaceWidget(0, self.pte_package_names)
        self.pte_package_names_old.deleteLater()
        self.pte_package_names.show()

    def save_package_names(self):
        data = self.pte_package_names.toPlainText()
        if not data:
            return NewMessageBox(
                "??????",
                "???????????????????????????",
            ).exec_()
        last_path = self.save_as_text_file(data, self.last_path)
        if last_path:
            self.last_path = last_path
            self.conf_dict["last_path"] = last_path

    def load_package_names(self):
        text, fpath = self.load_from_text(self.last_path)
        if text:
            self.pte_package_names.setPlainText(text)
            self.package_names = list()
            names = text.splitlines(keepends=False)
            for name in names:
                if name and (name not in self.package_names):
                    self.package_names.append(name)
        if fpath:
            self.last_path = fpath
            self.conf_dict["last_path"] = fpath

    def apply_default_conf(self):
        self.cb_including_pre.setChecked(self.conf_dict.get("include_pre", False))
        self.cb_install_for_user.setChecked(
            self.conf_dict.get("install_for_user", False)
        )
        self.cb_use_index_url.setChecked(self.conf_dict.get("use_index_url", False))
        self.le_use_index_url.setText(self.conf_dict.get("index_url", ""))
        if self.cb_use_index_url.isChecked():
            self.le_use_index_url.setEnabled(True)
        else:
            self.le_use_index_url.setEnabled(False)

    def store_default_conf(self):
        text = self.pte_package_names.toPlainText()
        if text:
            self.package_names = [
                name for name in text.splitlines(keepends=False) if name
            ]
        self.conf_dict["include_pre"] = self.cb_including_pre.isChecked()
        self.conf_dict["install_for_user"] = self.cb_install_for_user.isChecked()
        self.conf_dict["use_index_url"] = self.cb_use_index_url.isChecked()
        self.conf_dict["index_url"] = self.le_use_index_url.text()

    def closeEvent(self, event):
        event.accept()
        self.store_default_conf()
        save_conf(self.conf_dict, "insp")

    def show(self):
        super().show()
        self.apply_default_conf()

    def connect_signals_slots(self):
        self.pb_do_install.clicked.connect(self.store_default_conf)
        self.pb_do_install.clicked.connect(self.close)
        self.pb_save_as_text.clicked.connect(self.save_package_names)
        self.pb_load_from_text.clicked.connect(self.load_package_names)
        self.cb_use_index_url.clicked.connect(self.set_le_use_index_url)

    def set_target_env_info(self, env):
        self.le_target_env.setText(str(env))

    def set_le_use_index_url(self):
        self.le_use_index_url.setEnabled(self.cb_use_index_url.isChecked())


class IndexUrlManagerWindow(Ui_index_url_manager, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._urls_dict = load_conf("urls")
        self.connect_signals_slots()
        self._normal_size = self.size()

    def show(self):
        self.resize(self._normal_size)
        super().show()
        self._list_widget_urls_update()

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    @staticmethod
    def _widget_for_list_item(url):
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(""))
        item_layout.addWidget(QLabel(url))
        item_layout.setStretch(0, 2)
        item_layout.setStretch(1, 8)
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        return item_widget

    def _list_widget_urls_update(self):
        self.li_indexurls.clear()
        for name, url in self._urls_dict.items():
            item_widget = self._widget_for_list_item(url)
            li_item = QListWidgetItem()
            li_item.setSizeHint(QSize(560, 42))
            li_item.setText(name)
            self.li_indexurls.addItem(li_item)
            self.li_indexurls.setItemWidget(li_item, item_widget)
        if self.li_indexurls.count():
            self.li_indexurls.setCurrentRow(0)

    def connect_signals_slots(self):
        self.btn_clearle.clicked.connect(self._clear_line_edit)
        self.btn_saveurl.clicked.connect(self._save_index_urls)
        self.btn_delurl.clicked.connect(self._del_index_url)
        self.li_indexurls.clicked.connect(self._set_url_line_edit)
        self.btn_setindex.clicked.connect(self._set_global_index_url)
        self.btn_refresh_effective.clicked.connect(self._display_effective_url)

    def _set_url_line_edit(self):
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            return
        text = item.text()
        self.le_urlname.setText(text)
        self.le_indexurl.setText(self._urls_dict.get(text, ""))

    def _clear_line_edit(self):
        self.le_urlname.clear()
        self.le_indexurl.clear()

    def _check_name_url(self, name, url):
        error = lambda m: NewMessageBox("??????", m, QMessageBox.Critical)
        if not name:
            error = error("?????????????????????")
        elif not url:
            error = error("?????????????????????")
        elif not check_index_url(url):
            error = error("???????????????????????????")
        elif name in self._urls_dict:
            error = error(f"??????'{name}'????????????")
        else:
            return True
        # exec_???????????????????????????????????????
        # ??????????????????????????????????????????
        # ??????1????????????????????????????????????????????????????????????0
        # ???????????????????????????????????????????????????0
        return error.exec_()

    def _save_index_urls(self):
        name = self.le_urlname.text()
        url = self.le_indexurl.text()
        if self._check_name_url(name, url):
            self._urls_dict[name] = url
        self._list_widget_urls_update()
        save_conf(self._urls_dict, "urls")

    def _del_index_url(self):
        last_selected = self.li_indexurls.currentRow()
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            NewMessageBox(
                "??????",
                "???????????????????????????????????????",
            ).exec_()
            return
        del self._urls_dict[item.text()]
        self._list_widget_urls_update()
        items_num = self.li_indexurls.count()
        if items_num:  # ??????item???????????????0
            if last_selected == -1:
                self.li_indexurls.setCurrentRow(0)
            else:
                should_be_selected = (
                    0
                    if last_selected - 1 < 0
                    else last_selected
                    if last_selected < items_num
                    else last_selected - 1
                )
                self.li_indexurls.setCurrentRow(should_be_selected)
        save_conf(self._urls_dict, "urls")

    @staticmethod
    def _get_cur_env():
        """
        ????????????????????????????????????Python?????????????????????PyEnv????????????????????????
        ???????????????????????????PATH????????????Python?????????????????????????????????????????????None???
        """
        saved_paths = load_conf("pths")
        warn_box = lambda m: NewMessageBox(
            "??????",
            m,
            QMessageBox.Warning,
        ).exec_()
        if not saved_paths:
            return PyEnv(cur_py_path())
        for _path in saved_paths:
            try:
                return PyEnv(_path)
            except Exception:
                continue
        else:
            warn_box("????????????Python???????????????'????????????'?????????Python?????????")
        return

    def _set_global_index_url(self):
        url = self.le_indexurl.text()
        warn_box = lambda m: NewMessageBox("??????", m, QMessageBox.Warning)
        if not url:
            warn_box = warn_box("???????????????????????????????????????????????????")
        elif not check_index_url(url):
            warn_box = warn_box("????????????????????????pip????????????????????????")
        else:
            env = self._get_cur_env()
            if not env:
                warn_box = warn_box(
                    "?????????Python???????????????????????????????????????\n??????'????????????'?????????Python?????????",
                )
            elif env.set_global_index(url):
                warn_box = NewMessageBox("??????", f"????????????????????????????????????\n{url}")
            else:
                warn_box = warn_box(
                    "?????????Python?????????????????????????????????????????????\n??????'????????????'?????????Python?????????",
                )
        warn_box.exec_()

    def _display_effective_url(self):
        env = self._get_cur_env()
        if not env:
            self.le_effectiveurl.setText(
                "?????????Python???????????????????????????????????????????????????",
            )
            return
        self.le_effectiveurl.setText(
            env.get_global_index() or "?????????Python?????????????????????????????????????????????"
        )


class PyinstallerToolWindow(Ui_pyinstaller_tool, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget_group = (
            self.tab_project_files,
            self.tab_build_control,
            self.tab_file_ver_info,
            self.tab_advanced_setup,
            self.pb_select_py_env,
            self.pb_reinstall_pyi,
            self.cb_log_level,
            self.le_exefile_specfile_name,
            self.pb_check_imports,
            self.pb_gen_executable,
        )
        self.le_group_vers = (
            self.le_file_version_0,
            self.le_file_version_1,
            self.le_file_version_2,
            self.le_file_version_3,
            self.le_product_version_0,
            self.le_product_version_1,
            self.le_product_version_2,
            self.le_product_version_3,
        )
        self._setup_other_widgets()
        self.repo = ThreadRepo(500)
        self._stored_conf = {}
        self.toolwin_env = None
        self.pyi_tool = PyiTool()
        self.set_platform_info()
        self.pyi_running_mov = QMovie(os.path.join(resources_path, "loading.gif"))
        self.pyi_running_mov.setScaledSize(QSize(18, 18))
        self.connect_signals_slots()
        self._normal_size = self.size()

    def closeEvent(self, event):
        if not self.repo.is_empty():
            NewMessageBox(
                "??????",
                "?????????????????????????????????????????????????????????????????????\n??????????????????????????????\
????????????????????????????????????????????????",
                QMessageBox.Warning,
            ).exec_()
        self.store_state_of_widgets()
        save_conf(self._stored_conf, "pyic")
        event.accept()

    def show(self):
        self.resize(self._normal_size)
        super().show()
        if self.repo.is_empty():
            self.apply_stored_config()
            self.pyi_tool.initialize(
                self._stored_conf.get("env_path", ""),
                self._stored_conf.get("project_root", os.getcwd()),
            )
            self.set_pyi_info()

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def _setup_other_widgets(self):
        # ?????????????????????LineEdit??????
        self.le_program_entry = QLineEditMod("file", {".py", ".pyc", ".pyw", ".spec"})
        self.le_program_entry.setToolTip(
            "???????????????????????????????????????(*.py *.pyw *.pyc *.spec)??????????????????\n"
            "???????????????SPEC???????????????????????????????????????????????????????????????????????????\n"
            "?????????????????????????????????????????????"
        )
        self.horizontalLayout_3.replaceWidget(
            self.le_program_entry_old, self.le_program_entry
        )
        self.le_program_entry_old.deleteLater()
        # ????????????????????????????????????TextEdit??????
        self.te_module_search_path = QTextEditMod("dir")
        self.te_module_search_path.setToolTip(
            "?????????????????????????????????????????????????????????\n??????PYINSTALLER????????????????????????\
????????????????????????????????????????????????"
        )
        self.verticalLayout_3.replaceWidget(
            self.te_module_search_path_old, self.te_module_search_path
        )
        self.te_module_search_path_old.deleteLater()
        # ????????????????????????????????????LineEdit??????
        self.te_other_data = QTextEditMod("file")
        self.te_other_data.setToolTip(
            """???????????????????????????????????????????????????????????????????????????????????????????????????\n"""
            """?????????????????????????????????????????????????????????????????????????????????????????????????????????\
????????????????????????????????????"""
        )
        self.verticalLayout_4.replaceWidget(self.te_other_data_old, self.te_other_data)
        self.te_other_data_old.deleteLater()
        # ??????????????????????????????LineEdit??????
        self.le_file_icon_path = QLineEditMod("file", {".ico", ".icns"})
        self.le_file_icon_path.setToolTip(
            "?????????exe???????????????????????????\n??????.ico???.icns????????????????????????????????????????????????????????????"
        )
        self.horizontalLayout_11.replaceWidget(
            self.le_file_icon_path_old, self.le_file_icon_path
        )
        self.le_file_icon_path_old.deleteLater()
        reg_exp_val1 = QRegExpValidator(QRegExp(r'[^\\/:*?"<>|]*'))
        self.le_exefile_specfile_name.setValidator(reg_exp_val1)
        reg_exp_val2 = QRegExpValidator(QRegExp(r"[0-9]*"))
        for line_edit in self.le_group_vers:
            line_edit.setValidator(reg_exp_val2)
        self.le_runtime_tmpdir.setValidator(reg_exp_val1)

    def connect_signals_slots(self):
        self.pyi_tool.completed.connect(self.task_completion_tip)
        self.pyi_tool.stdout.connect(self.te_pyi_out_stream.append)
        self.pb_select_py_env.clicked.connect(win_chenviron.show)
        self.le_program_entry.textChanged.connect(self.set_le_project_root)
        self.pb_select_module_search_path.clicked.connect(
            self.set_te_module_search_path
        )
        self.pb_select_program_entry.clicked.connect(self.set_le_program_entry)
        self.pb_up_level_root.clicked.connect(lambda: self.project_root_level("up"))
        self.pb_reset_root_level.clicked.connect(
            lambda: self.project_root_level("reset")
        )
        self.pb_clear_module_search_path.clicked.connect(
            self.te_module_search_path.clear
        )
        self.pb_select_other_data.clicked.connect(self.set_te_other_data)
        self.pb_clear_other_data.clicked.connect(self.te_other_data.clear)
        self.pb_select_file_icon.clicked.connect(self.set_le_file_icon_path)
        self.pb_select_spec_dir.clicked.connect(self.set_le_spec_dir)
        self.pb_select_temp_working_dir.clicked.connect(self.set_le_temp_working_dir)
        self.pb_select_output_dir.clicked.connect(self.set_le_output_dir)
        self.pb_select_upx_search_path.clicked.connect(self.set_le_upx_search_path)
        self.pb_gen_executable.clicked.connect(self.build_executable)
        self.pb_reinstall_pyi.clicked.connect(self.reinstall_pyi)
        self.pb_check_imports.clicked.connect(self.check_project_imports)
        win_check_imp.pb_install_all_missing.clicked.connect(
            lambda: self.install_missings(win_check_imp.all_missing_modules)
        )

    def check_project_imports(self):
        self.store_state_of_widgets()
        if not self.toolwin_env:
            NewMessageBox(
                "??????",
                "???????????????Python?????????",
                QMessageBox.Warning,
            ).exec_()
            return
        project_root = self._stored_conf.get("project_root", None)
        if not project_root:
            NewMessageBox(
                "??????",
                "???????????????????????????",
                QMessageBox.Warning,
            ).exec_()
            return
        if not os.path.isdir(project_root):
            NewMessageBox(
                "??????",
                "???????????????????????????",
                QMessageBox.Warning,
            ).exec_()
            return
        missings = list()

        def get_missing_imps():
            imp_missings = ImportInspector(
                self.toolwin_env.env_path, project_root
            ).missing_items()
            missings.append(tuple(imp_missings))

        thread_check_imp = NewTask(get_missing_imps)
        thread_check_imp.at_start(
            self.lock_widgets,
            lambda: self.show_running("??????????????????????????????????????????..."),
        )
        thread_check_imp.at_finish(
            self.hide_running,
            self.release_widgets,
            lambda: win_check_imp.set_env_info(self.toolwin_env),
            lambda: win_check_imp.checkimp_table_update(missings),
            win_check_imp.show,
        )
        thread_check_imp.start()
        self.repo.put(thread_check_imp, 1)

    def set_le_program_entry(self):
        selected_file = self._select_file_dir(
            "???????????????",
            self._stored_conf.get("project_root", ""),
            file_filter="???????????? (*.py *.pyc *.pyw *.spec)",
        )[0]
        if not selected_file:
            return
        self.le_program_entry.setText(selected_file)

    def set_le_project_root(self):
        root = os.path.dirname(self.le_program_entry.text())
        self.le_project_root.setText(root)
        self._stored_conf["project_root"] = root

    def set_te_module_search_path(self):
        selected_dir = self._select_file_dir(
            "????????????????????????", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.te_module_search_path.append(selected_dir)

    def set_te_other_data(self):
        selected_files = self._select_file_dir(
            "???????????????????????????", self._stored_conf.get("project_root", ""), mult=True
        )
        if not selected_files:
            return
        self.te_other_data.append("\n".join(selected_files))

    def set_le_file_icon_path(self):
        selected_file = self._select_file_dir(
            "???????????????????????????",
            self._stored_conf.get("project_root", ""),
            file_filter="???????????? (*.ico *.icns)",
        )[0]
        if not selected_file:
            return
        self.le_file_icon_path.setText(selected_file)

    def set_le_spec_dir(self):
        selected_dir = self._select_file_dir(
            "??????SPEC??????????????????",
            self._stored_conf.get("project_root", ""),
            cht="dir",
        )[0]
        if not selected_dir:
            return
        self.le_spec_dir.setText(selected_dir)

    def set_le_temp_working_dir(self):
        selected_dir = self._select_file_dir(
            "????????????????????????", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_temp_working_dir.setText(selected_dir)

    def set_le_output_dir(self):
        selected_dir = self._select_file_dir(
            "??????????????????????????????", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_output_dir.setText(selected_dir)

    def set_le_upx_search_path(self):
        selected_dir = self._select_file_dir(
            "??????UPX??????????????????", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_upx_search_path.setText(selected_dir)

    def _select_file_dir(
        self,
        title="",
        start="",
        cht="file",
        mult=False,
        file_filter="???????????? (*)",
    ):
        file_dir_paths = []
        if cht == "file" and mult:
            if not title:
                title = "???????????????"
            path_getter = QFileDialog.getOpenFileNames
        elif cht == "file" and not mult:
            if not title:
                title = "????????????"
            path_getter = QFileDialog.getOpenFileName
        elif cht == "dir":
            if not title:
                title = "???????????????"
            path_getter = QFileDialog.getExistingDirectory
        else:
            return file_dir_paths
        if cht == "file" and not mult:
            path = path_getter(self, title, start, file_filter)[0]
            if not path:
                file_dir_paths.append("")
            else:
                file_dir_paths.append(os.path.realpath(path))
        elif cht == "file" and mult:
            paths = path_getter(self, title, start, file_filter)[0]
            file_dir_paths.extend(os.path.realpath(path) for path in paths if path)
            if not file_dir_paths:
                file_dir_paths.append("")
        elif cht == "dir":
            path = path_getter(self, title, start)
            if not path:
                file_dir_paths.append("")
            else:
                file_dir_paths.append(os.path.realpath(path))
        return file_dir_paths

    def set_env_update_info(self):
        self.toolwin_env = win_chenviron.winch_envlist[
            win_chenviron.lw_env_list.currentRow()
        ]
        self.lb_py_info.setText(self.toolwin_env.py_info())
        self.pyi_tool.initialize(
            self.toolwin_env.env_path,
            self._stored_conf.get("project_root", os.getcwd()),
        )
        self.set_pyi_info()

    def apply_stored_config(self):
        if not self._stored_conf:
            self._stored_conf.update(load_conf("pyic"))
        self.le_program_entry.setText(self._stored_conf.get("program_entry", ""))
        self.le_project_root.setText(self._stored_conf.get("project_root", ""))
        self.te_module_search_path.setText(
            "\n".join(self._stored_conf.get("module_search_path", []))
        )
        self.te_other_data.setText(
            "\n".join(
                path_group[0] for path_group in self._stored_conf.get("other_data", [])
            )
        )
        self.le_file_icon_path.setText(self._stored_conf.get("file_icon_path", ""))
        pack_to_one = self._stored_conf.get("pack_to_one", "dir")
        if pack_to_one == "file":
            self.rb_pack_to_one_file.setChecked(True)
        else:
            self.rb_pack_to_one_dir.setChecked(True)
        self.cb_execute_with_console.setChecked(
            self._stored_conf.get("execute_with_console", True)
        )
        self.cb_without_confirm.setChecked(
            self._stored_conf.get("without_confirm", False)
        )
        self.cb_use_upx.setChecked(self._stored_conf.get("use_upx", False))
        self.cb_clean_before_build.setChecked(
            self._stored_conf.get("clean_before_build", True)
        )
        self.cb_write_info_to_exec.setChecked(
            self._stored_conf.get("write_file_info", False)
        )
        self.le_temp_working_dir.setText(self._stored_conf.get("temp_working_dir", ""))
        self.le_output_dir.setText(self._stored_conf.get("output_dir", ""))
        self.le_spec_dir.setText(self._stored_conf.get("spec_dir", ""))
        self.le_upx_search_path.setText(self._stored_conf.get("upx_search_path", ""))
        self.te_upx_exclude_files.setText(
            "\n".join(self._stored_conf.get("upx_exclude_files", []))
        )
        _path = self._stored_conf.get("env_path", "")
        if _path:
            try:
                self.toolwin_env = PyEnv(_path)
                self.lb_py_info.setText(self.toolwin_env.py_info())
            except Exception:
                pass
        self.le_exefile_specfile_name.setText(
            self._stored_conf.get("exefile_specfile_name", "")
        )
        self.cb_log_level.setCurrentText(self._stored_conf.get("log_level", "INFO"))
        self.set_file_ver_info_text()
        self.change_debug_options("set")
        self.le_runtime_tmpdir.setText(self._stored_conf.get("runtime_tmpdir", ""))

    def store_state_of_widgets(self):
        self._stored_conf["program_entry"] = self.le_program_entry.local_path
        self._stored_conf[
            "exefile_specfile_name"
        ] = self.le_exefile_specfile_name.text()
        project_root = self.le_project_root.text()
        self._stored_conf["project_root"] = project_root
        self._stored_conf["module_search_path"] = self.te_module_search_path.local_paths
        self._stored_conf["other_data"] = self._abs_rel_groups(project_root)
        self._stored_conf["file_icon_path"] = self.le_file_icon_path.local_path
        if self.rb_pack_to_one_file.isChecked():
            self._stored_conf["pack_to_one"] = "file"
        else:
            self._stored_conf["pack_to_one"] = "dir"
        self._stored_conf[
            "execute_with_console"
        ] = self.cb_execute_with_console.isChecked()
        self._stored_conf["without_confirm"] = self.cb_without_confirm.isChecked()
        self._stored_conf["use_upx"] = self.cb_use_upx.isChecked()
        self._stored_conf["clean_before_build"] = self.cb_clean_before_build.isChecked()
        self._stored_conf["write_file_info"] = self.cb_write_info_to_exec.isChecked()
        self._stored_conf["temp_working_dir"] = self.le_temp_working_dir.text()
        self._stored_conf["output_dir"] = self.le_output_dir.text()
        self._stored_conf["spec_dir"] = self.le_spec_dir.text()
        self._stored_conf["upx_search_path"] = self.le_upx_search_path.text()
        self._stored_conf["upx_exclude_files"] = [
            string
            for string in self.te_upx_exclude_files.toPlainText().split("\n")
            if string
        ]
        if self.toolwin_env is None:
            self._stored_conf["env_path"] = ""
        else:
            self._stored_conf["env_path"] = self.toolwin_env.env_path
        self._stored_conf["log_level"] = self.cb_log_level.currentText()
        self._stored_conf["file_ver_info"] = self.file_ver_info_text()
        self._stored_conf["debug_options"] = self.change_debug_options("get")
        self._stored_conf["runtime_tmpdir"] = self.le_runtime_tmpdir.text()

    def _abs_rel_groups(self, starting_point):
        """????????????????????????????????????????????????????????????????????????????????????"""
        other_data_local_paths = self.te_other_data.local_paths
        abs_rel_path_groups = []
        for abs_path in other_data_local_paths:
            try:
                rel_path = os.path.relpath(os.path.dirname(abs_path), starting_point)
            except Exception:
                continue
            abs_rel_path_groups.append((abs_path, rel_path))
        return abs_rel_path_groups

    def change_debug_options(self, opt):
        """?????????"?????????????????????"??????????????????????????????????????????????????????"""
        if opt == "get":
            return {
                "imports": self.cb_db_imports.isChecked(),
                "bootloader": self.cb_db_bootloader.isChecked(),
                "noarchive": self.cb_db_noarchive.isChecked(),
            }
        elif opt == "set":
            db = self._stored_conf.get("debug_options", {})
            self.cb_db_imports.setChecked(db.get("imports", False))
            self.cb_db_bootloader.setChecked(db.get("bootloader", False))
            self.cb_db_noarchive.setChecked(db.get("noarchive", False))

    def file_ver_info_text(self):
        file_vers = tuple(int(x.text() or 0) for x in self.le_group_vers[:4])
        prod_vers = tuple(int(x.text() or 0) for x in self.le_group_vers[4:])
        return {
            "$filevers$": str(file_vers),
            "$prodvers$": str(prod_vers),
            "$CompanyName$": self.le_company_name.text(),
            "$FileDescription$": self.le_file_description.text(),
            "$FileVersion$": ".".join(map(str, file_vers)),
            "$LegalCopyright$": self.le_legal_copyright.text(),
            "$OriginalFilename$": self.le_original_filename.text(),
            "$ProductName$": self.le_product_name.text(),
            "$ProductVersion$": ".".join(map(str, prod_vers)),
            "$LegalTrademarks$": self.le_legal_trademarks.text(),
        }

    def set_file_ver_info_text(self):
        info = self._stored_conf.get("file_ver_info", {})
        self.le_file_description.setText(info.get("$FileDescription$", ""))
        self.le_company_name.setText(info.get("$CompanyName$", ""))
        for ind, val in enumerate(info.get("$FileVersion$", "0.0.0.0").split(".")):
            self.le_group_vers[ind].setText(val)
        self.le_product_name.setText(info.get("$ProductName$", ""))
        for ind, val in enumerate(info.get("$ProductVersion$", "0.0.0.0").split(".")):
            self.le_group_vers[ind + 4].setText(val)
        self.le_legal_copyright.setText(info.get("$LegalCopyright$", ""))
        self.le_legal_trademarks.setText(info.get("$LegalTrademarks$", ""))
        self.le_original_filename.setText(info.get("$OriginalFilename$", ""))

    def set_pyi_info(self, dont_set_enable=False):
        # ??????????????? self.pyi_tool????????? self.pyi_tool ?????????????????????
        if self.toolwin_env:
            if not dont_set_enable:
                self.pb_reinstall_pyi.setEnabled(True)
            pyi_info = self.pyi_tool.pyi_info()
            if pyi_info == "0.0":
                self.pb_reinstall_pyi.setText("??????")
            else:
                self.pb_reinstall_pyi.setText("????????????")
            self.lb_pyi_info.setText(f"PYINSTALLER - {pyi_info}")
        else:
            self.lb_pyi_info.clear()
            self.pb_reinstall_pyi.setEnabled(False)

    def reinstall_pyi(self):
        # NewMessageBox???exec_????????????0????????????"??????"??????
        if NewMessageBox(
            "??????",
            "????????????PYINSTALLER??????",
            QMessageBox.Question,
            (("accept", "??????"), ("reject", "??????")),
        ).exec_():
            return
        if not self.toolwin_env:
            NewMessageBox(
                "??????",
                "?????????????????????Python?????????",
                QMessageBox.Warning,
            ).exec_()
            return

        def do_reinstall_pyi():
            self.toolwin_env.uninstall("pyinstaller")
            self.toolwin_env.install("pyinstaller", upgrade=1)
            self.set_pyi_info(dont_set_enable=True)

        thread_reinstall = NewTask(target=do_reinstall_pyi)
        thread_reinstall.at_start(
            self.lock_widgets,
            lambda: self.show_running("????????????PYINSTALLER..."),
        )
        thread_reinstall.at_finish(
            self.hide_running,
            self.release_widgets,
        )
        thread_reinstall.start()
        self.repo.put(thread_reinstall, 0)

    def set_platform_info(self):
        self.lb_platform_info.setText(f"{platform()}-{machine()}")

    def project_root_level(self, opt):
        if opt not in ("up", "reset"):
            return
        root = self.le_project_root.text()
        if not root:
            return
        if opt == "up":
            self.le_project_root.setText(os.path.dirname(root))
        elif opt == "reset":
            deep = self.le_program_entry.text()
            if not deep:
                return
            self.le_project_root.setText(os.path.dirname(deep))

    def _check_requireds(self):
        self.store_state_of_widgets()
        program_entry = self._stored_conf.get("program_entry", "")
        if not program_entry:
            NewMessageBox(
                "??????",
                "?????????????????????",
                QMessageBox.Critical,
            ).exec_()
            return False
        if not os.path.isfile(program_entry):
            NewMessageBox(
                "??????",
                "???????????????????????????",
                QMessageBox.Critical,
            ).exec_()
            return False
        icon_path = self._stored_conf.get("file_icon_path", "")
        if icon_path != "" and not os.path.isfile(icon_path):
            NewMessageBox(
                "??????",
                "??????????????????????????????",
                QMessageBox.Critical,
            ).exec_()
            return False
        return True

    def show_running(self, msg):
        self.lb_running_tip.setText(msg)
        self.lb_running_gif.setMovie(self.pyi_running_mov)
        self.pyi_running_mov.start()

    def hide_running(self):
        self.pyi_running_mov.stop()
        self.lb_running_gif.clear()
        self.lb_running_tip.clear()

    def lock_widgets(self):
        for widget in self.widget_group:
            widget.setEnabled(False)

    def release_widgets(self):
        for widget in self.widget_group:
            widget.setEnabled(True)
        self.hide_running()

    @staticmethod
    def task_completion_tip(retcode):
        if retcode == 0:
            NewMessageBox(
                "????????????",
                "?????????????????????????????????",
            ).exec_()
        else:
            NewMessageBox(
                "????????????",
                "??????????????????????????????????????????????????????",
                QMessageBox.Critical,
            ).exec_()

    def build_executable(self):
        if not self._check_requireds():
            return
        self.te_pyi_out_stream.clear()
        self.pyi_tool.initialize(
            self._stored_conf.get("env_path", ""),
            self._stored_conf.get("project_root", os.getcwd()),
        )
        if not self.pyi_tool.pyi_ready:
            NewMessageBox(
                "??????",
                "PYINSTALLER??????????????????????????????'??????'?????????PYINSTALLER????????????????????????",
                QMessageBox.Warning,
            ).exec_()
            return
        self.pyi_tool.prepare_cmd(self._stored_conf)
        self.handle = self.pyi_tool.handle()
        thread_build = NewTask(self.pyi_tool.execute_cmd)
        thread_build.at_start(
            self.lock_widgets,
            lambda: self.show_running("???????????????????????????..."),
        )
        thread_build.at_finish(self.hide_running, self.release_widgets)
        thread_build.start()
        self.repo.put(thread_build, 0)

    def install_missings(self, missings):
        if not missings:
            NewMessageBox(
                "??????",
                "???????????????????????????????????????",
            ).exec_()
            win_check_imp.close()
            return
        if NewMessageBox(
            "??????",
            "??????????????????????????????????????????Python???????????????",
            QMessageBox.Question,
            (("accept", "??????"), ("reject", "??????")),
        ).exec_():
            return

        def install_mis():
            for name in missings:
                self.toolwin_env.install(name)

        thread_ins_mis = NewTask(install_mis)
        thread_ins_mis.at_start(
            self.lock_widgets,
            lambda: self.show_running("????????????????????????..."),
            win_check_imp.close,
        )
        thread_ins_mis.at_finish(
            self.hide_running,
            self.release_widgets,
            lambda: NewMessageBox(
                "??????",
                "????????????????????????????????????????????????????????????",
                QMessageBox.Information,
            ).exec_(),
        )
        thread_ins_mis.start()
        self.repo.put(thread_ins_mis, 0)


class ChooseEnvWindow(Ui_choose_env, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connect_signals_slots()
        self._normal_size = self.size()

    def connect_signals_slots(self):
        self.lw_env_list.pressed.connect(self.close)

    def pyenv_list_update(self):
        row_size = QSize(0, 28)
        self.lw_env_list.clear()
        for env in self.winch_envlist:
            item = QListWidgetItem(str(env))
            item.setSizeHint(row_size)
            self.lw_env_list.addItem(item)

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def close(self):
        super().close()
        win_pyi_tool.set_env_update_info()

    def show(self):
        self.resize(self._normal_size)
        self.winch_envlist = get_pyenv_list(load_conf("pths"))
        super().show()
        self.pyenv_list_update()


class CheckImportsWindow(Ui_check_imports, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_other_widgets()
        self._normal_size = self.size()
        self.pb_confirm.clicked.connect(self.close)
        self.all_missing_modules = None

    def _setup_other_widgets(self):
        self.tw_missing_imports.setColumnWidth(0, 260)
        self.tw_missing_imports.setColumnWidth(1, 350)
        self.tw_missing_imports.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self.tw_missing_imports.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def show(self):
        self.resize(self._normal_size)
        super().show()

    def checkimp_table_update(self, missing_data):
        # missing_data: ((filepath, {imps...}, {missings...})...)
        if not missing_data:
            return
        missing_data, *_ = missing_data
        self.all_missing_modules = set()
        for *_, m in missing_data:
            self.all_missing_modules.update(m)
        self.tw_missing_imports.clearContents()
        self.tw_missing_imports.setRowCount(len(missing_data))
        for rowind, value in enumerate(missing_data):
            # value[0]???filepath???None?????????ImportInspector???
            # missing_items??????????????????????????????????????????????????????????????????
            if value[0] is None:
                break
            item0 = QTableWidgetItem(os.path.basename(value[0]))
            item1 = QTableWidgetItem("???".join(value[1]))
            item2 = QTableWidgetItem("???".join(value[2]))
            item0.setToolTip(value[0])
            item1.setToolTip("\n".join(value[1]))
            item2.setToolTip("\n".join(value[2]))
            self.tw_missing_imports.setItem(rowind, 0, item0)
            self.tw_missing_imports.setItem(rowind, 1, item1)
            self.tw_missing_imports.setItem(rowind, 2, item2)
        self.show()

    def set_env_info(self, env):
        if not env:
            return
        self.le_cip_cur_env.setText(str(env))


class DownloadPackageWindow(Ui_download_package, QWidget, AskFilePath):
    set_download_table = pyqtSignal(list)
    download_completed = pyqtSignal(str)
    download_status = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.config = load_conf("dlpc")
        self.env_paths = None
        self.environments = None
        self.connect_signals_slots()
        self.last_path = None
        self.repo = ThreadRepo(500)

    def connect_signals_slots(self):
        self.cb_use_index_url.clicked.connect(self.change_le_index_url)
        self.pb_load_from_text.clicked.connect(self.names_from_file)
        self.pb_save_as_text.clicked.connect(self.save_names_to_file)
        self.pb_save_to.clicked.connect(self.select_saved_dir)
        self.pb_clear_package_names.clicked.connect(self.pte_package_names.clear)
        self.pb_start_download.clicked.connect(self.start_download_package)
        self.download_status.connect(win_downloading.status_changed)
        self.set_download_table.connect(win_downloading.setup_table)
        self.download_completed.connect(self.check_download)
        self.pb_show_dl_list.clicked.connect(win_downloading.show)

    def change_le_index_url(self):
        self.le_index_url.setEnabled(self.cb_use_index_url.isChecked())

    def names_from_file(self):
        text, _path = self.load_from_text(self.last_path)
        if _path:
            self.last_path = _path
        if text:
            self.pte_package_names.setPlainText(text)

    def save_names_to_file(self):
        data = self.pte_package_names.toPlainText()
        _path = self.save_as_text_file(data, self.last_path)
        if _path:
            self.last_path = _path

    def select_saved_dir(self):
        dir_path = self.get_dir_path(self.last_path)
        if dir_path:
            self.last_path = dir_path
            self.le_save_to.setText(dir_path)

    def closeEvent(self, event):
        if self.repo.is_empty():
            self.store_config()
            save_conf(self.config, "dlpc")
        else:
            NewMessageBox(
                "??????",
                "??????????????????????????????????????????????????????????????????",
                QMessageBox.Warning,
            ).exec_()
        super().closeEvent(event)

    def show(self):
        super().show()
        if self.repo.is_empty():
            self.apply_config()

    def update_envpaths_and_combobox(self):
        if self.env_paths is None:
            self.env_paths = list()
        else:
            self.env_paths.clear()
        self.env_paths.extend(load_conf("pths"))
        self.environments = get_pyenv_list(self.env_paths)
        index = self.config.get("derived_from", 0)
        text_list = [str(e) for e in self.environments]
        if index < 0 or index >= len(text_list):
            index = 0
        self.cmb_derived_from.clear()
        self.cmb_derived_from.addItems(text_list)
        self.cmb_derived_from.setCurrentIndex(index)

    def store_config(self):
        self.config["package_names"] = [
            s for s in self.pte_package_names.toPlainText().split("\n") if s
        ]
        self.config["derived_from"] = self.cmb_derived_from.currentIndex()
        self.config["download_deps"] = self.cb_download_deps.isChecked()
        download_type = (
            "unlimited"
            if self.rb_unlimited.isChecked()
            else "no_binary"
            if self.rb_no_binary.isChecked()
            else "only_binary"
            if self.rb_only_binary.isChecked()
            else "prefer_binary"
        )
        self.config["download_type"] = download_type
        self.config["include_pre"] = self.cb_include_pre.isChecked()
        self.config[
            "ignore_requires_python"
        ] = self.cb_ignore_requires_python.isChecked()
        self.config["save_to"] = self.le_save_to.text()
        self.config["platform"] = [s for s in self.le_platform.text().split() if s]
        self.config["python_version"] = self.le_python_version.text()
        self.config["implementation"] = self.cmb_implementation.currentText()
        self.config["abis"] = [s for s in self.le_abis.text().split() if s]
        self.config["use_index_url"] = self.cb_use_index_url.isChecked()
        self.config["index_url"] = self.le_index_url.text()

    def apply_config(self):
        self.update_envpaths_and_combobox()
        self.pte_package_names.setPlainText(
            "\n".join(self.config.get("package_names", []))
        )
        self.cb_download_deps.setChecked(self.config.get("download_deps", True))
        download_type = self.config.get("download_type", "unlimited")
        if download_type == "unlimited":
            self.rb_unlimited.setChecked(True)
        elif download_type == "no_binary":
            self.rb_no_binary.setChecked(True)
        elif download_type == "only_binary":
            self.rb_only_binary.setChecked(True)
        elif download_type == "prefer_binary":
            self.rb_prefer_binary.setChecked(True)
        else:
            self.rb_unlimited.setChecked(True)
        self.cb_include_pre.setChecked(self.config.get("include_pre", False))
        self.cb_ignore_requires_python.setChecked(
            self.config.get("ignore_requires_python", False)
        )
        self.le_save_to.setText(self.config.get("save_to", ""))
        self.le_platform.setText(" ".join(self.config.get("platform", [])))
        self.le_python_version.setText(self.config.get("python_version", ""))
        self.cmb_implementation.setCurrentText(self.config.get("implementation", ""))
        self.le_abis.setText("".join(self.config.get("abis", [])))
        use_index_url = self.config.get("use_index_url", False)
        self.cb_use_index_url.setChecked(use_index_url)
        self.le_index_url.setText(self.config.get("index_url", ""))
        self.le_index_url.setEnabled(use_index_url)

    @staticmethod
    def confirm_dest(dest):
        # ????????????????????????
        if not dest:
            return True
        if not os.path.exists(dest):
            # ??????'???'?????????????????????1???????????????not??????
            create_folder = not NewMessageBox(
                "??????",
                "?????????????????????????????????????????????",
                QMessageBox.Warning,
                (("accept", "???"), ("reject", "???")),
            ).exec_()
            if create_folder:
                try:
                    os.makedirs(dest)
                    return True
                except Exception as e:
                    NewMessageBox(
                        "??????",
                        f"???????????????????????????\n{e}???",
                    ).exec_()
                    return False
            else:
                return False
        elif os.path.isfile(dest):
            NewMessageBox(
                "??????",
                "????????????????????????????????????????????????????????????",
            ).exec_()
            return False
        return True

    def start_download_package(self):
        if not self.environments:
            return NewMessageBox(
                "??????",
                "????????????Python???????????????'????????????'????????????????????????Python???????????????",
            ).exec_()
        self.store_config()
        destination = self.config.get("save_to", "")
        pkg_names = self.config.get("package_names", [])
        if not self.confirm_dest(destination):
            return
        if not pkg_names:
            return NewMessageBox(
                "??????",
                "?????????????????????????????????",
            ).exec_()
        index = self.config.get("derived_from", 0)
        if index < 0 or index >= len(self.environments):
            index = 0
            self.cmb_derived_from.setCurrentIndex(0)
        env = self.environments[index]
        if not env.env_path:
            return NewMessageBox(
                "??????",
                "?????????Python??????????????????????????????????????????",
            ).exec_()
        config = self.make_configure(pkg_names)
        if not isinstance(config, dict):
            return

        def do_download():
            saved_path = ""
            self.set_download_table.emit(pkg_names)
            for index, name in enumerate(pkg_names):
                self.download_status.emit(index, "?????????...")
                try:
                    status = env.download(name, **config)
                    if status[0]:
                        self.download_status.emit(index, "????????????")
                    else:
                        self.download_status.emit(index, "????????????")
                except Exception:
                    status = False, ""
                    self.download_status.emit(index, "????????????")
                if status[1]:
                    saved_path = status[1]
            self.download_completed.emit(saved_path)

        thread_download = NewTask(target=do_download)
        thread_download.at_start(lambda: self.pb_start_download.setEnabled(False))
        thread_download.at_finish(
            lambda: self.pb_start_download.setEnabled(True),
        )
        thread_download.start()
        self.repo.put(thread_download, 0)

    def check_download(self, dest):
        if not dest:
            return NewMessageBox(
                "??????",
                f"???????????????????????????!",
                QMessageBox.Critical,
            ).exec_()
        return NewMessageBox(
            "????????????",
            f"????????????????????????\n{dest}",
        ).exec_()

    def make_configure(self, names):
        configure = dict()

        def unqualified():
            return (
                not configure.get("no_deps", False)
                or configure.get("no_binary", False)
                or configure.get("only_binary", False)
            )

        if not self.config.get("download_deps", True):
            configure.update(no_deps=True)
        download_type = self.config.get("download_type", "unlimited")
        if download_type == "no_binary":
            configure.update(no_binary=parse_package_names(names))
        elif download_type == "only_binary":
            configure.update(only_binary=parse_package_names(names))
        elif download_type == "prefer_binary":
            configure.update(prefer_binary=True)
        if self.config.get("include_pre", False):
            configure.update(pre=True)
        if self.config.get("ignore_requires_python", False):
            configure.update(ignore_requires_python=True)
        saved_path = self.config.get("save_to", "")
        if saved_path:
            configure.update(dest=saved_path)
        platform_name = self.config.get("platform", [])
        if platform_name:
            if unqualified():
                return NewMessageBox(
                    "??????",
                    "??????'????????????'??????????????????'????????????????????????????????????'???\
????????????'?????????????????????'???'?????????????????????'???",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(platform=platform_name)
        python_version = self.config.get("python_version", "")
        if python_version:
            if unqualified():
                return NewMessageBox(
                    "??????",
                    "??????'??????Python??????'??????????????????'????????????????????????????????????'???\
????????????'?????????????????????'???'?????????????????????'???",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(python_version=python_version)
        impl_name = self.config.get("implementation", "")
        if impl_name == "???????????????":
            impl_name = "py"
        if impl_name:
            if unqualified():
                return NewMessageBox(
                    "??????",
                    "??????'?????????????????????'??????????????????'????????????????????????????????????'???\
????????????'?????????????????????'???'?????????????????????'???",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(implementation=impl_name)
        abis = self.config.get("abis", [])
        if abis:
            if unqualified():
                return NewMessageBox(
                    "??????",
                    "??????'??????ABI'??????????????????'????????????????????????????????????'???\
????????????'?????????????????????'???'?????????????????????'???",
                    QMessageBox.Warning,
                ).exec_()
            if not (platform_name and python_version and impl_name):
                return NewMessageBox(
                    "??????",
                    "?????????ABI???????????????????????????'????????????'???'??????Python??????'???\
'?????????????????????'?????????????????????",
                ).exec_()
            configure.update(abis=abis)
        index_url = self.config.get("index_url", "")
        if self.config.get("use_index_url") and index_url:
            configure.update(index_url=index_url)
        return configure


class ShowDownloadingWindow(Ui_downloading, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_other_widgets()

    def status_changed(self, index, status):
        if index >= self.tw_downloading.rowCount():
            return False
        color_red = QColor(255, 0, 0)
        color_green = QColor(0, 170, 0)
        item = self.tw_downloading.item(index, 1)
        if item is None:
            item = QTableWidgetItem("????????????")
            self.tw_downloading.setItem(index, 1, item)
        item.setText(status)
        if status == "????????????":
            item.setForeground(color_red)
        elif status == "????????????":
            item.setForeground(color_green)
        return True

    def clear_table(self):
        self.tw_downloading.clearContents()
        self.tw_downloading.setRowCount(0)

    def setup_table(self, iterable):
        color_gray = QColor(243, 243, 243)
        self.clear_table()
        self.tw_downloading.setRowCount(len(iterable))
        for index, pkg_name in enumerate(iterable):
            item1 = QTableWidgetItem(pkg_name)
            item2 = QTableWidgetItem("????????????")
            if not index % 2:
                item1.setBackground(color_gray)
                item2.setBackground(color_gray)
            self.tw_downloading.setItem(index, 0, item1)
            self.tw_downloading.setItem(index, 1, item2)
        return True

    def _setup_other_widgets(self):
        horiz_head = self.tw_downloading.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.Stretch)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)


class NewMessageBox(QMessageBox):
    """
    ???????????????????????????????????????????????????????????????0(??????)
    ???'reject'????????????'destructive'??????????????????????????????'reject'??????1
    ???'reject'????????????'destructive'??????????????????????????????'destructive'??????1
    ???'accept'?????????'reject'???????????????'accept'??????0???'reject'?????????????????????1
    ???'reject'???'destructive'?????????'reject'?????????????????????0???'destructive'??????1
    ???3????????????'accept'??????0???'reject'?????????????????????1???'destructive'??????2
    """

    def __init__(
        self,
        title,
        message,
        icon=QMessageBox.Information,
        buttons=(("accept", "??????"),),
    ):
        super().__init__(icon, title, message)
        self._buttons = buttons
        self._set_push_buttons()

    def _set_push_buttons(self):
        for btn in self._buttons:
            role, text = btn
            if role == "accept":
                self.addButton(text, QMessageBox.AcceptRole)
            elif role == "destructive":
                self.addButton(text, QMessageBox.DestructiveRole)
            elif role == "reject":
                self.setDefaultButton(self.addButton(text, QMessageBox.RejectRole))

    def get_role(self):
        return self.exec_()


class NewInputDialog(QInputDialog):
    def __init__(self, parent, sw=560, sh=0, title="", label=""):
        super().__init__(parent)
        self.resize(sw, sh)
        self.setFont(QFont("Microsoft YaHei UI"))
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setOkButtonText("??????")
        self.setCancelButtonText("??????")
        self._confirm = self.exec_()

    def get_text(self):
        return self.textValue(), self._confirm


def _check_venv(_path):
    """???????????????venv???????????????Python???????????????????????????"""
    p = os.path.dirname(_path)
    if os.path.isfile(os.path.join(p, "pyvenv.cfg")):
        return p
    return _path


def main():
    global win_ins_pkg
    global win_package_mgr
    global win_chenviron
    global win_pyi_tool
    global win_index_mgr
    global win_check_imp
    global win_dload_pkg
    global win_downloading
    app_awesomepykit = QApplication(sys.argv)
    app_awesomepykit.setWindowIcon(QIcon(os.path.join(resources_path, "icon.ico")))
    win_ins_pkg = InstallPackagesWindow()
    win_package_mgr = PackageManagerWindow()
    win_chenviron = ChooseEnvWindow()
    win_check_imp = CheckImportsWindow()
    win_pyi_tool = PyinstallerToolWindow()
    win_index_mgr = IndexUrlManagerWindow()
    win_downloading = ShowDownloadingWindow()
    win_dload_pkg = DownloadPackageWindow()
    win_main_interface = MainInterface()
    win_main_interface.show()
    sys.exit(app_awesomepykit.exec_())


if __name__ == "__main__":
    main()
