# -*- codeing = utf-8 -*-
# @Time :2023/10/13 10:20
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  获取项目根路径.py
# 获得根路径
import os


def getRootPath():
    # 获取文件目录
    curPath = os.path.abspath(os.path.dirname(__file__))
    # 获取项目根路径，内容为当前项目的名字
    rootPath = curPath[:curPath.find("pyProject")+len("pyProject")]
    print(rootPath)
    return  rootPath

getRootPath()