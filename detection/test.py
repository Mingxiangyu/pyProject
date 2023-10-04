import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)
y1 = x ** 2
y2 = x ** 1.5

# 创建图形
fig, ax = plt.subplots()

# 填充 y1 和 y2 之间的区域
ax.fill_between(x, y1, y2, alpha=0.5) 

# 设置标题等
ax.set_title('Area Plot')
ax.set_xlabel('X')
ax.set_ylabel('Y')

plt.show()