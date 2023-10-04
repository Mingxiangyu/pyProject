# -*- codeing = utf-8 -*-
# @Time :2023/9/11 22:38
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  tset.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import patches


def find_nearest(point):
    """
    将depth转换为深度行索引
    :rtype: 深度行索引
    """
    if point < las_file[0][1]:
        return 0
    elif point > las_file[-1][1]:
        return len(las_file) - 1
    else:
        for index, las_row in enumerate(las_file):
            if abs(las_row[1] - point) <= 0.05 / 2 + 1e-6:
                break
        return index


# layer_file_name = r"E:\WorkSpace\DetectionWorkSpace\DetectionDemo\test_layer\Test-1_layer.csv"
# las_file_name = r"E:\WorkSpace\DetectionWorkSpace\DetectionDemo\test_data_washed\Test-1_las.csv"
#
# las_file_raw = pd.read_csv(las_file_name, header=0)
# las_file = las_file_raw.to_numpy()
#
# layer_file = pd.read_csv(layer_file_name).to_numpy()
#
# layer_file = layer_file
# for index, item in enumerate(layer_file):
#     layer_start = item[0]
#     layer_end = item[1]
#     las_start = find_nearest(layer_start)
#     las_end = find_nearest(layer_end)
#     print(las_start,las_end)



def build_parameter_two(pipe_info_file):
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
    keys = ['Tubing','Liner' ]
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

    return column_depth,bottoms

pipe_info_file = r"E:\WorkSpace\DetectionWorkSpace\DetectionDemo\ReportGeneration\test_file\Pipe Inofrmation.csv"
column_depth,bottoms = build_parameter_two(pipe_info_file)

# 镜像元组
mirrored_tuple = column_depth[::-1]
# 拼接两个元组
column_depth += mirrored_tuple

# bottoms 设置每个柱子的基准高度
bottoms_tuple = bottoms[::-1]
# 拼接两个元组
bottoms += bottoms_tuple

# create plot
fig, ax = plt.subplots(figsize=(10, 60))

index = np.arange(len(column_depth))
bar_width = 0.35
rects1 = ax.bar(index, column_depth, bar_width, color='gray',
                bottom=bottoms,
                label='Men')

#  修改为获取depth
ax.set_ylim(0, 6942)
ax.invert_yaxis()

ax.set_xticks(np.arange(len(column_depth)))
ax.set_xticklabels(index)

# ax.grid(alpha=0.3)  # grid 是否显示格子线条
ax.grid(which='minor', axis='x', linewidth=0.5)
# Create the intervals
intervals = [(0, 1000), (800, 950), (2000, 2500), (3600, 3800)]
# plt.show()

# Fill colors for each interval
colors = ['g', 'g', 'y', 'r', "r"]

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

    poly = patches.Polygon([[x, y1 + 600],
                            [x, y0 + 600],
                            [x + rect.get_width(), y0 + 600],
                            [x + rect.get_width(), y1 + 600]],
                           facecolor=colors[intervals.index(interval)],
                           zorder=1)

    ax.add_patch(poly)

plt.show()
