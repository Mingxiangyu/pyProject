# -*- codeing = utf-8 -*-
# @Time :2023/1/12 13:11
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://www.cnblogs.com/minseo/p/15745983.html
# @File :  下载NOAA全球开放气象数据.py
import os

import requests
from lxml import etree

tar_gz_url = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/'
# 定义请求头部信息
headers = {'User-Agent': 'M'}
# 发送请求
resp = requests.get(tar_gz_url, headers=headers)
tar_gz_resp_text = resp.text
# 根据返回的text创建etree对象才能使用xpath分析
tar_gz_etree_element = etree.HTML(tar_gz_resp_text)
tar_gz_url_xpath = tar_gz_etree_element.xpath('//*/table/tr/td/a')
# for i in tar_gz_url_xpath:
#     print(i.xpath('@href'))

for tar_gz in tar_gz_url_xpath[1:]:
    # 打印要下载的文件名
    file_name = tar_gz.xpath('@href')[0]

    if not "2022" in file_name:
        continue

    print(file_name)
    requests_url = tar_gz_url + file_name
    # 打印拼接以后的下载链接
    print(requests_url)
    # 通过下载链接创建对象r
    r = requests.get(requests_url)
    # 如果当前文件夹没有tar_gz目录则创建该目录
    if 'tar_gz' not in [x for x in os.listdir('..') if os.path.isdir(x)]:
        try:
            os.mkdir('tar_gz')
        except:
            print('创建文件夹失败')
    # 如果在目录tar_gz下已经有文件了则不重复下载,否则下载
    if file_name in [x for x in os.listdir('tar_gz')]:
        print('%s文件已下载' % (file_name))
    else:
        # 通过拼接的下载url下载文件,下载文件存储在目录tar_gz下
        with open(f'tar_gz/{file_name}', "wb") as code:
            code.write(r.content)
            print('下载文件%s成功' % (file_name))
