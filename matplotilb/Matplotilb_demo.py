import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def check_file_exist(save2file):
    dirname = os.path.dirname(save2file)
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)


display_legend = True
title = "测试"
save2file = f"./output/sparse_spike_inspect.svg"
save2file =""

"""
    画图相关
    """
# 设置了matplotlib的默认字体为微软雅黑。这样绘制的图形中的文字就会使用微软雅黑字体。
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 设置了解决matplotlib在显示中文时负号'-'显示为方块的问题。因为matplotlib默认会使用unicode编码,而很多中文字体不支持负号的unicode编码。这个设置将其关闭,就可以正常显示中文负号了。
plt.rcParams['axes.unicode_minus'] = False
# 调整figure的dpi参数,增大图像分辨率:
# fig = plt.figure(dpi=300)
# 设置绘图用的图形库后端为矢量图形后端,如SVG:
# plt.switch_backend('SVG')


# figsize 指定整个图片的大小。figsize是预先定义的一个变量。
figsize = (10, 60)
# sharey=True 表示这些子图共享y轴。这样不同子图的y轴范围保持一致。
sharey = True
fig, axes = plt.subplots(1, 3, figsize=figsize, sharey=sharey)  # 使用subplot（）绘制左右3张子图,共享y轴范围
fig.suptitle(title)  # 用于为绘图的整个图表添加一个总标题。


def one(axes):
    lasPath = r"C:\Users\12074\Desktop\Test-1_las.csv"
    # delim_whitespace=True : 按照空格分割列,不使用逗号分隔
    raw_data = pd.read_csv(lasPath, header=0, index_col=False)
    axes[1].grid(True)  # grid 是否显示格子线条 网格
    axes[1].set_ylim([raw_data['Depth'].min(),
                      raw_data['Depth'].max()])  # 通过调用 set_ylim() 方法限制绘图中第一个子图（axes[1]）的 y 轴范围为 Depth' 列的最小值和最大值之间。
    axes[1].invert_yaxis()  # 翻转绘图中第一个子图（axes[1]）的 y 轴方向。使较大的值出现在顶部，较小的值出现在底部。

    def draw_half_graph(col_name_mask: list, on_axis: plt.Axes,
                        gold_spikes: pd.DataFrame = None,
                        spikes_indx: np.ndarray = None):
        """
        绘制左右图
        inner function to draw left and right graphs
        for reducing the code redundancy

        Parameters
        ----------
        col_name_mask : 需要绘制的列名称集合
        on_axis :  轴对象on_axis
        gold_spikes : 金属探针区间数据
        spikes_indx : 探测峰值索引
        """
        exclude_cols = ['Depth', '0']  # 排除的列
        for col_name in raw_data.iloc[:, ~raw_data.columns.isin(exclude_cols)]:
            # for col_name in raw_data.columns[col_name_mask]:
            raw_data.plot(x=col_name, y='Depth', lw=0.5,  # lw=0.5 设置线的宽度为 0.5。
                          label=col_name,  # label=col_name 设置曲线的标签为列名。
                          ax=on_axis,  # ax=on_axis 指定要在 on_axis 对象（plt.Axes 对象）上绘制图形。
                          legend=display_legend)  # legend=display_legend 控制是否显示图例，

    # 内管指标 在左边的图
    draw_half_graph(raw_data.columns, axes[1], None, None)





def two(axes):
    axes[2].grid(True)  # grid 是否显示格子线条
    axes[2].invert_yaxis()  # 翻转绘图中第一个子图（axes[1]）的 y 轴方向。使较大的值出现在顶部，较小的值出现在底部。

    layer_file_path = r"C:\Users\12074\Desktop\Case-11_layer.csv"
    layer_file = pd.read_csv(layer_file_path).to_numpy()
    x = layer_file.flatten()
    for index, item in enumerate(layer_file):
        # layer_start = item[0]
        layer_end = item[1]

    # axes[2].hist(x, n_bins, density=True, histtype='bar', stacked=True)
    # ax1.set_title('stacked bar')


# one(axes)
two(axes)

if save2file == "":
    plt.show()
else:
    check_file_exist(save2file)
    plt.savefig(save2file, bbox_inches='tight')

plt.close()
