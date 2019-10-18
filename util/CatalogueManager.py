from typing import List

from PyQt5.QtGui import QStandardItem, QIcon, QStandardItemModel

from util.FileManager import FileManager
from util.IconExtractor import IconExtractor
from util.Singleton import singleton
from util.GlobalVarManager import GlobalVarManager


@singleton
class CatalogueManager:
    """
        单例化，管理目录结构
    """

    def __init__(self):
        self._root_abs_path = GlobalVarManager.root_abs_path
        self._lattice_edt = GlobalVarManager.lattice_edt
        self._file_mgr = FileManager()
        # 用于充当ListView数据源
        self._cat_list_model = QStandardItemModel()
        # 初始化目录
        self.init_catalogue()

    def init_catalogue(self):
        """从图数据库中读取路径用于填充"""
        self._cat_list_model.clear()
        self._cat_list_model.setHorizontalHeaderLabels(['节点名', '路径', '备注'])
        root_item: QStandardItem = self._cat_list_model.invisibleRootItem()
        parent_item = QStandardItem(QIcon(self._root_abs_path + "\\resources\\go-home.png"), "root")
        root_item.appendRow(parent_item)
        for path in self._lattice_edt.tree_model.get_root2leaf_path():
            print(path)
            depth = 1
            self._add_path(path, depth, parent_item, "root", len(path))

    def _add_path(self, path: List[str], depth: int, parent_item: QStandardItem, path_str: str, path_len: int):
        is_file = False
        if depth == path_len:
            return
        if depth == path_len - 1:
            # 为文件
            is_file = True
        node_name_list = path[depth]
        for node_name in node_name_list:
            note_str = "文件" if is_file else "文件夹"
            icon = QIcon(self._root_abs_path + "\\resources\\folder.png") if not is_file else IconExtractor(
                self._file_mgr.get_abs_path(node_name)).get_icon()
            node_item = QStandardItem(icon, node_name)
            path_str += "\\" + node_name
            path_item = QStandardItem(path_str)
            note_item = QStandardItem(note_str)
            parent_item.appendRow([node_item, path_item, note_item])
            self._add_path(path, depth + 1, node_item, path_str, path_len)

    @property
    def cat_list_model(self):
        return self._cat_list_model



