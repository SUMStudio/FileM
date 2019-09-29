# coding: utf-8
# import os
from os.path import dirname, realpath, join, exists, isdir, isfile
from os import makedirs, remove, removedirs
cur_dir = dirname(realpath(__file__))


def get_file_realpath(file):
    return join(cur_dir, file)


def check_and_create(absolute_file_path):
    slash_last_index = absolute_file_path.rindex("/")   # 返回‘/’在路径中最后出现的位置
    path = absolute_file_path[:slash_last_index]    # 取得目录的绝对路径
    # 检查目录
    if exists(path) is not True:
        makedirs(path)
    elif isdir(path) is not True:
        print(path, "is no a dir,delete and create a dir")
        remove(path)
        makedirs(path)
    # 检查文件
    if exists(absolute_file_path) is not True:
        with open(absolute_file_path, "w+", encoding="utf-8"):
            pass
    elif isfile(absolute_file_path) is not True:
        removedirs(absolute_file_path)
        with open(absolute_file_path, "w+", encoding="utf-8"):
            pass


def check_and_create_dir(absolute_dir_path):
    if exists(absolute_dir_path) is not True:
        makedirs(absolute_dir_path)
    elif isdir(absolute_dir_path) is not True:
        print(absolute_dir_path, "is no a dir,delete and create a dir")
        remove(absolute_dir_path)
        makedirs(absolute_dir_path)
