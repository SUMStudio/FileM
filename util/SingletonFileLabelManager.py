import json
import threading

from PyQt5.QtCore import QStringListModel

from model.FileModel import FileModel
from util.GlobalVarManager import GlobalVarManager
from util.SingletonConfigEditor import SingletonConfigEditor


class SingletonFileLabelManager:
    """实现单例化,instance()取单例化对象
        将标签写到本地
    """
    _instance_lock = threading.Lock()

    def __init__(self):
        self._file_section = 'Files'
        self._label_section = 'Labels'
        # 用于充当ListView数据源
        self._label_list_model = QStringListModel(SingletonConfigEditor.instance().get_all_options(self._label_section))
        print("初始化SingletonFileLabelManager")

    def add_label(self, new_label: str) -> bool:
        if new_label in self._label_list_model.stringList():
            return False
        # 更新绑定数据源
        self._label_list_model.insertRow(self._label_list_model.rowCount())
        index = self._label_list_model.index(self._label_list_model.rowCount() - 1, 0)
        self._label_list_model.setData(index, new_label)

        # 更新本地数据项
        SingletonConfigEditor.instance().add_option(self._label_section, new_label, '[]')
        return True

    def remove_labels(self, indexes):
        for index in indexes:
            self.remove_label(index)

    def remove_label(self, index):
        label_name = index.data()
        # 更新绑定数据源
        self._label_list_model.removeRow(index.row())
        # 更新本地数据项
        # 初始化被移除标签
        file_name_list = SingletonConfigEditor.instance().init_list(self._label_section, label_name)
        # 从文件中移除标签列表
        for file_name in file_name_list:
            # 读入文件模型
            json_dict = json.loads(SingletonConfigEditor.instance().get_option(self._file_section, file_name))
            file_model = FileModel()
            file_model.load_json_dict(json_dict)
            # 移除
            file_model.remove_file_label(label_name)
            # 写入文件模型
            SingletonConfigEditor.instance().add_option(self._file_section, file_name,
                                                        json.dumps(file_model.object2json()))
        result = SingletonConfigEditor.instance().remove_option(self._label_section, label_name)
        # 更新图数据库
        if len(file_name_list)>0:
            GlobalVarManager.lattice_editor.remove_attribute(label_name)

    def get_file_name_list(self,label_name:str)->list:
        file_name_list = SingletonConfigEditor.instance().init_list(self._label_section,label_name)
        return file_name_list

    @property
    def label_list_model(self):
        return self._label_list_model

    @classmethod
    def instance(cls):
        with SingletonFileLabelManager._instance_lock:
            if not hasattr(SingletonFileLabelManager, "_instance"):
                SingletonFileLabelManager._instance = SingletonFileLabelManager()
        return SingletonFileLabelManager._instance
