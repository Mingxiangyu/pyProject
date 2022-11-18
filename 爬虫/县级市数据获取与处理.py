# -*- codeing = utf-8 -*-
# @Time :2022/11/18 15:43
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://blog.csdn.net/qazwsxpy/article/details/127427409
# @File :  县级市数据获取与处理.py
import json
import re
import warnings

import pandas as pd
import requests

warnings.filterwarnings('ignore')


def get_feature_list(url):
    r = requests.get(url)
    data = json.loads(r.text)
    return data['features']


def get_data(city_data):
    df = []
    for city in city_data:
        city_code = city['properties']['adcode']
        city_name = city['properties']['name']
        lon, lat = city['properties']['center']
        df.append([city_code, city_name, lon, lat])
    df = pd.DataFrame(df, columns=['城市代码', '城市名称', '经度', '纬度'])
    return df


# 地级市
def get_city(number, filename='city'):
    data = get_feature_list('https://geo.datav.aliyun.com/areas/bound/geojson?code=' + str(number) + '_full')
    city_data = get_data(data)
    city_data.to_csv(filename + '.csv', encoding='gbk', index=False)
    print('数据下载完毕')


# 县级市
def get_county(number, filename='county'):
    data = get_feature_list('https://geo.datav.aliyun.com/areas/bound/geojson?code=' + str(number) + '_full')
    county = pd.DataFrame()
    pattern = '\d+'
    for city in data:
        city_code = city['properties']['adcode']
        url = re.sub(pattern, str(city_code),
                     'https://geo.datav.aliyun.com/areas/bound/geojson?code=' + str(number) + '_full')
        county_data = get_data(get_feature_list(url))
        county = pd.concat([county, county_data])
        print(city['properties']['name'] + '下所有区县保存完毕')
    county.to_csv(filename + '.csv', encoding='gbk', index=False)


# 获取河南省（adcode:410000）地级市数据
get_city(410000)

df = pd.read_csv('city.csv', encoding='gbk')
df

# 获取河南省（adcode:410000）县级市数据
get_county(410000)

df = pd.read_csv('county.csv', encoding='gbk')
df