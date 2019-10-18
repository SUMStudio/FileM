
import json
from configparser import ConfigParser
from typing import Generator, Iterable

from model.FileLabelModel import FileLabelModel
from model.FileModel import FileModel
from util.fileutil import check_and_create
from util.GlobalVarManager import GlobalVarManager
from util.Singleton import singleton

@ singleton
class ConfigEditor:
    """
    单例化，FileModel,FileLabelModel写到配置
    """

    def __init__(self):

        self.config_file = GlobalVarManager.root_abs_path+"\data\config.ini"
        print('配置文件绝对路径{}'.format(self.config_file))
        check_and_create(self.config_file)

        self._file_section = 'Files'
        self._label_section = 'Labels'

        self.cf = ConfigParser()
        self.cf.read(self.config_file, encoding="utf-8")  # 读取配置文件
        print("初始化ConfigEditor")

    def get_file_model(self,file_name:str)->FileModel:
        """
        :param file_name:要获取的文件名
        :return: FileModel:返回获取的文件模型
        """
        json_dict = self._init_dict(self._file_section,file_name)
        file_model = FileModel()
        file_model.abs_path = json_dict['abs_path']
        file_model.label_list = json_dict['label_list']
        return file_model

    def get_all_file_model(self)->Iterable[FileModel]:
        """
        取所有文件模型
        :return:
        """
        for file_name in self._get_all_options(self._file_section):
            yield self.get_file_model(file_name)

    def del_file(self,file_name:str):
        """

        :param file_name: 要删除的文件名
        :return:
        """
        self._remove_option(self._file_section,file_name)

    def get_label_model(self,label_name:str)->FileLabelModel:
        """

        :param label_name: 要获取的标签名
        :return: 返回获取的文件标签模型
        """
        json_dict = self._init_dict(self._label_section, label_name)
        label_model = FileLabelModel(label_name,json_dict['file_name_list'])
        return label_model

    def set_file_model(self,file_model:FileModel):
        """
        :param file_model: 要存储的文件模型
        :return:
        """
        json_dict = dict()
        json_dict['abs_path']= file_model.abs_path
        json_dict['label_list'] = file_model.label_list
        self._add_option(self._file_section,file_model.file_name,json.dumps(json_dict, ensure_ascii=False))

    def set_label_model(self,label_model:FileLabelModel):
        """

        :param label_model: 要存储的文件标签模型
        :return:
        """
        json_dict = dict()
        json_dict['file_name_list'] = label_model.file_name_list
        self._add_option(self._label_section, label_model.label, json.dumps(json_dict, ensure_ascii=False))

    def get_all_label_model(self)->Iterable[FileLabelModel]:
        """
        取所有文件标签模型
        :return:
        """
        for label_name in self._get_all_options(self._label_section):
            yield self.get_label_model(label_name)

    def del_label(self, label_name: str):
        """

        :param label_name: 要删除的文件名
        :return:
        """
        self._remove_option(self._label_section, label_name)


    def _list_add(self, section, option, value):
        option_list = self._init_list(section, option)
        option_list.append(value)
        self.cf.set(section, option, json.dumps(option_list, ensure_ascii=False))
        self._write_conf()

    def _list_remove(self, section, option, value):
        option_list = self._init_list(section, option)
        option_list.remove(value)
        self.cf.set(section, option, json.dumps(option_list, ensure_ascii=False))
        self._write_conf()

    def _init_list(self, section, option):
        option_list = []
        if not self.cf.has_section(section):
            self.cf.add_section(section)
            self._write_conf()
        else:
            string_option = self.cf.get(section, option)
            if string_option:
                option_list = json.loads(string_option)
        return option_list

    def _dict_add(self, section, option, value):
        option_dict = self._init_dict(section, option)
        option_dict.update(value)
        self.cf.set(section, option, json.dumps(option_dict, ensure_ascii=False))
        self._write_conf()

    def _dict_del(self, section, option, value):
        option_dict = self._init_dict(section, option)
        option_dict.pop(value)
        self.cf.set(section, option, json.dumps(option_dict, ensure_ascii=False))
        self._write_conf()

    def _init_dict(self, section, option) -> dict:
        option_dict = {}
        if not self.cf.has_section(section):
            self.cf.add_section(section)
            self._write_conf()
        else:
            string_option = self.cf.get(section, option)
            if string_option:
                option_dict = json.loads(string_option)
        return option_dict

    def _get_option(self, section, option):
        return self.cf.get(section,option)


    def _get_all_options(self, section) -> list:
        if not self.cf.has_section(section):  # 检查section是否存在于配置文件中，没有则新增
            self.cf.add_section(section)
            self._write_conf()
        # 取section下的所有option
        return self.cf.options(section)

    def _add_option(self,section,option,value):
        # 在section下添加option
        self.cf.set(section,option,value)
        self._write_conf()

    def _remove_option(self, section, option) -> bool:
        # 在section下的移除option
        result = self.cf.remove_option(section, option)
        self._write_conf()
        return result


    def _write_conf(self):
        with open(self.config_file, "w", encoding="utf-8") as f:
            self.cf.write(f)