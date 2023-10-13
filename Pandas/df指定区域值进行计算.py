# -*- codeing = utf-8 -*-
# @Time :2023/10/6 14:42
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  tesat.py
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3, 4, 5],
                   'B': [10, 20, 30, 40, 50],
                   'C': [100, 200, 300, 400, 500]})

# 新建个DataFrame来存放结果
df_new = pd.DataFrame()

for col in df.columns:
    mean = df.loc[1:2, col].mean()
    df.loc[1:2, col] = df.loc[1:2, col] * mean
    df_new[col] = df[col]

print(df_new)