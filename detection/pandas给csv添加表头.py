# -*- codeing = utf-8 -*-
# @Time :2023/7/6 10:54
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  pandas给csv添加表头.py

import pandas as pd

# 读取 CSV 文件
layer_path= r"C:\Users\12074\Desktop\Case-11_layer.csv"
df = pd.read_csv(layer_path, header=[0])
# 添加表头 df.columns 赋值一个列表，指定了表头的名称
df.columns = ['start', 'end', 'LayerODin1', 'LayerWtLbFt1', 'LayerODin2', 'LayerWtLbFt2', 'LayerODin3', 'LayerWtLbFt3']

# 将带有表头的 DataFrame 写入 CSV 文件 index=False 参数，避免写入索引列
df.to_csv('data_with_header.csv', index=False)

