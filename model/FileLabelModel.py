from typing import List


class FileLabelModel:
    def __init__(self,label:str,file_name_list:List[str]):
        self._label = label
        self._file_name_list = file_name_list

    @property
    def label(self):
        return self._label

    @property
    def file_name_list(self):
        return self._file_name_list