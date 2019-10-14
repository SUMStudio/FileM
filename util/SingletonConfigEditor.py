import os
from json import dumps, loads
from configparser import ConfigParser

from util.GlobalVarManager import GlobalVarManager
from util.fileutil import check_and_create
import threading


class SingletonConfigEditor:
    """实现单例化,instance()取单例化对象"""
    """
    配置文件控制
    初始化：init_list(),init_dict() 分別返回列表、字典
    修改配置文件中的列表：list_add(),list_del()
    修改配置文件中的字典：dict_add()
    """

    _instance_lock = threading.Lock()

    def __init__(self):
        self.config_file = GlobalVarManager.root_abs_path+"\data\config.ini"
        print('配置文件绝对路径{}'.format(self.config_file))
        check_and_create(self.config_file)
        self.cf = ConfigParser()
        self.cf.read(self.config_file, encoding="utf-8")  # 读取配置文件
        print("初始化SingletonConfigEditor")

    def list_add(self, section, option, value):
        option_list = self.init_list(section, option)
        option_list.append(value)
        self.cf.set(section, option, dumps(option_list, ensure_ascii=False))
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)

    def list_remove(self, section, option, value):
        option_list = self.init_list(section, option)
        option_list.remove(value)
        self.cf.set(section, option, dumps(option_list, ensure_ascii=False))
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)

    def init_list(self, section, option):
        option_list = []
        if not self.cf.has_section(section):
            self.cf.add_section(section)
            with open(self.config_file, "w", encoding="utf-8") as f:
                self.cf.write(f)
        else:
            string_option = self.cf.get(section, option)
            if string_option:
                option_list = loads(string_option)
        return option_list

    def dict_add(self, section, option, value):
        option_dict = self.init_dict(section, option)
        option_dict.update(value)
        self.cf.set(section, option, dumps(option_dict, ensure_ascii=False))
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)

    def dict_del(self, section, option, value):
        option_dict = self.init_dict(section, option)
        option_dict.pop(value)
        self.cf.set(section, option, dumps(option_dict, ensure_ascii=False))
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)

    def init_dict(self, section, option) -> dict:
        # 用option_dict存储配置文件中section下option的值，并返回一个包含它的值的列表
        option_dict = {}
        if not self.cf.has_section(section):  # 检查section是否存在于配置文件中，没有则新增
            self.cf.add_section(section)
            with open(self.config_file, "w", encoding="utf-8") as f:
                self.cf.write(f)
        else:
            string_option = self.cf.get(section, option)
            if string_option:
                option_dict = loads(string_option)
        return option_dict

    def get_option(self, section, option):
        return self.cf.get(section,option)


    def get_all_options(self, section) -> list:
        if not self.cf.has_section(section):  # 检查section是否存在于配置文件中，没有则新增
            self.cf.add_section(section)
            with open(self.config_file, "w", encoding="utf-8") as f:
                self.cf.write(f)
        # 取section下的所有option
        return self.cf.options(section)

    def add_option(self,section,option,value):
        # 在section下添加option
        self.cf.set(section,option,value)
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)

    def remove_option(self, section, option) -> bool:
        # 在section下的移除option
        result = self.cf.remove_option(section, option)
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)
        return result

    @classmethod
    def instance(cls):
        with SingletonConfigEditor._instance_lock:
            if not hasattr(SingletonConfigEditor, "_instance"):
                SingletonConfigEditor._instance = SingletonConfigEditor()
        return SingletonConfigEditor._instance


if __name__ == "__main__":
    # 测试单例化
    a = SingletonConfigEditor.instance()
    b = SingletonConfigEditor.instance()
    print(a)
    print(b)
