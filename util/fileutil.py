# coding: utf-8
from os.path import exists, isdir, isfile, dirname
from os import makedirs, remove, removedirs


def check_and_create(absolute_file_path):
    path = dirname(absolute_file_path)
    # 检查目录
    if not exists(path):
        makedirs(path)
    elif not isdir(path):
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
