# -*- codeing = utf-8 -*-
# @Time :2023/7/25 11:24
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : 原文链接：https://blog.csdn.net/qq_44761198/article/details/126890504
# @File :  文件夹内(包含子级)所有文件复制到另一个文件夹下.py
import os
import shutil

SrcPath = r"C:\Users\zhouhuilin\Desktop\DetectionDemo"  # 源文件夹
DescPath = r"C:\Users\zhouhuilin\Desktop\DetectionDemo-back"  # 目的文件夹


def restoreTheOriginalHierarchyInTheNewDirectory(SrcPath, DescPath):
    """
    新目录中还原原始层级
    @param SrcPath:
    @param DescPath:
    """
    # 如果目的文件夹不存在，创建之
    if not os.path.exists(DescPath):
        os.makedirs(DescPath)
    for ipath in os.listdir(SrcPath):
        SrcFile = os.path.join(SrcPath, ipath)  # 拼接成绝对路径
        TargetFile = os.path.join(DescPath, ipath)  # 新目录中还原原始结构
        print(SrcFile)  # 打印相关后缀的文件路径及名称
        if os.path.isfile(SrcFile):  # 文件，匹配->打印
            shutil.copy(SrcFile, TargetFile)
        if os.path.isdir(SrcFile):  # 目录，递归
            restoreTheOriginalHierarchyInTheNewDirectory(SrcFile, TargetFile)


def FindFile(SrcPath, DescPath):
    """
    所有文件都放到 目标目录根下
    @param SrcPath:
    @param DescPath:
    """
    for ipath in os.listdir(SrcPath):
        fulldir = os.path.join(SrcPath, ipath)  # 拼接成绝对路径
        print(fulldir)  # 打印相关后缀的文件路径及名称
        if os.path.isfile(fulldir):  # 文件，匹配->打印
            shutil.copy(fulldir, DescPath)
        if os.path.isdir(fulldir):  # 目录，递归
            FindFile(fulldir, DescPath)


# 所有文件（包含子文件）都平铺
FindFile(SrcPath, DescPath)

# 还原原始结构
restoreTheOriginalHierarchyInTheNewDirectory(SrcPath, DescPath)
