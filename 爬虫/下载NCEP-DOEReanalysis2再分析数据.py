# -*- codeing = utf-8 -*-
# @Time :2022/11/23 12:17
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://www.heywhale.com/api/notebooks/62ea6d2ef145d47a93d25a5a/RenderedContent?cellcomment=1&cellbookmark=1#2.2-NCEP-DOE-Reanalysis-2-%E5%86%8D%E5%88%86%E6%9E%90%E6%95%B0%E6%8D%AE-by-Guo
# @File :  下载NCEP-DOEReanalysis2再分析数据.py
"""
数据下载：https://psl.noaa.gov/data/gridded/data.ncep.reanalysis2.html
空间分辨率：2.5°×2.5°
时间分辨率：逐6小时
时间尺度：1979/01/01 to 2020/07/31
"""

import urllib

import lxml.html
import requests


def dload_gfs(url, start, end, out_path=''):
    try:
        html = requests.get(url).text
    except Exception as e:
        print(e)
    else:
        doc = lxml.html.fromstring(html)
        results = doc.xpath('//a/@href')
        for link in results:
            # TODO 没有nc！！！！！待解决
            if '.nc' in link:
                time = int(link.split('.')[-2])
                print(link)
                if time >= start and time <= end:
                    print(f'downloading {link} ...')
                    try:
                        r = urllib.request.urlopen(link, timeout=30).read()
                    except Exception as e:
                        print(e)
                    else:
                        with open(out_path + link.split('/')[-1], "wb") as f:
                            f.write(r)


if __name__ == "__main__":
    url = 'https://psl.noaa.gov/cgi-bin/db_search/DBListFiles.pl?did=59&tid=81620&vid=4241'
    start = 1979
    end = 1981
    out_path = 'D:/RS_data'
    dload_gfs(url, start, end, out_path)
