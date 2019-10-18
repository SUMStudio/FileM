from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from model.FileModel import FileModel
from util.ConfigEditor import ConfigEditor
from util.GlobalVarManager import GlobalVarManager
from util.IconExtractor import IconExtractor
from util.Singleton import singleton


@singleton
class FileManager:
    """
        单例化，管理文件
    """

    def __init__(self):

        self._conf_edt = ConfigEditor()
        self._lattice_edt = GlobalVarManager.lattice_edt
        # 用于充当ListView数据源
        self._file_list_model = QStandardItemModel()
        for file_model in self._conf_edt.get_all_file_model():
            self._add_items(file_model)

        print("初始化FileManager")

    def add_file(self, file_model: FileModel) -> bool:
        file_name = file_model.file_name
        root_item = self._file_list_model.invisibleRootItem()
        index = 0
        item = root_item.child(index)
        while item:
            if item.text() == file_name:
                return False
            index += 1
            item = root_item.child(index)
        # 更新绑定数据源
        self._add_items(file_model)
        # 更新本地数据项
        self._conf_edt.set_file_model(file_model)
        for label_name in file_model.label_list:
            label_model = self._conf_edt.get_label_model(label_name)
            if label_name not in label_model.file_name_list:
                label_model.file_name_list.append(file_name)
            self._conf_edt.set_label_model(label_model)
        # 更新图数据库
        if len(file_model.label_list) > 0:
            concept = self.file2concept(file_model)
            self._lattice_edt.add_concept(concept)
        return True

    def delete_file(self, index: QModelIndex):
        file_name = index.data()
        # 更新绑定数据源
        self._file_list_model.removeRow(index.row())
        # 更新本地数据项
        file_model = self._conf_edt.get_file_model(file_name)
        # 从文件项中移除文件
        self._conf_edt.del_file(file_name)
        # 从标签列表中移除文件
        for label in file_model.label_list:
            label_model = self._conf_edt.get_label_model(label)
            label_model.file_name_list.remove(file_name)
            self._conf_edt.set_label_model(label_model)
        # 更新图数据库
        if len(file_model.label_list) > 0:
            self._lattice_edt.remove_object(file_name)
        return file_model.abs_path

    def get_abs_path(self, file_name) -> str:
        file_model = self._conf_edt.get_file_model(file_name)
        return file_model.abs_path

    def get_label_list(self, file_name) -> list:
        file_model = self._conf_edt.get_file_model(file_name)
        return file_model.label_list

    def _add_items(self, file_model: FileModel):
        file_name = file_model.file_name
        abs_path = file_model.abs_path
        root_item = self._file_list_model.invisibleRootItem()
        item = QStandardItem(IconExtractor(abs_path).get_icon(), file_name)
        root_item.appendRow(item)

    @property
    def file_list_model(self):
        return self._file_list_model

    @staticmethod
    def file2concept(file_model: FileModel) -> ConceptNodeModel:
        """文件模型转为概念模型"""
        concept = ConceptNodeModel(intents=set(file_model.label_list), extents={file_model.file_name})
        return concept
