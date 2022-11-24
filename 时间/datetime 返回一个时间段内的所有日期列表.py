# -*- codeing = utf-8 -*-
# @Time :2022/11/23 15:39
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  datetime 返回一个时间段内的所有日期列表.py
import datetime


def daterange(begin, end):
    dates = []
    dt = datetime.datetime.strptime(begin, '%Y-%m-%d')
    dt_end = datetime.datetime.strptime(end, '%Y-%m-%d')
    # date=begin
    while dt <= dt_end:
        t = datetime.datetime.strftime(dt, '%Y-%m-%d')
        dates.append(t)
        dt += datetime.timedelta(1)
        # date=dt.strftime('Y%-m%-d%')
    return dates


ll = daterange('2021-12-23', '2022-09-30')
print(len(ll))
print(ll[:10], ll[-10:])
