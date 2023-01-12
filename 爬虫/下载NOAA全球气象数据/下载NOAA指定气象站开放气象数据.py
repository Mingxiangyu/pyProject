# -*- codeing = utf-8 -*-
# @Time :2023/1/12 13:11
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://www.cnblogs.com/minseo/p/15745983.html
# @File :  下载NOAA指定气象站开放气象数据.py
import os

import requests

base_url = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/access/{}/{}.csv'
# 定义请求头部信息
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"}
year_list = [2022]
station_list = [
    54511099999,  # 北京数据编号 站点为54511
    47662099999,  # 东京数据编号
    47108099999,  # 首尔数据编号
    45007099999,  # 香港数据编号
]
for year in year_list:
    for station_number in station_list:
        requests_url = base_url.format(year,station_number)
        # 打印拼接以后的下载链接
        print(requests_url)
        # 通过下载链接创建对象r
        r = requests.get(requests_url)
        # 如果当前文件夹没有tar_gz目录则创建该目录
        file_dir = 'tar_gz'
        if file_dir not in [x for x in os.listdir('..') if os.path.isdir(x)]:
            try:
                os.mkdir('tar_gz')
            except:
                print('创建文件夹失败')
        else:
            print("文件目录已存在")
        # 如果在目录tar_gz下已经有文件了则不重复下载,否则下载
        if f"{station_number}.csv" in [x for x in os.listdir(file_dir)]:
            print('%s文件已下载' % (f"{station_number}.csv"))
        else:
            # 通过拼接的下载url下载文件,下载文件存储在目录tar_gz下
            with open(f'{file_dir}/{station_number}.csv', "wb") as code:
                code.write(r.content)
                print('下载文件%s成功' % (f"{station_number}.csv"))
