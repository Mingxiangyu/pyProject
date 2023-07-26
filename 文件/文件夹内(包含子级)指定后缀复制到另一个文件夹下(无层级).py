# -*- codeing = utf-8 -*-
# @Time :2023/7/25 11:24
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  文件夹内(包含子级)所有文件复制到另一个文件夹下(无层级).py
import os
import shutil

SrcPath = r"C:\Users\zhouhuilin\Desktop\DetectionDemo"  # 源文件夹
DescPath = r"C:\Users\zhouhuilin\Desktop\DetectionDemo-back"  # 目的文件夹
suffix = '.xml'  # 要复制的文件后缀


def FindFile(SrcPath, DescPath, suffix):
    for ipath in os.listdir(SrcPath):
        fullDir = os.path.join(SrcPath, ipath)  # 拼接成绝对路径
        if suffix in os.path.split(fullDir)[1]:  # 查找包含了指定关键字的文件
            print(fullDir)  # 打印相关后缀的文件路径及名称
            if os.path.isfile(fullDir):  # 文件，匹配->打印
                shutil.copy(fullDir, DescPath)
            if os.path.isdir(fullDir):  # 目录，递归
                FindFile(fullDir, DescPath)


FindFile(SrcPath, DescPath, suffix)
