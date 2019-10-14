import os
from os.path import exists

from PyQt5.QtCore import QModelIndex, QItemSelection
from PyQt5.QtGui import QCursor

from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from gui.menu.CatalogueMenu import CatalogueMenu
from gui.menu.FileEditMenu import FileEditMenu
from gui.menu.LabelEditMenu import LabelEditMenu
from util.SingletonConfigEditor import SingletonConfigEditor
from util.SingletonFileLabelManager import SingletonFileLabelManager
from util.SingletonFileManager import SingletonFileManager


class FileMController:
    def __init__(self, window):
        self._window = window

    def on_menu_requested(self, point):
        sender = self._window.sender()
        menu = None
        if sender == self._window.tv_catalogue:
            menu = CatalogueMenu(self._window.tv_catalogue)
        else:
            # 取选中项
            index = sender.indexAt(point)
            if not index.data():
                sender.clearSelection()
                return
            elif sender == self._window.lv_file:
                menu = FileEditMenu(index)
            elif sender == self._window.lv_label:
                menu = LabelEditMenu(index)
        menu.exec(QCursor().pos())

    def on_lv_changed(self, selected:QItemSelection, deselected:QItemSelection):
        sender = self._window.sender()
        if sender == self._window.lv_file.selectionModel():
            file_name = selected.indexes()[0].data()
            label_list = SingletonFileManager.instance().get_label_list(file_name)
            self.show_message("{}:标签为{}".format(file_name,str(label_list)))
        if sender == self._window.lv_label.selectionModel():
            label_name = selected.indexes()[0].data()
            file_name_list = SingletonFileLabelManager.instance().get_file_name_list(label_name)
            self.show_message("{}:文件为{}".format(label_name, str(file_name_list)))

    def show_message(self, msg: str):
        self._window.lb_info.setText(msg)

    def on_btn_clicked(self):
        sender = self._window.sender()
        if sender == self._window.btn_updatetree:
            pass
        elif sender == self._window.btn_loadtree:
            # 从数据库中加载目录树
            self._window.root_list = list()
            for path in self._window.tree_model.get_root2leaf_path():
                print(path)
                for file_name in path[-1]:
                    temp_path = list()
                    for dir_name in path[:-1]:
                        temp_path.append(dir_name[0])
                    temp_path.append(file_name)
                    self._window.root_list.append(temp_path)
            self._window.init_catalogue()
            # print(self.root_list)
        elif sender == self._window.btn_updatelattice:
            # 仅更新概念格，耗时较大，建议用线程执行
            # 读取配置项
            i_dict = SingletonConfigEditor.instance().init_dict("global", "labels")
            # 处理数据Key-文件，Value-标签集合
            new_dict = dict()
            for label, file_names in i_dict.items():
                for file_name in file_names:
                    if not new_dict.get(file_name):
                        new_dict[file_name] = set()
                    new_dict[file_name].add(label)
            # 增量式构造格
            # 清空格
            self._window.lattice_model.delete_all()
            for file_name, label_set in new_dict.items():
                concept = ConceptNodeModel(extents={file_name}, intents=label_set)
                add_concept(self._window.lattice_model, concept)

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

    def on_tw_catalogue_clicked(self):
        # 若在目录中单击文件(叶节点)，则在文件列表中定位到该标签
        # 若在目录中单击标签，则在文件列表中定位拥有该标签的所有文件
        item_catalogue = self._window.tw_catalogue.currentItem()
        print("item_catalogue", item_catalogue.text(0))
        item_path = self._window.home_path + '/' + item_catalogue.text(0)
        print("item_path", item_path)
        is_exists = exists(item_path)
        if is_exists:
            # 若是文件
            item_main_index = self._window.lw_main.currentIndex()
            item_main = self._window.fileSystemModel.itemData(item_main_index)
            print("item_main", item_main)
            pass
        else:
            # 若是标签
            pass
        pass

    def on_tw_catalogue_db_clicked(self):
        # 若在目录中双击文件，则打开文件
        # 若在目录中双击标签，不操作
        pass

    # 拦截(设置)快捷键
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
