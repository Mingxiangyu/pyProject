#!/usr/bin/python
import time
from datetime import datetime


# 方法一： 利用库函数
def ret_day_1(year, month, day):
    d = datetime(year=year, month=month, day=day)
    return d.timetuple().tm_yday


# 方法二：利用时间戳差值
def ret_day_2(year, month, day):
    s_date = f"{year-1}-12-31"
    c_date = f"{year}-{month}-{day}"
    st = int(time.mktime(datetime.strptime(s_date, "%Y-%m-%d").timetuple()))
    ct = int(time.mktime(datetime.strptime(c_date, "%Y-%m-%d").timetuple()))
    duration = ct - st
    return int(duration / 60 / 60 / 24)


# 方法三：利用闰年计算公式
def ret_day_3(year, month, day):
    m_day = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        # 闰年二月29天，全年366天
        m_day[2] = 29
    days = 0
    for i in range(month):
        days += m_day[i]
    days += day
    return days


r1 = ret_day_1(2022, 6, 30)
r2 = ret_day_2(2022, 6, 30)
r3 = ret_day_3(2022, 6, 30)
print(r1, r2, r3)