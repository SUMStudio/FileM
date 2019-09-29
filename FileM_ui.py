# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileM.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from RebuildMethod import QListWidgetRebuild


class Ui_FileM(object):
    def setupUi(self, FileM):
        FileM.setObjectName("FileM")
        FileM.resize(715, 594)
        self.centralwidget = QtWidgets.QWidget(FileM)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.lb_sidebar = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lb_sidebar.sizePolicy().hasHeightForWidth())
        self.lb_sidebar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lb_sidebar.setFont(font)
        self.lb_sidebar.setFrameShadow(QtWidgets.QFrame.Plain)
        self.lb_sidebar.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignHCenter)
        self.lb_sidebar.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.lb_sidebar.setObjectName("lb_sidebar")
        self.gridLayout.addWidget(self.lb_sidebar, 1, 1, 1, 1)
        self.QLabl = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.QLabl.sizePolicy().hasHeightForWidth())
        self.QLabl.setSizePolicy(sizePolicy)
        self.QLabl.setObjectName("QLabl")
        self.gridLayout.addWidget(self.QLabl, 3, 0, 1, 1)
        self.le_path = QtWidgets.QLineEdit(self.centralwidget)
        self.le_path.setObjectName("le_path")
        self.gridLayout.addWidget(self.le_path, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(12)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(150, 150))
        self.splitter.setMaximumSize(QtCore.QSize(8510, 4000))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.lw_catalogue = QtWidgets.QTreeWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_catalogue.sizePolicy().hasHeightForWidth())
        self.lw_catalogue.setSizePolicy(sizePolicy)
        self.lw_catalogue.setMinimumSize(QtCore.QSize(100, 100))
        self.lw_catalogue.setMaximumSize(QtCore.QSize(4000, 16777215))
        self.lw_catalogue.setAcceptDrops(True)
        self.lw_catalogue.setDragEnabled(False)
        self.lw_catalogue.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.lw_catalogue.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.lw_catalogue.setObjectName("lw_catalogue")
        self.lw_catalogue.headerItem().setText(0, "1")
        self.lw_main = QtWidgets.QListView(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_main.sizePolicy().hasHeightForWidth())
        self.lw_main.setSizePolicy(sizePolicy)
        self.lw_main.setMinimumSize(QtCore.QSize(100, 100))
        self.lw_main.setMaximumSize(QtCore.QSize(4000, 16777215))
        self.lw_main.setAcceptDrops(True)
        self.lw_main.setDragEnabled(True)
        self.lw_main.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.lw_main.setResizeMode(QtWidgets.QListView.Adjust)
        self.lw_main.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.lw_main.setObjectName("lw_main")
        # self.lw_sidebar = QtWidgets.QListWidget(self.splitter)
        self.lw_sidebar = QListWidgetRebuild(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(2)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lw_sidebar.sizePolicy().hasHeightForWidth())
        self.lw_sidebar.setSizePolicy(sizePolicy)
        self.lw_sidebar.setMinimumSize(QtCore.QSize(50, 50))
        self.lw_sidebar.setMaximumSize(QtCore.QSize(500, 4000))
        self.lw_sidebar.setAcceptDrops(True)
        self.lw_sidebar.setDragEnabled(False)
        self.lw_sidebar.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.lw_sidebar.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.lw_sidebar.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lw_sidebar.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.lw_sidebar.setObjectName("lw_sidebar")
        self.gridLayout.addWidget(self.splitter, 2, 0, 1, 2)
        FileM.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FileM)
        self.statusbar.setObjectName("statusbar")
        FileM.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(FileM)
        self.toolBar.setObjectName("toolBar")
        FileM.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(FileM)
        QtCore.QMetaObject.connectSlotsByName(FileM)

    def retranslateUi(self, FileM):
        _translate = QtCore.QCoreApplication.translate
        FileM.setWindowTitle(_translate("FileM", "FileM"))
        self.lb_sidebar.setText(_translate("FileM", "收藏夹"))
        self.QLabl.setText(_translate("FileM", "TextLabelTest"))
        self.le_path.setText(_translate("FileM", "/tmp"))
        self.toolBar.setWindowTitle(_translate("FileM", "toolBar"))
