# -*- codeing = utf-8 -*-
# @Time :2023/6/25 16:53
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  递归获取这个字典中所有value.py

def flatten_value(dic):
    """
    递归获取这个字典中所有value（包含子字典）
    :param dic:
    :return:
    """
    result = []
    for value in dic.values():
        if isinstance(value, dict):
            result.extend(flatten_value(value))
        elif isinstance(value, list):
            for elem in value:
                result.extend(flatten_value(elem))
        else:
            result.append(value)
    return result


def flatten_key(dic):
    """
    递归获取这个字典中所有key（包含子字典）
    :param dic:
    :return:
    """
    result = []
    for key in dic.keys():
        value = dic[key]
        if isinstance(value, dict):
            result.extend(flatten_key(value))
        elif isinstance(value, list):
            for elem in value:
                result.extend(flatten_key(elem))
        else:
            result.append(key)
    return result

