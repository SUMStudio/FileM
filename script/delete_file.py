"""
删除文件
"""
from os import remove
from os.path import join
from shutil import rmtree
from os.path import isfile, isdir

import fmconfig


class delete_file:
    def execute(self, script_variable):
        cur_path = script_variable["cur_path"]
        file_list = script_variable["file_list"]
        i_dict = fmconfig.init_dict("global", "labels")
        i_del = []
        for file in file_list:
            file_path = join(cur_path, file)
            if isfile(file_path):
                remove(file_path)
                print("删除文件成功，" + file_path)
                for i in i_dict:
                    if file in i_dict[i]:
                        i_dict[i].remove(file)
                        # if not i_dict[i]:
                        #     i_del.append(i)
                # for i in i_del:
                #     fmconfig.dict_del("global", "labels", i)

            elif isdir(file_path):
                rmtree(file_path)
                print("删除目录成功，" + file_path)
            else:
                print("无法删除的项目")
            fmconfig.dict_add("global", "labels", i_dict)
