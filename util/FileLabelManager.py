
from typing import List

from PyQt5.QtCore import QStringListModel
from model.FileLabelModel import FileLabelModel
from util.ConfigEditor import ConfigEditor
from util.GlobalVarManager import GlobalVarManager
from util.Singleton import singleton

@ singleton
class FileLabelManager:
    """
        单例化，将标签写到本地
    """

    def __init__(self):
        self._conf_edt = ConfigEditor()
        self._lattice_edt = GlobalVarManager.lattice_edt
        # 用于充当ListView数据源
        label_name_list:List[str] = list()
        for label_model in self._conf_edt.get_all_label_model():
            label_name_list.append(label_model.label)
        self._label_list_model = QStringListModel(label_name_list)
        print("初始化FileLabelManager")

    def add_label(self, new_label: str) -> bool:
        if new_label in self._label_list_model.stringList():
            return False
        # 更新绑定数据源
        self._label_list_model.insertRow(self._label_list_model.rowCount())
        index = self._label_list_model.index(self._label_list_model.rowCount() - 1, 0)
        self._label_list_model.setData(index, new_label)

        # 更新本地数据项
        label_model = FileLabelModel(new_label,list())
        self._conf_edt.set_label_model(label_model)
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
        label_model = self._conf_edt.get_label_model(label_name)
        # 从文件中移除标签列表
        for file_name in label_model.file_name_list:
            # 读入文件模型
            file_model = self._conf_edt.get_file_model(file_name)
            # 移除文件标签
            file_model.remove_file_label(label_name)
            # 写入文件模型
            self._conf_edt.set_file_model(file_model)
        self._conf_edt.del_label(label_name)
        # 更新图数据库
        if len(label_model.file_name_list)>0:
            self._lattice_edt.remove_attribute(label_name)

    def get_file_name_list(self,label_name:str)->list:
        label_model = self._conf_edt.get_label_model(label_name)
        return label_model.file_name_list

    @property
    def label_list_model(self):
        return self._label_list_model

