# -*- coding:utf-8 -*-
"""
主程序
os.path.dirname() 去掉文件名返回路径
os.path.basename() 返回去除路径后的文件名
"""

# import sys
from subprocess import call
# import os
from os.path import basename   # join, dirname, isdir, isfile, exists
# from os import makedirs
# noinspection PyBroadException
try:
    from os import startfile
except Exception as e:
    pass

# if hasattr(sys, 'frozen'):
#     os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.Qt import QCursor, QAbstractItemView
# from PyQt5.uic import loadUi
from PyQt5.QtCore import pyqtSlot, QDir, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QFileSystemModel, QMenu, QInputDialog, QTreeWidgetItem, QApplication
# from PyQt5.QtWidgets import QTreeWidgetItemIterator
from shutil import copy2

from fileutil import *
from fmconfig import *
from bookmark import *
from menu import *
from exception_handler import *
from scriptmanager import *
from FileM_ui import *
from root_list_test import *

user_home_path = QDir.home().absolutePath()
home_path = user_home_path + "/FileM"


class FileM(QMainWindow, Ui_FileM):
    # 程序初始化
    def __init__(self, parent=None):
        super(FileM, self).__init__(parent)
        # loadUi(get_file_realpath("FileM.ui"), self)  # 加载主ui文件
        self.setupUi(self)
        self.setWindowIcon(QIcon(get_file_realpath('data/fileM.png')))   # 设置图标
        
        self.exception_handler = GlobalExceptionHandEr()  # 异常处理
        self.exception_handler.patch_except_hook()

        # 初始化文件列表
        self.lw_main.setSelectionMode(QAbstractItemView.ExtendedSelection)  # 允许多选
        self.lw_main.clicked.connect(self.on_lw_main_clicked)   # 单击文件列表中的某个文件时
        self.lw_main.doubleClicked.connect(self.on_lw_main_db_clicked)   # 双击文件列表中的某个文件时
        self.lw_main.installEventFilter(self)   # 为 文件列表窗口对象 添加事件过滤器-->eventFilter()
        self.fileSystemModel = QFileSystemModel(self.lw_main)
        self.fileSystemModel.setReadOnly(False)
        self.fileFilter = self.fileSystemModel.filter()
        self.fileFilter_hidden = None
        is_exists = exists(home_path)
        if not is_exists:
            makedirs(home_path)      # 若路径不存在则新建文件夹
        self.le_path.setText(home_path)         # 显示路径
        root = self.fileSystemModel.setRootPath(home_path)  # 设置设定C:\\Users\Username\FileM为主目录并
        self.lw_main.setModel(self.fileSystemModel)
        self.lw_main.setRootIndex(root)
        self.lw_main.setWrapping(True)      # 布局设置,不允许文件列表多列显示
        self.le_path.returnPressed.connect(self.on_pb_load_path_clicked)    # 在地址栏按下Enter键发出信号(响应回车键)

        # 初始化工具栏
        self.init_toolbar()
        self.bookmark_list = get_bookmark()

        # 初始化收藏夹(标签栏)
        self.init_bookmark()
        
        self.isWindowsOS = sys.platform == "win32"
        # self.lw_sidebar.itemDoubleClicked.connect(self.on_lw_sidebar_db_clicked)       #预留

        # 初始化右键菜单
        # self.main_menu = QMenu()
        self.file_menu = QMenu()
        # self.folder_menu = QMenu()
        # self.file_popup_menu = FileMenu()
        # self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.showContextMenu)
        self.action_open = self.file_menu.addAction("打开")
        self.action_copy = self.file_menu.addAction("复制")
        self.action_copy_path = self.file_menu.addAction("复制路径")
        self.action_paste = self.file_menu.addAction("粘贴")
        self.action_rename = self.file_menu.addAction("重命名")
        self.file_menu_delete = self.file_menu.addMenu("删除")
        self.action_del_file = self.file_menu_delete.addAction("文件")
        self.action_del_label = self.file_menu_delete.addMenu("标签")

        self.script_manager = ScriptManager()

        # 初始化目录树
        self.lw_catalogue.setColumnCount(1)
        self.lw_catalogue.setHeaderLabels(['目录'])
        root = QTreeWidgetItem(self.lw_catalogue)
        root.setText(0, "root")
        self.lw_catalogue.addTopLevelItem(root)
        self.lw_catalogue.setColumnWidth(0, 80)
        self.init_catalogue(root_list)

        self.lw_catalogue.clicked.connect(self.on_lw_catalogue_clicked)  # 单击目录中的某个文件时
        self.lw_catalogue.doubleClicked.connect(self.on_lw_catalogue_db_clicked)  # 双击目录中的某个文件时
        self.lw_catalogue.installEventFilter(self)  # 为 目录窗口对象 添加事件过滤器-->eventFilter()

        # 调用Drops方法，允许拖入
        self.setAcceptDrops(True)
        # self.setDragEnabled(True)    # 可在QT designer内实现

    def dragEnterEvent(self, evn):
        # 鼠标拖入窗口事件，待续
        self.QLabl.setText('文件路径：\n' + evn.mimeData().text())
        # 鼠标放开函数事件
        evn.accept()

    def dropEvent(self, evn):
        # 鼠标在窗口内放开时执行，待续
        self.statusbar.showMessage(str(evn.pos()))
        item_sidebar = self.lw_sidebar.currentItem()
        item_row = self.lw_sidebar.currentRow()
        i_dict = init_dict("global", "labels")
        if item_row >= 0:
            """
            # if item_sidebar.text() != "zzzzzzzz":
                # 将文件与标签关联，生成字典
                # path = basename(evn.mimeData().text())
            """
            real_path = evn.mimeData().text().split('\n', -1)
            for i in real_path:
                if i:
                    path = basename(i)
                    if not i_dict.get(item_sidebar.text()):
                        i_dict[item_sidebar.text()] = []
                    if path not in i_dict[item_sidebar.text()]:
                        i_dict[item_sidebar.text()].append(path)
                    dict_add("global", "labels", i_dict)
        else:
            # 复制文件到主目录
            # path_len = len(evn.mimeData().text())
            # src_path = evn.mimeData().text()[8:path_len]
            src_path = evn.mimeData().text().split('\n', -1)
            for i in src_path:
                dst = home_path + '/' + basename(i)
                if i:
                    path_len = len(i)
                    if not exists(dst):
                        copy2(i[8:path_len], home_path)

    def dragMoveEvent(self, evn):
        # 鼠标拖动过程中执行，待续
        pass

    def init_bookmark(self):
        self.lw_sidebar.clear()
        if self.bookmark_list:
            for b in self.bookmark_list:
                self.lw_sidebar.addItem(b)
        # self.lw_sidebar.currentItemChanged.connect(self.on_lw_sidebar_clicked)

    def init_toolbar(self):
        self.toolBar.addAction(QIcon(get_file_realpath("data/list-add.png")), "新增")
        self.toolBar.addAction(QIcon(get_file_realpath("data/list-remove.png")), "删除")
        self.toolBar.addAction(QIcon(get_file_realpath("data/go-home.png")), "主页")
        self.toolBar.addAction(QIcon(get_file_realpath("data/folder.png")), "显示文件夹").setCheckable(True)
        self.toolBar.addAction(QIcon(get_file_realpath("data/eye.png")), "显示隐藏文件").setCheckable(True)
        self.toolBar.addAction(QIcon(get_file_realpath("data/go-up.png")), "返回上层")
        self.toolBar.actionTriggered[QAction].connect(self.on_toolbar_clicked)  # 发送信号执行操作

    # 生成目录树
    def init_catalogue(self, root_list_t):
        root = self.lw_catalogue.topLevelItem(0)
        # child = root
        row_length = len(root_list_t)
        for row in range(row_length):
            col_length = len(root_list_t[row])
            child = root
            for col in range(1, col_length):
                child_count = child.childCount()
                flags = True
                for i in range(child_count):
                    # child = child.child(i)
                    if child.child(i).text(0) == root_list_t[row][col]:
                        flags = False
                        break
                if flags:
                    item = QTreeWidgetItem(child)
                    item.setText(0, root_list_t[row][col])
                    file_split = root_list_t[row][col].split('.', -1)
                    file_type = file_split[-1]
                    if file_type == 'txt':
                        item.setIcon(0, QIcon(get_file_realpath("data/txt.png")))
                    elif file_type == 'mp3':
                        item.setIcon(0, QIcon(get_file_realpath("data/mp3.png")))
                    elif file_type == 'iso':
                        item.setIcon(0, QIcon(get_file_realpath("data/iso.png")))
                    elif file_type == 'dll':
                        item.setIcon(0, QIcon(get_file_realpath("data/dll.png")))
                    elif file_type == 'jpg' or file_type == 'jpeg' or file_type == 'png':
                        item.setIcon(0, QIcon(get_file_realpath("data/jpg.png")))
                    elif file_type == 'doc' or file_type == 'docx':
                        item.setIcon(0, QIcon(get_file_realpath("data/word.png")))
                    elif file_type == 'ppt' or file_type == 'pptx':
                        item.setIcon(0, QIcon(get_file_realpath("data/ppt.png")))
                    elif file_type == 'xls' or file_type == 'xlsx':
                        item.setIcon(0, QIcon(get_file_realpath("data/excel.png")))
                    else:
                        if len(file_split) > 1:
                            item.setIcon(0, QIcon(get_file_realpath("data/else.png")))
                        pass
                    child = item
                else:
                    child = child.child(i)
        # pass

    # 工具栏点击动作，未完成
    def on_toolbar_clicked(self, action):
        action_text = action.text()
        if action_text == "主页":
            self.go_home()
        elif action_text == "返回上层":
            parent_dir = dirname(self.le_path.text())
            self.le_path.setText(parent_dir)
            self.on_pb_load_path_clicked()
        elif action_text == "显示隐藏文件":
            if action.isChecked():
                self.fileFilter_hidden = QDir.Hidden
                self.fileSystemModel.setFilter(self.fileFilter | QDir.Hidden)
            else:
                self.fileFilter_hidden = None
                self.fileSystemModel.setFilter(self.fileFilter)
        elif action_text == "显示文件夹":
            if action.isChecked():
                if self.fileFilter_hidden:
                    self.fileSystemModel.setFilter(QDir.Dirs | QDir.Hidden | QDir.NoDot | QDir.NoDotDot)
                else:
                    self.fileSystemModel.setFilter(QDir.Dirs | QDir.NoDot | QDir.NoDotDot)
            else:
                self.fileSystemModel.setFilter(self.fileFilter)
        elif action_text == "新增":
            if self.lb_sidebar.text() == "收藏夹":
                new_label, ok = QInputDialog.getText(self, "新增标签", "请输入一个新标签：")
                self.bookmark_list = get_bookmark()
                i_dict = init_dict("global", "labels")
                if new_label not in self.bookmark_list:
                    self.lw_sidebar.addItem(new_label)
                    list_add("global", "bookmark", new_label)
                if not i_dict.get(new_label):
                    i_dict[new_label] = []
                dict_add("global", "labels", i_dict)
        elif action_text == "删除":
            if self.lb_sidebar.text() == "收藏夹":
                # print(self.lw_sidebar.currentRow())
                print(self.lw_sidebar.currentItem())
                item = self.lw_sidebar.currentItem()
                del_item = item.text()
                # if del_item != "zzzzzzzz":
                list_del("global", "bookmark", del_item)
                dict_del("global", "labels", del_item)
                self.bookmark_list.discard(del_item)
                self.lw_sidebar.takeItem(self.lw_sidebar.currentRow())  # 删除item
                print(self.bookmark_list)

    # 定义槽
    # @pyqtSlot()
    # def on_lw_sidebar_clicked(self):
    #     # 单击侧边栏动作

    # @pyqtSlot()
    # def on_lw_sidebar_db_clicked(self):
    #     # 双击侧边栏动作

    @pyqtSlot()
    def on_pb_load_path_clicked(self):
        # 更新文件列表
        root = self.fileSystemModel.setRootPath(self.le_path.text())
        self.lw_main.setRootIndex(root)
    
    @pyqtSlot()
    def on_lw_main_clicked(self):
        # 单击文件
        # if self.lw_main.selectionMode() == Qt.ControlModifier:
        #     return

        cur_item_index = self.lw_main.currentIndex()
        cur_item1 = self.fileSystemModel.itemData(cur_item_index)
        cur_item = cur_item1[0]     # 当前选中文件的文件名
        print("cur_item", cur_item1)
        sub_path = join(self.le_path.text(), cur_item)  # 被选中文件的文件名与当前所在文件夹合成绝对路径
        print("sub_path:" + sub_path)

        # 测试用
        if isdir(str(sub_path)):
            print(sub_path + "is a dir")
        elif isfile(str(sub_path)):
            print(sub_path + " is a file")
        else:
            print(type(sub_path))

    @pyqtSlot()
    def on_lw_main_db_clicked(self):
        # 双击文件
        cur_item_index = self.lw_main.currentIndex()
        cur_item1 = self.fileSystemModel.itemData(cur_item_index)
        cur_item = cur_item1[0]     # 文件名
        sub_path = join(self.le_path.text(), cur_item)  # 取得绝对路径

        if isfile(str(sub_path)):
            # 若双击的是文件，则打开该文件
            if self.isWindowsOS:
                startfile(sub_path)
            else:
                call(["xdg-open", sub_path])
            # self.showMinimized()      #最小化窗口
        elif isdir(str(sub_path)):
            # 若选中的是文件夹，则更新地址栏并进入该文件夹
            print(sub_path + "is a dir")
            self.le_path.setText(sub_path)
            self.on_pb_load_path_clicked()

    @pyqtSlot()
    def on_lw_catalogue_clicked(self):
        # 若在目录中单击文件(叶节点)，则在文件列表中定位到该标签
        # 若在目录中单击标签，则在文件列表中定位拥有该标签的所有文件
        item_catalogue = self.lw_catalogue.currentItem()
        print("item_catalogue", item_catalogue.text(0))
        item_path = home_path + '/' + item_catalogue.text(0)
        print("item_path", item_path)
        is_exists = exists(item_path)
        if is_exists:
            # 若是文件
            item_main_index = self.lw_main.currentIndex()
            item_main = self.fileSystemModel.itemData(item_main_index)
            print("item_main", item_main)
            pass
        else:
            # 若是标签
            pass
        pass

    @pyqtSlot()
    def on_lw_catalogue_db_clicked(self):
        # 若在目录中双击文件，则打开文件
        # 若在目录中双击标签，不操作
        pass

    def go_home(self):
        # 返回主目录
        # self.le_path.setText(QDir.home().absolutePath())
        self.le_path.setText(home_path)
        self.on_pb_load_path_clicked()

    def eventFilter(self, q_object, q_event):
        # 事件过滤器，响应右键菜单
        q_type = q_event.type()

        if q_type == 82:  # 82为上下文弹出菜单QContextMenuEvent，即右键菜单
            counter = len(self.lw_main.selectedIndexes())  # 返回选中文件个数

            # 处理选中的文件,待改进
            if counter >= 1:
                # action = self.file_menu.exec_(self.file_popup_menu.menu_item, QCursor.pos())  # 单击菜单action时
                # 获取选中已选中文件的文件列表,仅包含文件名，并非是绝对路径
                file_list = [self.fileSystemModel.itemData(i)[0] for i in self.lw_main.selectedIndexes()]
                actions = self.get_label_actions(file_list)
                self.action_del_label.addActions(actions)
                # for i in actions:
                #     self.action_del_label.addAction(i)
                action = self.file_menu.exec_(QCursor.pos())  # 单击菜单action时
                if action:
                    script_name = action.text()
                    file_path = self.le_path.text()
                    label_parent = action.parentWidget()
                    if action.parentWidget() == self.file_menu_delete:
                        script_name = "删除文件"
                    if not label_parent:
                        script_name = "删除标签"
                        file_path = action.text()
                    self.script_manager.run_script(script_name, file_path, file_list)  # 执行相应脚本功能
                    # run_script(self, script_name, filePath, file_list)
                else:
                    pass
        return False

    def get_label_actions(self, file_list):
        i_dict = init_dict("global", "labels")
        action_list = []
        # for file in file_list:
        for label in i_dict:
            if file_list[0] in i_dict[label]:
                action = QAction(label)
                action_list.append(action)
        return action_list

    def show_statusbar_msg(self, msg):
        self.statusbar.showMessage(msg)
    
#     拦截(设置)快捷键
    def keyPressEvent(self, event):
        key = event.key()
        print("按下：" + str(event.key()))
        if event.modifiers() == Qt.ControlModifier and key == Qt.Key_C:
            file_list = [self.fileSystemModel.itemData(i)[0] for i in self.lw_main.selectedIndexes()]
            self.script_manager.run_script("复制", self.le_path.text(), file_list)
        elif event.modifiers() == Qt.ControlModifier and key == Qt.Key_V:
            self.script_manager.run_script("粘贴", self.le_path.text(), None)
        elif key == Qt.Key_F2:
            file_list = [self.fileSystemModel.itemData(self.lw_main.currentIndex())[0]]
            self.script_manager.run_script("重命名", self.le_path.text(), file_list)

        """
        elif event.modifiers() == Qt.ControlModifier and key == None:
            self.lw_main.setSelectionMode(QAbstractItemView.ExtendedSelection)
            print("duoxuan")
        elif event.modifiers() == Qt.ShiftModifier and key == None :
            self.lw_main.setSelectionMode(QAbstractItemView.ContiguousSelection)
            print("shit 多选")
        """


def main():
    app = QApplication(sys.argv)
    win = FileM()
    win.show()
    sys.exit(app.exec_())
