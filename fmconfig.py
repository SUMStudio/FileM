"""
配置文件控制
初始化：init_list(),init_dict() 分別返回列表、字典
修改配置文件中的列表：list_add(),list_del()
修改配置文件中的字典：dict_add()
"""

from json import dumps, loads
from configparser import ConfigParser
from fileutil import check_and_create, get_file_realpath

config_file = get_file_realpath("data/config.ini")
check_and_create(config_file)
cf = ConfigParser()
cf.read(config_file, encoding="utf-8")  # 读取配置文件


def list_add(section, option, value):
    option_list = init_list(section, option)
    option_list.append(value)
    cf.set(section, option, dumps(option_list, ensure_ascii=False))
    with open(config_file, "w", encoding="utf-8") as f:
        cf.write(f)


def list_del(section, option, value):
    option_list = init_list(section, option)
    option_list.remove(value)
    cf.set(section, option, dumps(option_list, ensure_ascii=False))
    with open(config_file, "w", encoding="utf-8") as f:
        cf.write(f)


def init_list(section, option):
    if not cf.has_section(section):
        cf.add_section(section)
    option_list = []
    if cf.has_option(section, option):
        string_option = cf.get(section, option)
        if string_option:
            option_list = loads(string_option)
    return option_list


def dict_add(section, option, value):
    option_dict = init_dict(section, option)
    option_dict.update(value)
    cf.set(section, option, dumps(option_dict, ensure_ascii=False))
    with open(config_file, "w", encoding="utf-8") as f:
        cf.write(f)


def dict_del(section, option, value):
    option_dict = init_dict(section, option)
    option_dict.pop(value)
    cf.set(section, option, dumps(option_dict, ensure_ascii=False))
    with open(config_file, "w", encoding="utf-8") as f:
        cf.write(f)


def init_dict(section, option):
    if not cf.has_section(section):     # 检查section是否存在于配置文件中，没有则新增
        cf.add_section(section)

    # 用option_dict存储配置文件中section下option的值，并返回一个包含它的值的列表
    option_dict = {}
    if cf.has_option(section, option):
        string_option = cf.get(section, option)
        if string_option:
            option_dict = loads(string_option)
    return option_dict
