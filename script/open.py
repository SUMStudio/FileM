"""
打开文件

"""
try:
    from os import startfile
except Exception as e:
    pass
from sys import platform
from os import system
from os.path import join


class open:
    def execute(self, script_variable):
        cur_path = script_variable["cur_path"]
        cur_file = script_variable["file_list"][0]
        cur_item = join(cur_path, cur_file)
        if platform == "win32":
            startfile(cur_item)
        else:
            system('x-terminal-emulator --working-directory={} &'.format(script_variable["cur_item"]))    # linux
