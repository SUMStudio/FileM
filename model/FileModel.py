import json
import os
from typing import List


class FileModel:
    """初始化单个文件模型,通常仅在内存中保存正在编辑的实例化文件模型"""

    def __init__(self):
        self._file_name = ""
        self._abs_path = ""
        self.label_list = list()


    def add_file_label(self, label: str):
        self._label_list.append(label)

    def remove_file_label(self, label: str):
        self._label_list.remove(label)

    def open_file(self):
        os.system('cmd /c {}'.format(self._abs_path))

    @property
    def label_list(self) -> list:
        return self._label_list

    @label_list.setter
    def label_list(self, label_list):
        self._label_list = label_list

    @property
    def abs_path(self):
        return self._abs_path

    @abs_path.setter
    def abs_path(self, abs_path):
        self._abs_path = abs_path
        self._file_name = self._abs_path.split('/')[-1]

    @property
    def file_name(self):
        return self._file_name




