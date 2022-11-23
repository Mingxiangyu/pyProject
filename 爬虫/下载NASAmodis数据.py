# -*- codeing = utf-8 -*-
# @Time :2022/11/22 16:56
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://blog.csdn.net/qq_62257457/article/details/126864449
# @File :  下载NASAmodis数据.py
import re

import numpy as np
import requests


class modis_download(object):
    ''' 初始化Modis数据下载的参数 '''

    def __init__(self,
                 modis_url='https://e4ftl01.cr.usgs.gov',
                 tiles=None,  # 设置默认条带号
                 path='MOLT',  # 下载地址与产品目录之间的文件夹
                 product=None,  # 产品类型
                 star_time=None,  # 开始时间
                 end_time=None,  # 结束时间
                 ):
        self.modis_url = modis_url
        self.tiles = tiles
        self.path = path
        self.product = product
        self.star_time = star_time
        self.end_time = end_time

    # 定义爬取数据的方法
    def down_load_conect(self, path_time):
        # 设置headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
        }
        # 拼接下载连接
        url = self.modis_url + '/' + self.path + '/' + self.product + '/' + path_time + '/'

        response = requests.get(url)
        html = response.text

        regular = f'<a.+?href=\\"(.+{self.tiles}.*.hdf?)\\".*>'  # 正则表达式获取指定条带号数据
        hdf_list = re.findall(regular, html)

        # 写文件
        print(f'{path_time}总共有{len(hdf_list)}个连接')
        a = 0  # 文件计数
        for i in hdf_list:
            url_download = url + i
            with open('data.txt', 'a') as f:  # 统一到一个data.txt文件中
                f.writelines(url_download + '\n')
                a += 1
                print(f'已经写入{a}个连接')

    # 获取时间
    def path_time_get(self, star_time, end_time):
        time_path = self.modis_url + '/' + self.path + '/' + self.product + '/'
        response = requests.get(time_path)

        html = response.text
        regular = r'<a.+?href=\"(\d.*)/\".*>'  # 正则表达式
        time_list = re.findall(regular, html)
        regular_num = u"([^\u0030-\u0039])"  # 只保留数字
        for i in range(len(time_list)):
            time_list[i] = int(re.sub(regular_num, '', time_list[i]))  # 将time_list  str 转为 int
        time_list_array = np.array(time_list)
        result_time = time_list_array[np.where((time_list_array >= star_time) & (time_list_array <= end_time))]
        result_time = result_time.astype(str)

        for i in range(len(result_time)):
            result_time[i] = result_time[i][:4] + '.' + result_time[i][4:6] + '.' + result_time[i][6:8]  # 格式化时间

        return result_time

    def main_get(self):
        time_list = self.path_time_get(self.star_time, self.end_time)
        for i in time_list:
            self.down_load_conect(i)

        print('写入完成！')


if __name__ == '__main__':
    # 根据需要修改参数，以下为参数格式参考
    download = modis_download(product='MOD13Q1.061', star_time=20190218, end_time=20190306, tiles='h26v06')

    download.main_get()
