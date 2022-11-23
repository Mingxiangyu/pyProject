# -*- codeing = utf-8 -*-
# @Time :2022/11/23 11:46
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  新建文件夹.py
import os


# 新建文件夹函数，便于分站点存储数据
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    else:
        pass
