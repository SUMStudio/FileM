
from os.path import exists

from PyQt5.QtCore import  QItemSelection
from PyQt5.QtGui import QCursor


from gui.menu.CatalogueMenu import CatalogueMenu
from gui.menu.FileEditMenu import FileEditMenu
from gui.menu.LabelEditMenu import LabelEditMenu
from util.FileLabelManager import FileLabelManager
from util.FileManager import FileManager


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
        if not selected.indexes():
            return
        sender = self._window.sender()
        if sender == self._window.lv_file.selectionModel():
            file_name = selected.indexes()[0].data()
            label_list = FileManager().get_label_list(file_name)
            self.show_message("{}:标签为{}".format(file_name,str(label_list)))
        elif sender == self._window.lv_label.selectionModel():
            label_name = selected.indexes()[0].data()
            file_name_list = FileLabelManager().get_file_name_list(label_name)
            self.show_message("{}:文件为{}".format(label_name, str(file_name_list)))

    def show_message(self, msg: str):
        self._window.lb_info.setText(msg)


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


