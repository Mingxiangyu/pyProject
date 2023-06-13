# -*- codeing = utf-8 -*-
# @Time :2023/5/28 20:27
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://cloud.tencent.com/developer/article/1856554
# @Link : https://blog.csdn.net/qq_25888559/article/details/123936983
# @File :  pandas读取CSV.py


import pandas as pd

df = pd.read_csv('E:\WorkSpace\pyWorkSpace\pyProject\detection\Case-3_Edited_Raw_las.csv', encoding='utf-8')
# df.index获取了df的行索引，并将其存储为变量index_num。
index_num = df.index
print(index_num)

print(df.columns)


def getAverage(col_name):
    # 取指定某列，直接输入表头
    ad_ = df[col_name]
    # 使用mean函数计算score列的平均值
    average = ad_.mean()
    # 输出平均值
    print("score列的平均值为:", average)
    return average


n均 = getAverage("AD[17]")


def 获取行索引列索引(col_name, cell_value):
    # 找到score列中值为85的元素
    row_index = df.index[df[col_name] == cell_value].tolist()[0]
    col_index = df.columns.get_loc(col_name)
    # 输出行索引和列索引
    print("值为", col_name, "的元素在第", row_index + 1, "行，第", col_index + 1, "列")


获取行索引列索引("Depth",4.0667)
