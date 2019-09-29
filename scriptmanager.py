"""
脚本管理
待完善
用于构建文件浏览器的各项功能
"""

# import importlib
from importlib import import_module
from os.path import splitext    # dirname   # splitext()用于分享文件名与拓展名，返回元组
from PyQt5.QtWidgets import QDialog, QAction, QMessageBox       # QListWidgetItem,
from PyQt5.QtCore import pyqtSignal     # pyqtSlot,
# import fmconfig
from fmconfig import init_dict


class ScriptManager(QDialog):
    show_script_result_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # self.init_dict()        # 初始化脚本字典
        self.temp_variable = {}     # 存入脚本的临时变量

    # def init_dict(self):
        self.script_dict = init_dict("script", "customer_script")
         
    def load_plugin(self, filename, filepath, file_list):
        print("loading plugin:" + 'FileM.script.' + splitext(filename)[0])

        script_module = import_module('script.' + splitext(filename)[0])
        script_class = getattr(script_module, splitext(filename)[0])
        o = script_class()      # 实例化脚本对象
        self.temp_variable["cur_path"] = filepath
        self.temp_variable["file_list"] = file_list
        try:
            o.execute(self.temp_variable)
        except Exception as e:
            print("检测异常", e)
            QMessageBox.information(self, "系统异常", str(e), QMessageBox.Ok)
        print("temp_variable:", self.temp_variable)

    # def get_file_menu_item(self):
    #     # 遍历字典取得右键菜单选项
    #     sc_items = self.script_dict.items()
    #     actions = set()
    #     for sc in sc_items:
    #         if sc[1]["apply_type"] == 1:
    #             action = QAction(sc[0])
    #             actions.add(action)
    #     return actions

    def run_script(self, script_name, filepath, file_list):
        script_path = self.script_dict[script_name]["path"]
        print("script_path:" + script_path)
        self.load_plugin(script_path, filepath, file_list)
