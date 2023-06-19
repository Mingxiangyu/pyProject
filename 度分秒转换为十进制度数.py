# -*- codeing = utf-8 -*-
# @Time :2023/4/21 15:27
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  度分秒转换为十进制度数.py

import re

def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'E' or direction == 'N':
        dd *= -1
    return dd

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]

def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms)
    lat = dms2dd(parts[0], parts[1], parts[2], parts[3])

    return (lat)

dd = parse_dms("36.77°N")
print(dd)

