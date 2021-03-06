# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'install_package.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_install_package(object):
    def setupUi(self, install_package):
        install_package.setObjectName("install_package")
        install_package.setWindowModality(QtCore.Qt.ApplicationModal)
        install_package.resize(480, 486)
        install_package.setMinimumSize(QtCore.QSize(480, 486))
        install_package.setMaximumSize(QtCore.QSize(480, 486))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(9)
        install_package.setFont(font)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(install_package)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QtWidgets.QLabel(install_package)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.le_target_env = QtWidgets.QLineEdit(install_package)
        self.le_target_env.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_target_env.setFrame(False)
        self.le_target_env.setReadOnly(True)
        self.le_target_env.setObjectName("le_target_env")
        self.horizontalLayout.addWidget(self.le_target_env)
        self.horizontalLayout.setStretch(1, 9)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.line_3 = QtWidgets.QFrame(install_package)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout_6.addWidget(self.line_3)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(install_package)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.splitter = QtWidgets.QSplitter(install_package)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pte_package_names_old = QtWidgets.QPlainTextEdit(self.splitter)
        self.pte_package_names_old.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.pte_package_names_old.setObjectName("pte_package_names_old")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cb_including_pre = QtWidgets.QCheckBox(self.layoutWidget)
        self.cb_including_pre.setObjectName("cb_including_pre")
        self.verticalLayout_2.addWidget(self.cb_including_pre)
        self.cb_install_for_user = QtWidgets.QCheckBox(self.layoutWidget)
        self.cb_install_for_user.setObjectName("cb_install_for_user")
        self.verticalLayout_2.addWidget(self.cb_install_for_user)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        self.line_2 = QtWidgets.QFrame(self.layoutWidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.pb_load_from_text = QtWidgets.QPushButton(self.layoutWidget)
        self.pb_load_from_text.setObjectName("pb_load_from_text")
        self.verticalLayout_3.addWidget(self.pb_load_from_text)
        self.pb_save_as_text = QtWidgets.QPushButton(self.layoutWidget)
        self.pb_save_as_text.setObjectName("pb_save_as_text")
        self.verticalLayout_3.addWidget(self.pb_save_as_text)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.pb_do_install = QtWidgets.QPushButton(self.layoutWidget)
        self.pb_do_install.setMinimumSize(QtCore.QSize(0, 50))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.pb_do_install.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.pb_do_install.setFont(font)
        self.pb_do_install.setObjectName("pb_do_install")
        self.verticalLayout_4.addWidget(self.pb_do_install)
        self.verticalLayout_5.addWidget(self.splitter)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.line_4 = QtWidgets.QFrame(install_package)
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.verticalLayout_6.addWidget(self.line_4)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.cb_use_index_url = QtWidgets.QCheckBox(install_package)
        self.cb_use_index_url.setObjectName("cb_use_index_url")
        self.verticalLayout.addWidget(self.cb_use_index_url)
        self.le_use_index_url = QtWidgets.QLineEdit(install_package)
        self.le_use_index_url.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_use_index_url.setObjectName("le_use_index_url")
        self.verticalLayout.addWidget(self.le_use_index_url)
        self.verticalLayout_6.addLayout(self.verticalLayout)
        self.line = QtWidgets.QFrame(install_package)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_6.addWidget(self.line)
        self.label_2 = QtWidgets.QLabel(install_package)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_6.addWidget(self.label_2)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)

        self.retranslateUi(install_package)
        QtCore.QMetaObject.connectSlotsByName(install_package)

    def retranslateUi(self, install_package):
        _translate = QtCore.QCoreApplication.translate
        install_package.setWindowTitle(_translate("install_package", "??????"))
        self.label_3.setToolTip(_translate("install_package", "??????????????????????????????????????????"))
        self.label_3.setText(_translate("install_package", "???????????????"))
        self.le_target_env.setToolTip(_translate("install_package", "??????????????????????????????????????????"))
        self.label.setText(_translate("install_package", "?????????"))
        self.cb_including_pre.setToolTip(_translate("install_package", "??????????????????????????????????????????????????????????????????????????????\n"
"????????????????????????????????????????????????????????????????????????????????????"))
        self.cb_including_pre.setText(_translate("install_package", "??????????????????????????????"))
        self.cb_install_for_user.setToolTip(_translate("install_package", "???????????????????????????????????????????????????????????????"))
        self.cb_install_for_user.setText(_translate("install_package", "????????????????????????"))
        self.pb_load_from_text.setToolTip(_translate("install_package", "????????????????????????????????????????????????\n"
"??????????????????requirements.txt???????????????"))
        self.pb_load_from_text.setText(_translate("install_package", "?????????????????????"))
        self.pb_save_as_text.setToolTip(_translate("install_package", "????????????????????????????????????????????????"))
        self.pb_save_as_text.setText(_translate("install_package", "?????????????????????"))
        self.pb_do_install.setText(_translate("install_package", "????????????"))
        self.cb_use_index_url.setText(_translate("install_package", "??????????????????????????????"))
        self.label_2.setText(_translate("install_package", "????????????????????????????????????????????????????????????\n"
"\"==\"???\">=\"???\"<=\"???\">\"???\"<\"???\",\"\n"
"??????????????????????????????????????????????????????????????????\n"
"?????????fastpip>=0.6.2,<0.10.0\n"
"?????????whl?????????????????????????????????????????????????????????whl???????????????????????????"))
