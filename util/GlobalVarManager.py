import os

from database.util.LatticeEditor import LatticeEditor


class GlobalVarManager:
    print("初始化GlobalVarManager")
    lattice_edt= LatticeEditor('fileM')
    # 项目根目录绝对路径
    root_abs_path = os.path.abspath('')
    print(root_abs_path)

