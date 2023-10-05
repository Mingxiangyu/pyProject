import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors


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


def build_parameter_three(pipe_info_file):
    # 管柱顺序判断逻辑就是 CASING-顺序号从大到小，Casing排完就是liner，然后就是tubing,tubing存在后面带序号的可能，如tubing2
    pipe_info = {}
    pipe_info_csv = pd.read_csv(pipe_info_file, skiprows=1)
    pipe_info_dict_list = pipe_info_csv.to_dict(orient='records')
    for pipe_info_dict in pipe_info_dict_list:
        pipe_item = {}
        type = pipe_info_dict.get("Type")
        start_dpt = pipe_info_dict.get("StartDpt")
        end_dpt = pipe_info_dict.get("EndDpt")
        start_end = {
            "start": start_dpt,
            "end": end_dpt
        }
        # 将当前 n_label 的起始值记录下
        pipe_info_type = pipe_info.get(type)
        if pipe_info_type:
            pipe_info[type].append(start_end)
        else:
            pipe_info[type] = []
            pipe_info[type].append(start_end)

    print(pipe_info)
    #  将value中所有存在多个尺寸的数据融合到一块，形成一根柱体数据
    result = {}
    for type, start_end in pipe_info.items():
        if len(start_end) > 1:
            start = min([d['start'] for d in start_end])
            end = max([d['end'] for d in start_end])
            result[type] = {'start': start, 'end': end}
        else:
            result[type] = start_end
    print(result)

    # 提取排序键
    keys = ['Tubing', 'Liner']
    casing_keys = [k for k in result.keys() if 'Casing' in k]
    casing_keys.sort()
    order = keys + casing_keys
    print(order)

    # 按 order 顺序排序字典
    result = dict(sorted(result.items(), key=lambda x: order.index(x[0])))

    # 实现 字典key 的反转（因为图标中顺序是这样的）
    keys = list(result.keys())  # 获得键列表
    keys.reverse()  # 倒序键列表
    reversed_d = dict()
    for key in keys:
        reversed_d[key] = result[key]

    print(reversed_d)

    column_depth = []
    bottoms = []
    for value in reversed_d.values():
        if isinstance(value, list):
            for d in value:
                column_depth.append(d['end'])
                bottoms.append(d['start'])
        elif isinstance(value, dict):
            column_depth.append(value['end'])
            bottoms.append(value['start'])

    return column_depth, bottoms


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
    sampleFreq = int(0.05 / 0.05)
    sampleFreq = int(1 / 0.05)
    original_data = original_data[::sampleFreq  # 切片操作中的第三个参数表示步长，即每隔 global_var.sampleFreq 行的数据。
                    ].reset_index(
        drop=True)  # reset_index so that the sparsity don't affect the indices reset_index（）使得稀疏性不影响索引

    # 移除无关列
    cols = [col for col in original_data.columns if 'LN' in col]
    original_data = original_data[cols]

    # 修改无用数据或站位数据
    original_data = original_data.replace(-999.25, np.nan)

    # original_data = original_data.to_numpy()
    return original_data


def one(axes, path):
    axes.invert_yaxis()

    data = build_parameter(path)

    # grid 是否显示格子线条 网格
    # ax.grid(True)

    # 绘制热力图
    # 创建自定义的颜色映射
    # cmap = colors.LinearSegmentedColormap.from_list('red_purple', ['red', "orangered", "orange","yellow","yellowgreen","green","Cyan","skyblue",'purple'])
    cmap = colors.LinearSegmentedColormap.from_list('red_purple',
                                                    ['#FF4500', '#FFA500', '#FFFF00', '#ADFF2F', '#00FFFF', '#0000FF',
                                                     '#A020F0'])

    # im = ax.imshow(data,  cmap=cmap,interpolation='bilinear', aspect='auto')
    im = axes.imshow(data, cmap=cmap, interpolation='nearest', aspect='auto')
    # im = axes.imshow(data, cmap=cmap, interpolation='nearest')

    # grid 是否显示格子线条 网格
    axes.grid(True)

    # 设置图像对象(im)的extent:表示设置此图像的:
    # x方向范围为0 - 111
    # y方向范围为0 - 1111
    # im.set_extent([0, 111, 0, 1111])

    # 隐藏坐标轴
    # axes.axis('off')

    """
    颜色条
    """
    # # 设置值范围为0-1映射整个颜色条
    im.set_clim(0.6, 1.4)

    # 获取颜色条
    # cbar = fig.colorbar(im, ax=axes, orientation='horizontal')
    #
    # # 设置颜色条宽度与热力图相同
    # cbar.ax.set_aspect(axes.get_aspect())
    #
    # # 设置颜色条宽度为图的宽度
    # w = axes.get_position().width
    # cbar.ax.set_aspect(w)
    #
    # """
    # cbar.ax.set_position() 来设置颜色条的位置,它需要传入一个 [left, bottom, width, height] 的列表作为参数。
    # 我们把 bottom 设置为0.8,使其接近顶部,width设为0.6纵跨图像的一部分。
    # """
    # cbar.ax.set_position([0.207, axes.get_position().y1 + 0.01, w, 0.05])
    # # 直接设置颜色条的字体大小更大
    # cbar.ax.tick_params(labelsize=10)


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


def three(axes, path):
    axes.invert_yaxis()

    column_depth, bottoms = build_parameter_three(path)

    # 镜像元组
    mirrored_tuple = column_depth[::-1]
    # 拼接两个元组
    column_depth += mirrored_tuple

    # bottoms 设置每个柱子的基准高度
    bottoms_tuple = bottoms[::-1]
    # 拼接两个元组
    bottoms += bottoms_tuple

    result = tuple()
    for i in range(len(column_depth)):
        result += (column_depth[i] - bottoms[i],)

    # create plot

    index = np.arange(len(column_depth))
    bar_width = 0.35
    rects1 = axes.bar(index, result, bar_width, color='gray',
                      bottom=bottoms,
                      label='Men')

    # 隐藏坐标轴
    # axes.axis('off')

    # grid 是否显示格子线条 网格
    axes.grid(True)

    axes.set_xticks(np.arange(len(column_depth)))
    axes.set_xticklabels(index)


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

three(axes[2], pipe_info_file)

# plt.tight_layout(True)


save2file = f"./output/sparse_spike_inspect{random.randint(1, 100)}.png"
# save2file = ""

if save2file == "":
    plt.show()
else:
    check_file_exist(save2file)
    plt.savefig(save2file, bbox_inches='tight')

plt.close()
