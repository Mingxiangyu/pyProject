import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# matplotlib中fil_between和fill_betweenx的用法 https://blog.csdn.net/weixin_43776305/article/details/121524002
data = pd.DataFrame(np.random.uniform(-1, 1, size=(1000, 4)), columns=['A', 'B', "C", "D"])
data[['B' ]] = 0
data[[ 'D']] = 1

# 分割A列为两部分
data['A1'] = np.where(data['A'] > data['B'], data['A'], np.nan)
data['A2'] = np.where(data['A'] <= data['B'], data['A'], np.nan)

# 分割C列
data['C1'] = np.where(data['C'] > data['D'], data['C'], np.nan)
data['C2'] = np.where(data['C'] <= data['D'], data['C'], np.nan)

# 填充面积图
plt.fill_between(data.index, data['A1'], alpha=0.5, color='blue')
# 使用颜色映射Colormap:
cmap = plt.get_cmap('jet')
plt.fill_between(data.index, data['A2'], alpha=0.5, color=cmap(0.5))
plt.fill_between(data.index, data['C1'], alpha=0.5, color='blue')
# 设置边框轮廓颜色: edgecolor='purple'
plt.fill_between(data.index, data['C2'], alpha=0.5, edgecolor='purple')


plt.plot(data['B'], 'r')
# plt.plot(data['D'], 'r-')

plt.show()