# -*- codeing = utf-8 -*-
# @Time :2022/11/25 10:51
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  对文件夹夹文件内容的操作.py

import glob
import os

path = r'E:\Persona_project\6S\data\Landsat8\LC81260362017228LGN00'
# os.walk循环当前目录与下级目录，直到目录全部遍历完
for root, dirs, RSFiles in os.walk(path):
    print('-' * 1000)
    print(root)  # 所指的是当前正在遍历的这个文件夹的本身的地址
    print(dirs)  # 内容是该文件夹中所有的目录的名字(不包括子目录)
    print(RSFiles)  # 内容是该文件夹中所有的文件(不包括子目录)
print(glob.glob(os.path.join(path, '*MTL.txt')))  # 某类文件的全路径列表
