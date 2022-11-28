# -*- codeing = utf-8 -*-
# @Time :2022/11/23 12:03
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载GFS&GDAS 数据最常用的气象预报数据.py
import hashlib
import json
import os

import requests
from fake_useragent import UserAgent

SaveDir = "D:\RS_data\GFS"


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


class gfsDownload(object):
    def __init__(self):
        # 下载请求链接
        # todo 如果需要，可以将“file=gfs.t{}z.pgrb2.{}.anl” 的.anl更换为循环，实现不同预测时间的细分文件
        # https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t06z.pgrb2.0p25.anl&var_UGRD=on&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%2Fgfs.20221122%2F06%2Fatmos
        self.url = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_{}.pl?file=gfs.t{}z.pgrb2.{}.anl&{}&{}&subregion=&leftlon={}3&rightlon={}&toplat={}&bottomlat={}&dir=%2Fgfs.{}%2F{}%2Fatmos"
        self.file_name = "gfs.t{}z.pgrb2.{}.anl"
        # 产生随机的User - Agent请求头进行访问
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 30):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }

    # 请求网站获取url
    def download(self, url, out):
        # toDo 添加代理，更新反扒
        print("下载时url为：" + url)
        response = requests.get(url, headers=self.headers)
        with open(out, "wb") as code:
            # requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content来边下载边存硬盘
            for chunk in response.iter_content(chunk_size=1024):
                code.write(chunk)
            # code.write(response.content)

    def main(self, res, gfs_time, level, var, gfs_date, left_lon, right_lon, top_lat, bottom_lat):
        for gfs_time in [0, 6, 12, 18]:  # 表示数据发布的时间分别是00,06,12,18 todo 待确定是用户选择还是默认全采集
            if gfs_time < 10:
                gfs_time = "0%d" % gfs_time
            elif gfs_time < 100:
                gfs_time = "%d" % gfs_time
            else:
                gfs_time = str(gfs_time)
            url = self.url.format(res, gfs_time, res, level, var, left_lon, right_lon, top_lat, bottom_lat, gfs_date,
                                  gfs_time)
            print("start download html:{}".format(url))

            # 构建业务数据
            data = {
                # todo 添加数据来源、文件指纹
                "res": res,
                "gfs_time": gfs_time,
                "level": level,
                "var": var,
                "gfs_date": gfs_date,
                "left_lon": left_lon,
                "right_lon": right_lon,
                "top_lat": top_lat,
                "bottom_lat": bottom_lat
            }

            # 数据下载
            if not os.path.exists(SaveDir):
                os.makedirs(SaveDir)
            file_name = self.file_name.format(gfs_time, res)
            path = os.path.join(SaveDir, file_name)

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
            data["id"] = file_md5

            data_json = json.dumps(data)

            with open(SaveDir + "/" + "md5" + ".modisjson", "wb") as f:
                # 写文件用bytes而不是str，所以要转码
                f.write(bytes(data_json, "utf-8"))


if __name__ == '__main__':
    spider = gfsDownload()
    res = "0p25"  # 0p25, 0p50 or 1p00 精度，每0.25度（经纬度）一个点
    gfs_time = "00"  # 00, 06, 12, 18
    level = "all_lev=on"
    var = "all_var=on"  # 气象因子选择
    gfs_date = "20221122"
    # leftlon=0&rightlon=360&toplat=90&bottomlat=-90
    left_lon = "0"
    right_lon = "360"
    top_lat = "90"
    bottom_lat = "-90"
    spider.main(res, gfs_time, level, var, gfs_date, left_lon, right_lon, top_lat, bottom_lat)
