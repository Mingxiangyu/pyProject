# -*- codeing = utf-8 -*-
# @Time :2023/6/25 16:58
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  字典数组基于字典值来获取数组中最大字典和最小字典.py
# 定义字典数组
my_list = [
    {"name": "Alice", "age": 25, "score": 80},
    {"name": "Bob", "age": 30, "score": 90},
    {"name": "Charlie", "age": 35, "score": 85},
    {"name": "David", "age": 40, "score": 95}
]

# 基于 "score" 键获取最大字典和最小字典
max_dict = max(my_list, key=lambda x: x["age"])
min_dict = min(my_list, key=lambda x: x["age"])

print(max_dict)
print(min_dict)
