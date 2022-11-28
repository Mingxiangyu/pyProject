# -*- codeing = utf-8 -*-
# @Time :2022/11/25 18:44
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载历史航迹数据.py
import calendar
import datetime
import hashlib
import os
import time

import requests
from fake_useragent import UserAgent
from flask import Flask


def get_file_md5_top10m(file_name):
    """
    根据前10兆计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_name, 'rb') as fobj:
        data = fobj.read(1024 * 1024 * 10)
        m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


def get_day_in_month(y, m):
    """
    获取指定月份的所有天数
    :param y: 年
    :param m: 月
    :return:
    """
    res = lambda year, month: list(
        range(1, 1 + time.localtime(time.mktime((year, month + 1, 1, 0, 0, 0, 0, 0, 0)) - 86400).tm_mday))
    return res(y, m)


SaveDir = "D:\RS_data\AIS"


class AisDownload(object):

    def __init__(self):
        # 11年前数据链接：https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2010/01_January_2010/Zone1_2010_01.zip
        #  11年数据链接： https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2011/01/Zone10_2011_01.gdb.zip
        # 15年前数据链接：https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2014/01/Zone1_2014_01.zip
        # 15年后数据链接：https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2015/AIS_2015_01_01.zip
        self.url = "https://coast.noaa.gov/htdata/CMSP/AISDataHandler/{}/{}"
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }

    # 请求网站获取url
    def download(self, url, out):
        # toDo 添加代理，更新反扒
        print("下载时url为：" + url)
        response = requests.get(url, headers=self.headers, timeout=60)
        with open(out, "wb") as code:
            # requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content来边下载边存硬盘
            for chunk in response.iter_content(chunk_size=1024):
                code.write(chunk)
            # code.write(response.content)

    def main(self, year, month):
        today = datetime.datetime.today()
        today_year = today.year
        url_suf_list = []
        if int(year) < 2009:
            # todo 结束，同时记录日志，提示数据不存在
            pass
        elif int(year) < 2011:
            # 11年前数据链接：https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2010/01_January_2010/Zone1_2010_01.zip
            zone_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
            for zone in zone_list:
                url_suf = "%s_%s_%s/Zone%s_%s_%s.zip" % (
                    month, calendar.month_name[int(month)], year, zone, year, month)
                url_suf_list.append(url_suf)
        elif int(year) < 2014:
            #  14年前数据链接： https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2011/01/Zone10_2011_01.gdb.zip
            zone_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
            for zone in zone_list:
                url_suf = "%s/Zone%s_%s_%s.gdb.zip" % (
                    month, zone, year, month)
                url_suf_list.append(url_suf)
        elif int(year) < 2015:
            # 15年前数据链接：https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2014/01/Zone1_2014_01.zip
            zone_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
            for zone in zone_list:
                url_suf = "%s/Zone%s_%s_%s.zip" % (
                    month, zone, year, month)
                url_suf_list.append(url_suf)
        elif int(year) > 2014:
            # 15年后数据链接：https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2015/AIS_2015_01_01.zip
            # day_list = get_day_in_month(int(year), int(month))
            # todo 可修改为获取当月所有数据
            day = 1
            # for day in day_list:
            if day < 10:
                day = "0%s" % day
            url_suf = "AIS_%s_%s_%s.zip" % (
                year, month, day)
            url_suf_list.append(url_suf)
        elif int(year) > int(today_year):
            # todo 结束，同时记录日志，提示数据不存在
            pass

        for url_suf in url_suf_list:
            url = self.url.format(year, url_suf)

            # 数据下载
            join = os.path.join(SaveDir, year, month)
            if not os.path.exists(join):
                os.makedirs(join)

            file_name = url.split('/')[-1]
            # SaveDir+"/"+year+"/"+month+"/"+file_name
            path = os.path.join(SaveDir, year, month, file_name)

            # 这一步判断本地是否存在该文件，如果不存在就下载，存在的话就跳过
            if not os.path.exists(path):
                print('downloading: ', path)
                self.download(url, path)
            else:
                # 如果存在，但是字节数为空，则重新下载 todo 如果字节数对应不上网站对数据的描述，是不是也可以重新下载
                if not os.path.getsize(path):
                    print('downloading: ', path)
                    self.download(url, path)
                else:
                    print('skipping: ', path)

            file_md5 = get_file_md5_top10m(path)
            print("数据md5为：" + file_md5)
            # data["id"] = file_md5


app = Flask(__name__)  # 创建flask实例

if __name__ == '__main__':
    spider = AisDownload()
    # year = "2015"
    year_list = [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
    for year in year_list:
        month = "1"
        if int(month) < 10:
            month = "0%s" % month
        spider.main(str(year), month)
