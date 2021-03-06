# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'index_url_manager.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_index_url_manager(object):
    def setupUi(self, index_url_manager):
        index_url_manager.setObjectName("index_url_manager")
        index_url_manager.setWindowModality(QtCore.Qt.ApplicationModal)
        index_url_manager.resize(660, 600)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        index_url_manager.setFont(font)
        self.centralwidget = QtWidgets.QWidget(index_url_manager)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.li_indexurls = QtWidgets.QListWidget(self.centralwidget)
        self.li_indexurls.setObjectName("li_indexurls")
        self.verticalLayout_4.addWidget(self.li_indexurls)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.btn_delurl = QtWidgets.QPushButton(self.centralwidget)
        self.btn_delurl.setObjectName("btn_delurl")
        self.horizontalLayout_4.addWidget(self.btn_delurl)
        self.horizontalLayout_4.setStretch(0, 9)
        self.horizontalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.le_urlname = QtWidgets.QLineEdit(self.centralwidget)
        self.le_urlname.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_urlname.setObjectName("le_urlname")
        self.verticalLayout.addWidget(self.le_urlname)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.le_indexurl = QtWidgets.QLineEdit(self.centralwidget)
        self.le_indexurl.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_indexurl.setObjectName("le_indexurl")
        self.verticalLayout_2.addWidget(self.le_indexurl)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 9)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.btn_clearle = QtWidgets.QPushButton(self.centralwidget)
        self.btn_clearle.setObjectName("btn_clearle")
        self.horizontalLayout.addWidget(self.btn_clearle)
        self.btn_saveurl = QtWidgets.QPushButton(self.centralwidget)
        self.btn_saveurl.setObjectName("btn_saveurl")
        self.horizontalLayout.addWidget(self.btn_saveurl)
        self.btn_setindex = QtWidgets.QPushButton(self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.btn_setindex.setPalette(palette)
        self.btn_setindex.setObjectName("btn_setindex")
        self.horizontalLayout.addWidget(self.btn_setindex)
        self.horizontalLayout.setStretch(0, 9)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 2)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.verticalLayout_4.addWidget(self.line_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.btn_refresh_effective = QtWidgets.QPushButton(self.centralwidget)
        self.btn_refresh_effective.setObjectName("btn_refresh_effective")
        self.horizontalLayout_3.addWidget(self.btn_refresh_effective)
        self.horizontalLayout_3.setStretch(0, 9)
        self.horizontalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.le_effectiveurl = QtWidgets.QLineEdit(self.centralwidget)
        self.le_effectiveurl.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.le_effectiveurl.setReadOnly(True)
        self.le_effectiveurl.setObjectName("le_effectiveurl")
        self.verticalLayout_3.addWidget(self.le_effectiveurl)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.setStretch(0, 9)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 1)
        self.verticalLayout_4.setStretch(5, 1)
        self.verticalLayout_4.setStretch(6, 1)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        index_url_manager.setCentralWidget(self.centralwidget)

        self.retranslateUi(index_url_manager)
        QtCore.QMetaObject.connectSlotsByName(index_url_manager)

    def retranslateUi(self, index_url_manager):
        _translate = QtCore.QCoreApplication.translate
        index_url_manager.setWindowTitle(_translate("index_url_manager", "???????????????"))
        self.btn_delurl.setToolTip(_translate("index_url_manager", "??????????????????????????????????????????"))
        self.btn_delurl.setText(_translate("index_url_manager", "??????"))
        self.label.setText(_translate("index_url_manager", "???????????????"))
        self.label_2.setText(_translate("index_url_manager", "???????????????"))
        self.btn_clearle.setToolTip(_translate("index_url_manager", "????????????????????????????????????????????????"))
        self.btn_clearle.setText(_translate("index_url_manager", "????????????"))
        self.btn_saveurl.setToolTip(_translate("index_url_manager", "???????????????????????????????????????????????????"))
        self.btn_saveurl.setText(_translate("index_url_manager", "???????????????"))
        self.btn_setindex.setToolTip(_translate("index_url_manager", "????????????????????????????????????????????????????????????"))
        self.btn_setindex.setText(_translate("index_url_manager", "???????????????"))
        self.label_3.setText(_translate("index_url_manager", "???????????????????????????????????????"))
        self.btn_refresh_effective.setToolTip(_translate("index_url_manager", "??????????????????????????????????????????????????????"))
        self.btn_refresh_effective.setText(_translate("index_url_manager", "??????"))
