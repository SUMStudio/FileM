# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddFileDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddFileDialog(object):
    def setupUi(self, AddFileDialog):
        AddFileDialog.setObjectName("AddFileDialog")
        AddFileDialog.setWindowModality(QtCore.Qt.WindowModal)
        AddFileDialog.resize(291, 313)
        AddFileDialog.setModal(False)
        self.verticalLayoutWidget = QtWidgets.QWidget(AddFileDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 271, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_addselect = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_addselect.setObjectName("btn_addselect")
        self.horizontalLayout.addWidget(self.btn_addselect)
        self.btn_newlabel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_newlabel.setObjectName("btn_newlabel")
        self.horizontalLayout.addWidget(self.btn_newlabel)
        self.btn_removelabel = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_removelabel.setObjectName("btn_removelabel")
        self.horizontalLayout.addWidget(self.btn_removelabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.lv_label = QtWidgets.QListView(self.verticalLayoutWidget)
        self.lv_label.setEnabled(True)
        self.lv_label.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lv_label.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.lv_label.setObjectName("lv_label")
        self.verticalLayout.addWidget(self.lv_label)

        self.retranslateUi(AddFileDialog)
        QtCore.QMetaObject.connectSlotsByName(AddFileDialog)

    def retranslateUi(self, AddFileDialog):
        _translate = QtCore.QCoreApplication.translate
        AddFileDialog.setWindowTitle(_translate("AddFileDialog", "新增文件"))
        self.btn_addselect.setText(_translate("AddFileDialog", "添加选中"))
        self.btn_newlabel.setText(_translate("AddFileDialog", "新的标签"))
        self.btn_removelabel.setText(_translate("AddFileDialog", "移除标签"))

