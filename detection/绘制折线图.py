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
    new_data = new_data.replace(-999.25, 0)

    # original_data = original_data.to_numpy()
    return new_data


def two(axes, path):
    axes.invert_yaxis()

    data = build_parameter_two(path)

    # 可以试试在plot之前清空子图的图例:
    axes.legend_ = None

    # contains = data.columns.str.contains('ADEC')
    color_map = ['r', 'g', 'b', 'y']
    for i, col_name in enumerate(list(data.columns)):
        if col_name == "Depth":
            continue
        color = color_map[(i % 4)]
        data.plot(x=col_name,
                  y='Depth',
                  lw=0.5,  # lw=0.5 设置线的宽度为 0.5。
                  color=color,  # matplotlib 的颜色映射colormap来获取不同的颜色
                  label=None,  # label=col_name 设置曲线的标签为列名。
                  ax=axes,  # ax=on_axis 指定要在 on_axis 对象（plt.Axes 对象）上绘制图形。
                  use_index=True,  # 加上 use_index=True,这会强制使用原始的索引值(这里是 Depth)作为 y 值,而不是重新设置 y 轴范围。
                  # legend=True,
                  legend=False,
                  )  # legend  控制是否显示图例，

    # grid 是否显示格子线条 网格
    axes.grid(True)

    """
    图例
    """
    lines = axes.get_lines()
    labels = [line.get_label() for line in lines]
    # 给labels去重，避免图例项重复
    labels = list(set(labels))

    def get_index(col):
        if "[" not in col:
            return 0
        return int(col.split('[')[1].split(']')[0])

    # 排序，避免顺序换乱
    labels = sorted(labels, key=get_index)

    # 调用 legend() 方法,并指定参数 loc='upper center',bbox_to_anchor=(0.5, 1.15)。这可以把图例放在中心上方,并稍微抬高一些:
    #  fontsize=12 设置图例的字体大小:    # 调整图例的边框:, borderaxespad=0.
    # 去掉图例的边框线:edgecolor='none'  #ncol=3: 将图例分为3列显示
    # 如果不需要边框, 可以设置:frameon=False
    # axes.legend(lines, labels, loc='upper center',
    #             bbox_to_anchor=(0.5, 1.05),
    #             fontsize=3,
    #             frameon=True, borderaxespad=1., ncol=2,
    #             edgecolor='none'
    #             )


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
