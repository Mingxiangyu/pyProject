# -*- codeing = utf-8 -*-
# @Time :2022/11/18 13:57
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://blog.csdn.net/qazwsxpy/article/details/127427409
# @link：https://blog.csdn.net/lilizhekou/article/details/123766062
# @File :  下载俄怀明的全球探空数据.py

import datetime
import os

from siphon.simplewebservice.wyoming import WyomingUpperAir  # 来自怀俄明大学的探空数据


# 新建文件夹函数，便于分站点存储数据
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
    else:
        pass


# 设置下载时段（这里是UTC时刻）
start = datetime.datetime(2020, 1, 1, 0)
end = datetime.datetime(2020, 1, 1, 0)
datelist = []
while start <= end:
    datelist.append(start)
    start += datetime.timedelta(hours=12)

datelist_s = []
# 选择下载站点
# 我国的探空站表格：http://data.cma.cn/article/showPDFFile.html?file=/pic/static/doc/B/B.0011.0001C/UPAR_CHN_MUL_STATION.pdf
stationlist = ['57494']

# 可通过外部文件批量导入站点编号
# sta = pd.read_csv("station.csv",encoding = 'gb2312',dtype={"id": str})
# stationlist = sta['id']


nodata = []
data_missing = []
# 批量下载
for station in stationlist:
    datelist_s = datelist.copy()
    for date in datelist_s:
        try:
            df = WyomingUpperAir.request_data(date, station)
            mkdir('D:/RS_data/' + station)
            file_path = 'D:/RS_data/' + station + '/' + station + '_' + date.strftime('%Y%m%d%H') + '.csv'
            df.to_csv(file_path, index=False)
            print(station + date.strftime('%Y%m%d_%H') + '下载成功', "路径为：" + file_path)
        except Exception as e:
            print('错误类型是', e.__class__.__name__)
            print('错误明细是', e)
            print(station + date.strftime('%Y%m%d_%H') + '下载失败,原因如下：')
            if e.__class__.__name__ == "IndexError":
                # 加入无数据队列
                print(
                    'No data available for {time:%Y-%m-%d %HZ} '
                    'for station {stid}.'.format(time=date, stid=station))
                nodata.append(station + '_' + date.strftime('%Y%m%d%H'))

            elif e.__class__.__name__ == "TypeError":
                print('Error data type in web page')
                nodata.append(station + '_' + date.strftime('%Y%m%d%H'))
            elif e.__class__.__name__ == "KeyError":
                print('Missing data in web page')
                data_missing.append(station + '_' + date.strftime('%Y%m%d%H'))
                # 其他需要忽略下载的错误可以继续往下加
            else:
                # 把下载失败日期加入到下载队列末端重新下载
                datelist_s.append((date))

# 将无数据的站点及日期写入文件
print("无数据提供的站点及日期：")
print(nodata)
f = open("nodata_12.txt", "w")
for line in nodata:
    f.write(line + '\n')
f.close()

# 将数据列缺失的站点及日期写入文件
print("数据列存在缺失的站点和日期：")
print(data_missing)
f = open("data_missing_12.txt", "w")
for line in data_missing:
    f.write(line + '\n')
f.close()

"""
 读取示例数据
 数据包含气压、高度、气温、露点、风向、风速、经向风速、纬向风速，还包含探空战观测时刻、经纬度和高程信息。
"""
import pandas as pd

df = pd.read_csv('D:/RS_data/57494/57494_2020010100.csv')
print(df)
