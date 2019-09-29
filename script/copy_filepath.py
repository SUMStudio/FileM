"""
复制文件的完整路径,仅支持单个文件操作
"""
from PyQt5.QtWidgets import QApplication
from os.path import join


class copy_filepath:
    def execute(self, script_variable):
        cur_filepath = join(script_variable["cur_path"], script_variable["file_list"][0])
        clipboard = QApplication.clipboard()
        clipboard.setText(cur_filepath)
