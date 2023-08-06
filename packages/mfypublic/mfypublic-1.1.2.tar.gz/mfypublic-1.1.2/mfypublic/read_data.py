# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   MfyPublic
# FileName:     read_data
# Author:      MingFeiyang
# Datetime:    2021/8/14 9:51
# -----------------------------------------------------------------------------------
import json
import openpyxl
import yaml

class ReadData:

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
