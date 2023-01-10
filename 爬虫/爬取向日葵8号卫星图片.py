# -*- codeing = utf-8 -*-
# @Time :2023/1/10 16:30
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://github.com/CharlesPikachu/pytools/blob/master/pytools/modules/decryptbrowser/decryptbrowser.py
# @File :  爬取向日葵8号卫星图片.py

'''爬取壁纸'''
import datetime
import os

import requests


def crawlWallpaper(cache_dir='download'):
    if not os.path.isdir(cache_dir): os.mkdir(cache_dir)
    url_base = 'http://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/'
    date = datetime.datetime.utcnow().strftime('%Y/%m/%d/')
    # 卫星图更新到网站上是有时延的
    hour = str(int(datetime.datetime.utcnow().strftime('%H')) - 1).zfill(2)
    minute = str(datetime.datetime.utcnow().strftime('%M'))[0] + '0'
    second = '00'
    ext = '_0_0.png'
    picture_url = url_base + date + hour + minute + second + ext
    print(picture_url)
    res = requests.get(picture_url)
    with open(os.path.join(cache_dir, 'cache_wallpaper.png'), "wb") as code:
        # requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content来边下载边存硬盘
        for chunk in res.iter_content(chunk_size=1024):
            code.write(chunk)

crawlWallpaper()