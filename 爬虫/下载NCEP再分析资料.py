# -*- codeing = utf-8 -*-
# @Time :2022/11/18 17:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://blog.csdn.net/qazwsxpy/article/details/127427409
# 原文链接：https://www.heywhale.com/mw/project/5f3e0b4cce44c0002c8e0073
# @File :  下载NCEP再分析资料.py
"""
NCEP的FNL资料：http://rda.ucar.edu/data/ds083.2
空间分辨率：1°×1°
时间分辨率：逐6小时
"""
import datetime

import requests


# 定义登录函数
def builtSession():
    email = "xxxxxxx"  # 此处改为注册邮箱
    passwd = "xxxxxxxx"  # 此处为登陆密码
    loginurl = "https://rda.ucar.edu/cgi-bin/login"
    params = {"email": email, "password": passwd, "action": "login"}
    sess = requests.session()
    sess.post(loginurl, data=params)
    return sess


# 定义下载函数
def download(sess, dt):
    # grib1格式文件启用时间
    g1 = datetime.datetime(1999, 7, 30, 18)
    # grib2格式文件启用时间
    g2 = datetime.datetime(2007, 12, 6, 12)
    if dt >= g2:
        suffix = "grib2"
    elif dt >= g1 and dt < g2:
        suffix = "grib1"
    else:
        print("DateTime excess limit")
        # raise StandardError("DateTime excess limit")
    url = "http://rda.ucar.edu/data/ds083.2"
    folder = "{}/{}/{}.{:0>2d}".format(suffix, dt.year, dt.year, dt.month)
    filename = "fnl_{}.{}".format(dt.strftime('%Y%m%d_%H_00'), suffix)
    # 构建文件路径
    fullurl = "/".join([url, folder, filename])
    r = sess.get(fullurl)
    with open(filename, "wb") as fw:
        fw.write(r.content)
    print(filename + " downloaded")


# 批量下载
if __name__ == '__main__':
    print("downloading...")
    s = builtSession()
    for i in range(2):  # 共下载多少个时次
        startdt = datetime.datetime(2018, 5, 16, 0)  # 开始时次
        interval = datetime.timedelta(hours=i * 6)
        dt = startdt + interval
        download(s, dt)
    print("download completed!")
