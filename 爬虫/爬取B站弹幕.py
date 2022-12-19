# -*- codeing = utf-8 -*-
# @Time :2022/12/19 17:35
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  爬取B站弹幕.py
# -*-coding:utf-8 -*-
# Website: https://cuijiahua.com
# Author: Jack Cui
# Date: 2020.07.22
# import xml2ass
import time
from contextlib import closing

import requests

filename = '自制夫妻分分合合床'
danmu_name = filename + '.xml'
danmu_ass = filename + '.ass'
download_url = 'https://upos-sz-mirrorhw.bilivideo.com/upgcxcode/73/93/213419373/213419373-1-208.mp4?e=ig8euxZM2rNcNbh3hzdVhwdlhz4zhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1595414435&gen=playurl&os=hwbv&oi=837395164&trid=e936c792a83d4305b722c6a81a40c2f5T&platform=html5&upsig=f60cec742f9f6d3d9bbbf2b3d7cb3db3&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=580104086&orderid=0,1&logo=80000000'
oid = download_url.split('/')[6]
danmu_url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(oid)
print(danmu_url)
sess = requests.Session()
danmu_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9'}
with closing(sess.get(danmu_url, headers=danmu_header, stream=True, verify=False)) as response:
    if response.status_code == 200:
        with open(danmu_name, 'wb') as file:
            for data in response.iter_content():
                file.write(data)
                file.flush()
    else:
        print('链接异常')
time.sleep(0.5)
# xml转为ass文件
# xml2ass.Danmaku2ASS(danmu_name, danmu_ass, 1280, 720)
