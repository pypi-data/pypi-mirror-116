# -*- coding:utf8 -*- #
# -----------------------------------------------------------------------------------
# ProjectName:   MfyPublic
# FileName:     get_path
# Author:      MingFeiyang
# Datetime:    2021-05-20 16:44
# -----------------------------------------------------------------------------------
import os


def get_file_path(path1):
    """
    需要的文件的路径
    :param path1: 文件路径
    :return:
    """
    # 通过分割实参得到项目名字
    pro_name = path1.split("/")[0]
    # 获取到当前文件的路径
    path = os.path.dirname(__file__)
    # 通过项目名字分割路径，获取到项目在电脑上的路径
    before_path = path.split(pro_name)[0]
    # 把获取的项目路径和实参进行拼接得到完整路径
    return os.path.join(before_path, path1)

