"""
复制
"""
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMimeData


class copy:
    def execute(self, script_variable):
        cur_path = script_variable["cur_path"]
        file_list = script_variable["file_list"]
        
        files = ""
        for f in file_list:
            files += "file://" + cur_path + "/" + f + "\r\n"
        
        mimeData = QMimeData()
        mimeData.setData("text/uri-list", files.encode())
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mimeData)
        
        print("成功复制到剪切板", files)
