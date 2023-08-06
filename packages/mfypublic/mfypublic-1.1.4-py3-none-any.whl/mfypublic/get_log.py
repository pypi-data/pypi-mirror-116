# -*- coding:utf8 -*- #
#-----------------------------------------------------------------------------------
# ProjectName:   MfyPublic
# FileName:     get_log
# Author:      MingFeiyang
# Datetime:    2021-05-21 11:02
#-----------------------------------------------------------------------------------
import logging
import sys

def get_logging(log_path):
    # 实例化对象
    log = logging.Logger("name")
    # 设置格式
    set_format = logging.Formatter("[%(filename)s][%(asctime)s]:%(message)s")

    # 打印日志到指定位置
    # 实例化对象
    fh = logging.FileHandler(log_path)
    # 调用设置好的格式，来规范日志
    fh.setFormatter(set_format)
    # 保存存日志
    log.addHandler(fh)

    # 打印日志到控制台
    sh = logging.StreamHandler(sys.stdout)
    # 设置日志格式
    sh.setFormatter(set_format)
    # 保存日志
    log.addHandler(sh)

    return log