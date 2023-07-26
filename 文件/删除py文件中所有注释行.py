# -*- codeing = utf-8 -*-
# @Time :2023/7/25 9:26
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://www.jb51.net/article/66683.htm
# @Link : https://blog.csdn.net/qq_43470698/article/details/128410859
# @Link : https://www.cnblogs.com/kyle-blog/p/15267474.html
# @Link : https://blog.csdn.net/qq_36387683/article/details/104036954
# @File :  删除py文件中注释行.py
# !/usr/bin/python
import os
import re
import shutil


def remove_comments(code):
    # 删除多行注释
    code = re.sub(r'""".*?"""', '', code, flags=re.DOTALL)
    code = re.sub(r"'''.*?'''", '', code, flags=re.DOTALL)

    # 先匹配出所有字符串
    strings = re.findall(r'(".*?"|\'. *?\')', code)
    # 替换字符串，避免字符串中包含 # 后被移除
    for s in strings:
        code = code.replace(s, '$$')

    # 删除单行注释
    code = re.sub(r'#.*$', '', code, flags=re.MULTILINE)

    # 删除行尾注释
    code = re.sub(r'#[^\n]*', '', code)

    # 还原字符串
    for s in strings:
        code = code.replace('$$', s, 1)
    return code


def restoreTheOriginalHierarchyInTheNewDirectory(SrcPath, DescPath, FileList):
    # 如果目的文件夹不存在，创建之
    if not os.path.exists(DescPath):
        os.makedirs(DescPath)

    # 获取需要处理的py文件集合
    for ipath in os.listdir(SrcPath):
        SrcFile = os.path.join(SrcPath, ipath)  # 拼接成绝对路径
        TargetFile = os.path.join(DescPath, ipath)  # 新目录中还原原始结构
        # 判断文件是否为 Python 文件
        if os.path.splitext(SrcFile)[1] == ".py":
            # 读取并处理文件
            fobj = open(SrcFile, 'r', encoding='utf-8')
            content = fobj.read()
            comments = remove_comments(content)
            with open(TargetFile, "w", encoding="utf-8") as f:
                f.write(comments)
        else:
            # 如果不是python则正常复制
            print(SrcFile)  # 打印相关后缀的文件路径及名称
            if os.path.isfile(SrcFile):  # 文件，匹配->打印
                shutil.copy(SrcFile, TargetFile)
            if os.path.isdir(SrcFile):  # 目录，递归
                FileList = restoreTheOriginalHierarchyInTheNewDirectory(SrcFile, TargetFile, FileList)
    return FileList


if __name__ == '__main__':
    SrcPath = r"C:\Users\zhouhuilin\Desktop\DetectionDemo"  # 源文件夹
    DescPath = r"C:\Users\zhouhuilin\Desktop\DetectionDemo-back"  # 目的文件夹

    FileList = []
    restoreTheOriginalHierarchyInTheNewDirectory(SrcPath, DescPath, FileList)

print('>>>End<<<')
