# -*- codeing = utf-8 -*-
# @Time :2022/11/23 14:56
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  pandas获取起始日期的时间列表.py

# 设置下载时段（这里是UTC时刻）
import datetime

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 1, 3)
datelist = []
while start <= end:
    datelist.append(start)
    start += datetime.timedelta(days=1)
print(datelist)

print("-" * 20)

import pandas


def get_date_list(begin_date, end_date, freq):
    date_list = [x.strftime("%Y-%m-%d") for x in list(pandas.date_range(start=begin_date, end=end_date, freq=freq))]
    return date_list


# "D"代表间隔单位为天
date_list = get_date_list('20200101', '20201210', 'M')
print(type(date_list))
print(date_list)

print("-" * 20)

date_range = pandas.date_range('20200101', '20201210')
print(type(date_range))
print(date_range)

# @link：https://blog.csdn.net/weixin_42327752/article/details/121654538
