"""
重命名文件
"""
from os.path import join
from os import rename as osRename
from PyQt5.QtWidgets import QInputDialog
import fmconfig


class rename:
    def execute(self, script_variable):
        origin_name = script_variable["file_list"][0]
        cur_path = script_variable["cur_path"]
        cur_file = join(cur_path, origin_name)
        i_dict = fmconfig.init_dict("global", "labels")
        print(cur_file)
        new_name, ok = QInputDialog.getText(None, "重命名文件", "请输入一个新名称：")
        if ok and new_name != origin_name:
            osRename(cur_file, join(cur_path, new_name))
            print("重命名文件：" + cur_file + "->" + join(cur_path, new_name))
            for i in i_dict:
                if origin_name in i_dict[i]:
                    i_dict[i].remove(origin_name)
                    i_dict[i].append(new_name)
        fmconfig.dict_add("global", "labels", i_dict)
