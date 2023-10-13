import random

import matplotlib.pyplot as plt
import numpy as np


def one(axes, path):

    """
    颜色条
    """
    # # 设置值范围为0-1映射整个颜色条
    # axes.set_clim(0.6, 1.4)

    # 获取颜色条
    cbar = fig.colorbar( ax=axes, orientation='horizontal')

    # 设置颜色条宽度与热力图相同
    cbar.ax.set_aspect(axes.get_aspect())

    # 设置颜色条宽度为图的宽度
    w = axes.get_position().width
    cbar.ax.set_aspect(w)

    """
    cbar.ax.set_position() 来设置颜色条的位置,它需要传入一个 [left, bottom, width, height] 的列表作为参数。
    我们把 bottom 设置为0.8,使其接近顶部,width设为0.6纵跨图像的一部分。
    """
    cbar.ax.set_position([0.207, axes.get_position().y1 + 0.01, w, 0.05])
    # 直接设置颜色条的字体大小更大
    cbar.ax.tick_params(labelsize=10)


def two(axes, path):
    axes.invert_yaxis()

    # grid 是否显示格子线条 网格
    axes.grid()

    # 隐藏坐标轴
    # axes.axis('off')

    data = build_parameter_two(path)
    nom_cols = data.filter(like='Nom_Thick').columns

    color_map = ['r', 'g', 'b', 'y']
    for i, col in enumerate(nom_cols):
        thick_col = col.replace('Nom_Thick', 'Thickness')
        # 取上部分数据
        # data[thick_col + "A"] = np.where(data[thick_col] > data[col], data[thick_col], np.nan)
        # 取下部分数据
        data[thick_col + "B"] = np.where(data[thick_col] <= data[col], data[thick_col], np.nan)

        # 绘制基准线
        data.plot(x=col,
                  y='Depth', lw=1,
                  color="black",
                  label=col,
                  legend=False,
                  ax=axes, use_index=True)
        color = color_map[(i % 4)]
        data.plot(x=thick_col + "B",
                  y='Depth', lw=0.8,
                  color=color,
                  label=thick_col + "B",
                  legend=False,
                  ax=axes, use_index=True)

        #  指定颜色
        # 1 - Tubing为深绿色(单柱)
        # 2 - TubingS为墨绿色(单柱)，为橘红色(双柱)
        # 4 - Casing1为深蓝色(双柱)，5 - Casing2为浅蓝色(双柱)，6 - Casing3为深黄色(双柱)，7 - Casing4为土黄色(双柱)
        # 8 - Casing5为紫色(双柱)，9 - Casing6为深灰色(双柱)
        fill_color = None
        if "Tubing" in col:
            fill_color = "g"
        elif "Liner" in col:
            fill_color = "tab:orange"
        elif "Casing" in col:
            if "1" in col:
                fill_color = "b"
            elif "2" in col:
                fill_color = "tab:blue"
            elif "3" in col:
                fill_color = "yellow"
            elif "4" in col:
                fill_color = "darkkhaki"
            elif "5" in col:
                fill_color = "purple"
            elif "6" in col:
                fill_color = "gray"
        # data["Depth"]: y轴的数据, 填充的竖向基准。    # data[thick_col + "A"]: x轴的下限数据, 填充区域的左边界。
        # data[col]: x轴的上限数据, 填充区域的右边界。
        # alpha: 填充颜色的透明度, 0    完全透明, 1    完全不透明。
        # color: 填充的颜色。
        # plt.fill_betweenx(data["Depth"], data[col], data[thick_col + "A"], alpha=0.5, color=cmap(0.2))
        axes.fill_betweenx(data["Depth"], data[col], data[thick_col + "B"], alpha=1, color=fill_color)




"""
画图相关
"""
# 设置了matplotlib的默认字体为微软雅黑。这样绘制的图形中的文字就会使用微软雅黑字体。
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 设置了解决matplotlib在显示中文时负号'-'显示为方块的问题。因为matplotlib默认会使用unicode编码,而很多中文字体不支持负号的unicode编码。这个设置将其关闭,就可以正常显示中文负号了。
plt.rcParams['axes.unicode_minus'] = False

# toDo 基于设置指定比例
# figsize 指定整个图片的大小表示图形 宽8 长5。figsize是预先定义的一个变量。
# figsize = (5, 50)
# figsize = (16, 9)
figsize=None

# sharey=True 表示这些子图共享y轴。这样不同子图的y轴范围保持一致。
# constrained_layout 会自动调整子图和装饰，使其尽可能地适合图中。
# 必须在创建子图之前或期间激活 constrained_layout，因为它会在每个绘制步骤之前优化布局。
fig, axes = plt.subplots(1, 3, figsize=figsize, sharey=True, constrained_layout=True)  # 使用subplot（）绘制左右3张子图,共享y轴范围
# fig, axes = plt.subplots(1, 3, figsize=figsize, sharey=True)  # 使用subplot（）绘制左右3张子图,共享y轴范围
# fig, axes = plt.subplots(1, 3, figsize=figsize)  # 使用subplot（）绘制左右3张子图,共享y轴范围
# fig.suptitle("test")  # 用于为绘图的整个图表添加一个总标题。

# 设置figure的dpi参数,增大像素密度进行缩放:
fig.set_dpi(800)

raw_las_file_path = r"G:\软件备份\Project\测井\项目所需\Test-1_input&output\Result Package\Test-1_Processed Data_LAS.las"
raw_las_file_path = r"G:\软件备份\Project\测井\项目所需\Test-1_input&output\Result Package\Test-1_Processed Data_LAS.las"
pipe_info_file = r"G:\软件备份\Project\测井\项目所需\Test-1_input&output\Input Package\Test-1_Pipe Inofrmation.csv"

one(axes[0], raw_las_file_path)

two(axes[1], raw_las_file_path)


# plt.tight_layout(True)


save2file = f"./output/sparse_spike_inspect{random.randint(1, 100)}.png"
# save2file = ""

if save2file == "":
    plt.show()
else:
    plt.savefig(save2file, bbox_inches='tight')

plt.close()
