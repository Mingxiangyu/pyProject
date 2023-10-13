# -*- codeing = utf-8 -*-
# @Time :2023/10/11 10:52
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  求二维数组中第二维的最大元素量.py
dict_list = [
    {'layer_no': 1, 'pipe_type': 'Tubing', 'od': 7.0, 'weight': 26.0},
    {'layer_no': 2, 'pipe_type': 'Liner', 'od': 7.0, 'weight': 26.0},
    {'layer_no': 3, 'pipe_type': 'Casing1', 'od': 9.625, 'weight': 40.0},
]

# 定义要判断的字典
dict_to_check = {'od': 9.625, 'weight': 40.0}

# 方法1:使用 any 和生成器表达式
is_in = any(dict_to_check == d for d in dict_list)

# 方法2:使用 in 操作符
is_in = dict_to_check in dict_list

# 方法3:用字典键进行判断
keys = [tuple(d.keys()) for d in dict_list]
is_in = tuple(dict_to_check.keys()) in keys

# 方法4:自定义元素相等判断
def dict_equal(d1, d2):
    return d1['od'] == d2['od'] and d1['weight'] == d2['weight']

is_in = any(dict_equal(dict_to_check, d) for d in dict_list)

print(is_in) # True