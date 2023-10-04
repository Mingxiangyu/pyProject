# -*- codeing = utf-8 -*-
# @Time :2023/9/11 22:38
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  tset.py
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches

n_groups = 5
means_men = (20, 35, 30, 35, 27)

# create plot
fig, ax = plt.subplots()
index = np.arange(n_groups)
bar_width = 0.35
# bottoms 设置每个柱子的基准高度
bottoms = [0, 2, 5, 10,20]
rects1 = ax.bar(index, means_men, bar_width, color='b', bottom=bottoms,label='Men')

# Set the y limits
ax.set_ylim(0, 40)
ax.invert_yaxis()
# Create the intervals
intervals = [(0, 10), (10, 20), (20, 30), (30, 40)]
# plt.show()

# Fill colors for each interval
colors = ['g', 'g', 'y', 'r']

for rect, interval in zip(rects1, intervals):
    x = rect.get_x()
    y0, y1 = interval

    poly = patches.Polygon([[x, y1],
                            [x, y0],
                            [x + rect.get_width(), y0],
                            [x + rect.get_width(), y1]],
                           facecolor=colors[intervals.index(interval)],
                           zorder=1)

    ax.add_patch(poly)

plt.show()