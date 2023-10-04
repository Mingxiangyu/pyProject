# -*- codeing = utf-8 -*-
# @Time :2022/7/17 18:42
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  test.py
# Base64 Encoder - encodes a folder of PNG files and creates a .py file with definitions
import matplotlib.pyplot as plt
import numpy as np

N = 5
menMeans = (20, 35, 30, 35, 27)
womenMeans = (25, 32, 34, 20, 25)

ind = np.arange(N)    # the x locations for the groups
width = 0.35       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, menMeans, width, color='blue', label='Men')
rects2 = ax.bar(ind + width/2, womenMeans, width, color='pink', label='Women')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Scores by group and gender')
ax.set_xticks(ind)
ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)

# Create the fill colors
colors=['#1f77b4', '#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']

# Fill in the areas under the plot curves
for i in range(len(ind)):
    x1,x2=ind[i]-0.2,ind[i]+0.2
    y1=0
    plt.fill_between([x1,x2],[y1,y1],facecolor=colors[i],alpha=0.3)

plt.show()