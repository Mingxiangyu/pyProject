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

# 基于 "score" 键计算平均值
total_score = sum(d["score"] for d in my_list)
average_score = total_score / len(my_list)

print(average_score)

