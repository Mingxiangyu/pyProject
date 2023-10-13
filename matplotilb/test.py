# -*- codeing = utf-8 -*-
# @Time :2023/10/5 17:21
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  test.py
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)

# 自定义颜色和区间
cmap = mcolors.ListedColormap(['purple', 'blue', 'green', 'yellow', 'red'])
norm = mcolors.BoundaryNorm([-1, -0.5, 0, 0.5, 1], cmap.N)

# 绘制图形并生成色条
cs = plt.fill(x, y, 'b')
cb = plt.colorbar(cs, ticks=[-1, -0.5, 0, 0.5, 1], cmap=cmap, norm=norm)

plt.show()