import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors


def check_file_exist(save2file):
    dirname = os.path.dirname(save2file)
    if dirname != '':
        os.makedirs(dirname, exist_ok=True)


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


# 生成7000x80的随机数据
data = np.random.rand(7000, 10)


def build_parameter(raw_las_file_path):
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

    # 去除depth列
    original_data = original_data.loc[:, original_data.columns != 'Depth']

    # 将数据量缩小 sampleFreq（10） 倍，方便计算
    sampleFreq = int(0.05/ 0.05)
    sampleFreq = int(1/ 0.05)
    original_data = original_data[::sampleFreq  # 切片操作中的第三个参数表示步长，即每隔 global_var.sampleFreq 行的数据。
                    ].reset_index(
        drop=True)  # reset_index so that the sparsity don't affect the indices reset_index（）使得稀疏性不影响索引

    # 移除无关列
    cols = [col for col in original_data.columns if 'ADEC' in col]
    original_data = original_data[cols]

    # 修改无用数据或站位数据
    original_data = original_data.replace(-999.25, 0)

    # original_data = original_data.to_numpy()
    return original_data


raw_las_file_path = r"G:\软件备份\Project\测井\项目所需\Case-3文件及说明\Case-3_Result.las"
data = build_parameter(raw_las_file_path)

# 返回df的行数和列数
shape = data.shape
# 返回df的行数
row = data.shape[0]
# 返回df的列数
col = data.shape[1]

# 获取全部列最大、最小值:
# data_max = data.max()
# print(data_max)
# data_min = data.min()
# print(data_min)

# 获取整个DataFrame的最大最小值:
values_max = data.values.max()
values_min = data.values.min()

# fig, ax = plt.subplots(figsize=(5,50))
fig, ax = plt.subplots()

# 设置figure的dpi参数,增大像素密度进行缩放:
fig.set_dpi(1100)

# 使用tight_layout来自动调整子图和轴标签之间的空间:
# plt.tight_layout()

if row>10000:
    row = row/10
fig.set_size_inches(((row * 2 / fig.dpi)/25)/1, (row * 2 / fig.dpi)/1)

# grid 是否显示格子线条 网格
# ax.grid(True)


# 绘制热力图
# 创建自定义的颜色映射
# cmap = colors.LinearSegmentedColormap.from_list('red_purple', ['red', "orangered", "orange","yellow","yellowgreen","green","Cyan","skyblue",'purple'])
cmap = colors.LinearSegmentedColormap.from_list('red_purple', ['#FF4500', '#FFA500', '#FFFF00', '#ADFF2F', '#00FFFF', '#0000FF', '#A020F0'])
# from color import Color
# colors = list(Color('red').range_to(Color('purple'),7))
# cmap = plt.cm.get_cmap('RdBu', 128)

# im = ax.imshow(data,  cmap=cmap,interpolation='bilinear', aspect='auto')
im = ax.imshow(data,  cmap=cmap,interpolation='nearest', aspect='auto')
# 设置图像对象(im)的extent:
im.set_extent([0, 111, 0, 1111])

# 设置值范围为0-1映射整个颜色条
im.set_clim(0.6,1.4)

# 设置坐标轴范围
# ax.set_ylim(row/100, 0)
# ax.set_xlim(0, cos)

# 隐藏坐标轴
# ax.axis('off')

# 添加颜色条 # 设置颜色条的方向为横向:orientation='horizontal'
# fig.colorbar(im, orientation='horizontal')
# 获取颜色条
cbar = fig.colorbar(im, orientation='horizontal')

# 设置颜色条宽度与热力图相同
# cbar.ax.set_aspect(ax.get_aspect())

# 设置颜色条宽度为图的宽度
w = ax.get_position().width
cbar.ax.set_aspect(w)

"""
cbar.ax.set_position() 来设置颜色条的位置,它需要传入一个 [left, bottom, width, height] 的列表作为参数。
我们把 bottom 设置为0.8,使其接近顶部,width设为0.6纵跨图像的一部分。
"""
cbar.ax.set_position([0.207, ax.get_position().y1 + 0.01, w, 0.05])
# 直接设置颜色条的字体大小更大
cbar.ax.tick_params(labelsize=10)

save2file = f"./output/sparse_spike_inspect.svg"
save2file = ""

if save2file == "":
    plt.show()
else:
    check_file_exist(save2file)
    plt.savefig(save2file, bbox_inches='tight', format='svg')
