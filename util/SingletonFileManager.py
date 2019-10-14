import json
import threading

from PyQt5.QtCore import  QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from database.model.lattice.ConceptNodeModel import ConceptNodeModel
from model.FileModel import FileModel
from util.GlobalVarManager import GlobalVarManager

from util.IconExtractor import IconExtractor
from util.SingletonConfigEditor import SingletonConfigEditor


class SingletonFileManager:
    """实现单例化,instance()取单例化对象
        将FileModel保存到本地
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        self._file_section = 'Files'
        self._label_section = 'Labels'
        # 用于充当ListView数据源
        self._file_list_model = QStandardItemModel()
        for file_name in SingletonConfigEditor.instance().get_all_options(self._file_section):
            json_dict = SingletonConfigEditor.instance().init_dict(self._file_section, file_name)
            abs_path = json_dict['abs_path']
            file_model = FileModel()
            file_model.abs_path = abs_path
            self._add_items(file_model)

        print("初始化SingletonFileManager")

    def add_file(self, file_model: FileModel)->bool:
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
        SingletonConfigEditor.instance().add_option(self._file_section, file_name, json.dumps(file_model.object2json()))
        for file_label in file_model.label_list:
            SingletonConfigEditor.instance().list_add(self._label_section, file_label, file_name)
        # 更新图数据库
        if len(file_model.label_list)>0:
            concept = self.file2concept(file_model)
            GlobalVarManager.lattice_editor.add_concept(concept)
        return True

    def delete_file(self, index:QModelIndex):
        file_name = index.data()
        # 更新绑定数据源
        self._file_list_model.removeRow(index.row())
        # 更新本地数据项
        # 初始化被删除的文件模型
        json_dict = json.loads(SingletonConfigEditor.instance().get_option(self._file_section, file_name))
        file_model = FileModel()
        file_model.load_json_dict(json_dict)
        # 从文件项中移除文件
        result = SingletonConfigEditor.instance().remove_option(self._file_section, file_name)
        # 从标签列表中移除文件
        for label in file_model.label_list:
            SingletonConfigEditor.instance().list_remove(self._label_section, label, file_name)
        # 更新图数据库
        if len(file_model.label_list)>0:
            # concept = self.file2concept(file_model)
            GlobalVarManager.lattice_editor.remove_object(file_model.file_name)
        return file_model.abs_path

    def get_abs_path(self,file_name)->str:
        file_dict= SingletonConfigEditor.instance().init_dict(self._file_section,file_name)
        return file_dict['abs_path']

    def get_label_list(self,file_name)->list:
        file_dict = SingletonConfigEditor.instance().init_dict(self._file_section, file_name)
        return file_dict['label_list']

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
        concept = ConceptNodeModel(intents=set(file_model.label_list),extents={file_model.file_name})
        return concept

    @classmethod
    def instance(cls):
        with SingletonFileManager._instance_lock:
            if not hasattr(SingletonFileManager, "_instance"):
                SingletonFileManager._instance = SingletonFileManager()
        return SingletonFileManager._instance
