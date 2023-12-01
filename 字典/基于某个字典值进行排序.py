# -*- codeing = utf-8 -*-
# @Time :2023/12/1 22:44
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  基于某个字典值进行排序.py
dicts = [
    {'name': 'a', 'value': 5},
    {'name': 'b', 'value': 3},
    {'name': 'c', 'value': 1}
]
"""
dicts 是一个字典的列表
在 sorted() 中,依然通过 key 参数指定一个 lambda 函数
lambda 函数中访问每个字典的'value' key 对应的值
这样就可以基于字典的值字段对整个列表进行排序
"""
sorted_dicts = sorted(dicts, key=lambda x: x['value'])

print(sorted_dicts)
