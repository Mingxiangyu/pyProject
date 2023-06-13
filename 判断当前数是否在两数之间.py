# -*- codeing = utf-8 -*-
# @Time :2023/6/5 16:36
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  判断当前数是否在两数之间.py
import math


def is_between(a, x, b):
    """
    判断 x 是否在 a 和 b 之间
    :param a: 小数
    :param x: 判断数
    :param b:  大数
    :return: true or false
    """
    if math.isnan(a):
        print("a不是数")
        a = 0
    if math.isnan(b):
        print("b不是数")
        b = 0
    return min(a, b) < x < max(a, b)
