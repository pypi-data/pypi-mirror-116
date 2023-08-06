# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   MfyPublic
# FileName:     read_data
# Author:      MingFeiyang
# Datetime:    2021/8/14 9:51
# -----------------------------------------------------------------------------------
import json
import openpyxl
import configparser
import os
import yaml

from mfypublic.get_path import get_file_path


class ReadData:

    def get_file_path(self, pro_name, ini_path, section_name, file_name):
        """
        读取ini文件，获取完整路径
        :param pro_name: 项目名字
        :param ini_path: ini文件在项目中的路径
        :param section_name: ini文件中section的名字
        :param file_name: ini文件中配置的路径的名字
        :return:
        """
        config = configparser.ConfigParser()
        before_path = get_file_path(pro_name)
        config.read(os.path.join(before_path, ini_path))
        path = config.get(section_name, file_name)
        return os.path.join(before_path, path)

    def get_excel_data(self, path, sheet_name):
        """
        读取excel文件数据，数据格式是[[],[],[]]
        :param path: excel文件的路径
        :param sheet_name: sheet页的名字
        :return:
        """
        excel_file = openpyxl.load_workbook(path)
        get_sheet = excel_file[sheet_name]
        all_list = []
        for hang_tuple in get_sheet:
            list1 = []
            for i in hang_tuple:
                list1.append(i.value)
            all_list.append(list1)
        return all_list[1:]

    def get_json_data(self, path):
        """
        读取josn文件的数据
        :param path: json文件路径
        :return:
        """
        with open(path, encoding="utf8") as j_file:
            return json.load(j_file)

    def get_yaml_data(self, path):
        """
        读取yaml文件数据
        :param path: yaml文件路径
        :return:
        """
        with open(path, mode="r", encoding="utf8") as yaml1:
            return yaml.safe_load(yaml1)
