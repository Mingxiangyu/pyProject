# -*- codeing = utf-8 -*-
# @Time :2023/1/12 13:17
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://www.cnblogs.com/minseo/p/15745983.html
# @File :  解压tar.gz.py
import os
import tarfile


def untar(fname, dirs):
    t = tarfile.open(fname)
    t.extractall(path=dirs)


# print(os.listdir('tar_gz'))
# t=tarfile.open('tar_gz/1929.tar.gz')
# t.extractall(path='tar_gz/1929')

def _decomp_tar_gz(tar_file_dir):
    # 遍历压缩包文件夹，获取的是所有压缩包文件名的list
    for tar_gz_file in os.listdir(tar_file_dir):
        # print(tar_gz_file)
        # 把压缩的文件名使用.分割，取第一个元素作为解压缩文件的文件夹，例如文件2021.tar.gz则全部解压缩到文件夹tar_gz/2021下
        tar_gz_dir = tar_gz_file.split('.')[0]
        if os.path.isfile(f'{tar_file_dir}/{tar_gz_file}'):
            untar(f'{tar_file_dir}/{tar_gz_file}', f'{tar_file_dir}/{tar_gz_dir}')


# tar_file_dir 为带解压tar文件所在路径
tar_file_dir = r"/爬虫/下载NOAA全球气象数据/tar_gz"
_decomp_tar_gz(tar_file_dir)
