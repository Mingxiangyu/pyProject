# -*- codeing = utf-8 -*-
# @Time :2023/9/27 15:39
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  折线图.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data = pd.DataFrame(np.random.rand(1000, 2), columns=['A', 'B'])

# 转置DataFrame
# data = data.T

# 绘制折线图
data.plot(x=data.columns,kind='line')

plt.title('Line Plot')
# plt.xlabel('Index')
# plt.ylabel('Columns')

plt.show()