# -*- codeing = utf-8 -*-
# @Time :2022/11/26 19:11
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  获取指定月份的所有天数.py
import time


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


# 如果超过12会换到下一年
l = get_day_in_month(2022, 14)
print(l)
