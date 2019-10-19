# -*- coding:utf-8 -*-
"""
主程序
os.path.dirname() 去掉文件名返回路径
os.path.basename() 返回去除路径后的文件名
"""

from gui.dialog.AddFileDialog import AddFileDialog
from gui.mainwindow.FileMController import FileMController
from model.FileModel import FileModel
from util.CatalogueManager import CatalogueManager
from util.FileLabelManager import FileLabelManager
from util.FileManager import FileManager
from util.GlobalVarManager import GlobalVarManager

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction

from util.GlobalExceptionHandEr import *
from gui.mainwindow.FileM_ui import *


class FileM(QMainWindow, Ui_FileM):
    # 程序初始化
    def __init__(self, parent=None):
        super(FileM, self).__init__(parent)
        self.setupUi(self)
        # 初始化控制器
        self._controller = FileMController(self)

        self.setWindowIcon(QIcon('resources/fileM.png'))  # 设置图标

        self.exception_handler = GlobalExceptionHandEr()  # 异常处理
        self.exception_handler.patch_except_hook()

        # 初始化文件列表
        self.init_lv_file()
        # 初始化标签栏
        self.init_lv_label()
        # 初始化目录框
        self.init_tv_catalogue()
        # 初始化地址栏
        self.le_path.setText('root')  # 显示路径
        #   self.le_path.returnPressed.connect(self._controller.on_pb_load_path_clicked)  # 在地址栏按下Enter键发出信号(响应回车键)

        # 初始化工具栏
        # self.init_toolbar()

        self.isWindowsOS = sys.platform == "win32"
        # self.lw_sidebar.itemDoubleClicked.connect(self.on_lw_sidebar_db_clicked)       #预留

        # 调用Drops方法，允许拖入
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)    # 可在QT designer内实现

    def init_tv_catalogue(self):
        self.tv_catalogue.setModel(CatalogueManager().cat_list_model)
        self.tv_catalogue.selectionModel().selectionChanged.connect(self._controller.on_selected_changed)
        self.tv_catalogue.customContextMenuRequested[QPoint].connect(self._controller.on_menu_requested)

    def init_lv_file(self):
        self.lv_file.setModel(FileManager().file_list_model)
        self.lv_file.selectionModel().selectionChanged.connect(self._controller.on_selected_changed)
        self.lv_file.customContextMenuRequested[QPoint].connect(self._controller.on_menu_requested)

    def init_lv_label(self):
        self.lv_label.setModel(FileLabelManager().label_list_model)
        self.lv_label.selectionModel().selectionChanged.connect(self._controller.on_selected_changed)
        self.lv_label.customContextMenuRequested[QPoint].connect(self._controller.on_menu_requested)

    def init_toolbar(self):
        self.toolBar.addAction(QIcon("resources/list-add.png"), "新增")
        self.toolBar.addAction(QIcon("resources/list-remove.png"), "删除")
        self.toolBar.addAction(QIcon("resources/go-home.png"), "主页")
        self.toolBar.addAction(QIcon("resources/folder.png"), "显示文件夹").setCheckable(True)
        self.toolBar.addAction(QIcon("resources/eye.png"), "显示隐藏文件").setCheckable(True)
        self.toolBar.addAction(QIcon("resources/go-up.png"), "返回上层")
        self.toolBar.actionTriggered[QAction].connect(self._controller.on_toolbar_clicked)  # 发送信号执行操作

    def dragEnterEvent(self, evn):
        # 鼠标拖入窗口事件，待续
        # self.lb_info.setText('文件路径：\n' + evn.mimeData().text())
        # 鼠标放开函数事件
        evn.accept()

    def dropEvent(self, evn):
        # 鼠标在窗口内放开时执行
        self.statusbar.showMessage(str(evn.pos()))
        # 取拖入文件列表
        for url in evn.mimeData().urls():
            file_path = url.toLocalFile()
            # 初始化文件模型
            file_model = FileModel()
            file_model.abs_path = file_path
            # 标签信息
            self._controller.show_message("文件路径:"+url.toLocalFile())
            # 弹出文件标签编辑框
            AddFileDialog(file_model).exec_()

    def dragMoveEvent(self, evn):
        # 鼠标拖动过程中执行，待续
        pass


def main():
    app = QApplication(sys.argv)
    win = FileM()
    win.show()
    sys.exit(app.exec_())
