import matplotlib.pyplot as plt
import numpy as np

plt.show()

import os
import random

import matplotlib.pyplot as plt
import pandas as pd


def remove_lines_with_stop_char(file_path, stop_char):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    output_lines = []
    for line in lines:
        if stop_char in line:
            break
        output_lines.append(line)

    # 使用列表推导式过滤掉要移除的元素
    result = [x for x in lines if x not in output_lines]
    result[0] = result[0].replace("~A ", "")
    # print(result)

    result = ''.join(result)

    with open(file_path, 'w') as file:
        file.write(result)


def check_file_exist(save2file):
    dirname = os.path.dirname(save2file)
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)


def build_parameter_two(raw_las_file_path):
    with open(raw_las_file_path, 'r') as file:
        # 读取第一行
        first_line = file.readline()
        # 输出第一行内容
        # print(first_line)
        print("Data mismatch, proceed with further processing: ")
    stop_char = '~A Depth'
    if "Depth" not in first_line:
        remove_lines_with_stop_char(raw_las_file_path, stop_char)
    original_data = pd.read_csv(raw_las_file_path, delim_whitespace=True, header=0)

    # 移除无关列
    cols = [col for col in original_data.columns if 'Thickness' in col or 'Nom_Thick' in col]
    new_data = original_data[cols]

    new_data = pd.concat(
        [original_data['Depth'], new_data], axis=1)

    # 去除depth列
    # new_data = original_data.loc[:, original_data.columns != 'Depth']

    # 将数据量缩小 sampleFreq（10） 倍，方便计算
    sampleFreq = int(0.05 / 0.05)
    sampleFreq = int(1 / 0.05)
    new_data = new_data[::sampleFreq  # 切片操作中的第三个参数表示步长，即每隔 global_var.sampleFreq 行的数据。
               ].reset_index(
        drop=True)  # reset_index so that the sparsity don't affect the indices reset_index（）使得稀疏性不影响索引

    # 修改无用数据或站位数据
    new_data = new_data.replace(-999.25, np.nan)

    # original_data = original_data.to_numpy()
    return new_data


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
        # col = "Tubing_Nom_Thick"
        print(col)


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
                  ax=axes, use_index=True)
        color = color_map[(i % 4)]
        data.plot(x=thick_col + "B",
                  y='Depth', lw=0.8,
                  color=color,
                  label=thick_col + "B",
                  ax=axes, use_index=True)

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
        # data["Depth"]: y轴的数据, 填充的竖向基准。    # data[thick_col + "A"]: x轴的下限数据, 填充区域的左边界。
        # data[col]: x轴的上限数据, 填充区域的右边界。
        # alpha: 填充颜色的透明度, 0    完全透明, 1    完全不透明。
        # color: 填充的颜色。
        # plt.fill_betweenx(data["Depth"], data[col], data[thick_col + "A"], alpha=0.5, color=cmap(0.2))
        axes.fill_betweenx(data["Depth"], data[col], data[thick_col + "B"], alpha=1, color=fill_color)

    # 让matplotlib自动设置限制:
    # axes.autoscale(enable=True, axis='x', tight=True)

    # 在填充后设置x轴的范围:
    values_max = data[thick_col].max()
    values_min = data[thick_col].min()

    # axes.set_xlim([values_min, values_max + 1])



"""
画图相关
"""
# 设置了matplotlib的默认字体为微软雅黑。这样绘制的图形中的文字就会使用微软雅黑字体。
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
# 设置了解决matplotlib在显示中文时负号'-'显示为方块的问题。因为matplotlib默认会使用unicode编码,而很多中文字体不支持负号的unicode编码。这个设置将其关闭,就可以正常显示中文负号了。
plt.rcParams['axes.unicode_minus'] = False

# figsize 指定整个图片的大小表示图形 宽8 长5。figsize是预先定义的一个变量。
figsize = (5, 50)
# figsize = (16, 9)

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

two(axes[1], raw_las_file_path)

# plt.tight_layout(True)


save2file = f"./output/sparse_spike_inspect{random.randint(1, 100)}.png"
# save2file = ""

if save2file == "":
    plt.show()
else:
    check_file_exist(save2file)
    plt.savefig(save2file, bbox_inches='tight')

plt.close()
