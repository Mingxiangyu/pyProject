# -*- codeing = utf-8 -*-
# @Time :2023/9/18 10:58
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://dev.to/oscarleo/how-to-create-a-beautiful-polar-histogram-with-python-and-matplotlib-400l
# @File :  环状直方图.py
import math

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from PIL import Image
from matplotlib.lines import Line2D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import Wedge


def add_legend(labels, colors, title):
    """
    添加图例
    观看者无法理解颜色的含义，但我们可以通过添加图例来解决这个问题。

为了添加图例，我创建了以下函数，该函数接受要添加的标签、它们的颜色和标题。
    :param labels:
    :param colors:
    :param title:
    """
    lines = [
        Line2D([], [], marker='o', markersize=24, linewidth=0, color=c)
        for c in colors
    ]

    plt.legend(
        lines, labels,
        fontsize=18, loc="upper left",
        # alignment="left",
        borderpad=1.3, edgecolor="#E4C9C9", labelspacing=1,
        facecolor="#F1E4E4", framealpha=1, borderaxespad=1,
        title=title, title_fontsize=20,
    )


def get_xy_with_padding(length, angle, padding):
    """
    定义职位
当您向 Matplotlib 中的图表添加标志和文本时，您需要计算正确的位置。

这通常很棘手，尤其是当您具有像极坐标直方图中这样的不寻常形状时。

下面的函数采用楔子的长度及其角度来计算位置。填充将位置推离栏以增加一些视觉空间。
    :param length:
    :param angle:
    :param padding:
    :return:
    """
    x = math.cos(math.radians(angle)) * (length + padding)
    y = math.sin(math.radians(angle)) * (length + padding)
    return x, y


def draw_wedge(ax, start_angle, end_angle, length, bar_length, color):
    """
该函数根据角度、长度、条形长度和颜色绘制楔形。
    :type length: object
    """
    ax.add_artist(
        Wedge((0, 0),
              length, start_angle, end_angle,
              color=color, width=bar_length
              )
    )


def add_text(ax, x, y, country, score, angle):
    """
    与标志一样，如果角度超过 270 度，我会更改旋转。否则，文字就会颠倒。
    :param ax:
    :param x:
    :param y:
    :param country:
    :param score:
    :param angle:
    """
    if angle < 270:
        text = "{} ({})".format(country, score)
        ax.text(x, y, text, fontsize=13, rotation=angle - 180, ha="right", va="center", rotation_mode="anchor")
    else:
        text = "({}) {}".format(score, country)
        ax.text(x, y, text, fontsize=13, rotation=angle, ha="left", va="center", rotation_mode="anchor")


def add_flag(ax, x, y, name, zoom, rotation):
    """
    添加标志
对于标志，我使用 FlatIcon 中的这些圆形标志。

它们需要许可证，因此，不幸的是，我无法共享它们，但您可以在其他地方找到类似的标志。

这是我向图表添加标志的函数。它采用位置、国家/地区名称（对应于正确文件的名称）、缩放和旋转。
    :param ax:
    :param x:
    :param y:
    :param name:
    :param zoom:
    :param rotation:
    """
    flag = Image.open("<location>/{}.png".format(name.lower()))
    flag = flag.rotate(rotation if rotation > 270 else rotation - 180)
    im = OffsetImage(flag, zoom=zoom, interpolation="lanczos", resample=True, visible=True)

    ax.add_artist(AnnotationBbox(
        im, (x, y), frameon=False,
        xycoords="data",
    ))


def color(income_group):
    """
添加颜色
接下来，我有一个简单的颜色函数，可以根据该国家/地区的收入水平决定每个楔形的颜色。
    :param income_group:
    :return:
    """
    if income_group == "High income":
        return "#468FA8"
    elif income_group == "Lower middle income":
        return "#E5625E"
    elif income_group == "Upper middle income":
        return "#62466B"
    elif income_group == "Low income":
        return "#6B0F1A"
    else:
        return "#909090"


def draw_reference_line(ax, point, size, padding, fontsize=18):
    """
    绘制参考线
参考线是一种优秀的视觉助手。它们在这里与标准条形图一样有效。

这个想法是在特定分数上画一条线，这间接帮助我们比较不同的国家。

这是我绘制参考线的函数。我正在重用该draw_wedge()函数来绘制 0 到 360 度的楔形。
    :param ax:
    :param point:
    :param size:
    :param padding:
    :param fontsize:
    """
    draw_wedge(ax, 0, 360, point + padding + size / 2, size, background_color)
    ax.text(-0.6, padding + point, point, va="center", rotation=1, fontsize=fontsize)


df = pd.read_csv("./hapiness_report_2022.csv", index_col=None)
df = df.sort_values("score").reset_index(drop=True)

font_family = "PT Mono"
background_color = "#F8F1F1"
text_color = "#040303"

sns.set_style({
    "axes.facecolor": background_color,
    "figure.facecolor": background_color,
    "font.family": font_family,
    "text.color": text_color,
})

START_ANGLE = 100  # At what angle to start drawing the first wedge
END_ANGLE = 450  # At what angle to finish drawing the last wedge
SIZE = (END_ANGLE - START_ANGLE) / len(df)  # The size of each wedge
PAD = 0.2 * SIZE  # The padding between wedges

INNER_PADDING = 2 * df.score.min()
LIMIT = (INNER_PADDING + df.score.max()) * 1.3  # Limit of the axes

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(30, 30))
ax.set(xlim=(-LIMIT, LIMIT), ylim=(-LIMIT, LIMIT))

for i, row in df.iterrows():
    bar_length = row.score
    length = bar_length + INNER_PADDING
    start = START_ANGLE + i * SIZE + PAD
    end = START_ANGLE + (i + 1) * SIZE
    angle = (end + start) / 2

    # Add variables here
    flag_zoom = 0.004 * length
    flag_x, flag_y = get_xy_with_padding(length, angle, 8 * flag_zoom)
    text_x, text_y = get_xy_with_padding(length, angle, 16 * flag_zoom)

    # Add functions here
    draw_wedge(ax, start, end, length, bar_length, color(row.income))
    # add_flag(ax, flag_x, flag_y, row.country, flag_zoom, angle)
    add_text(ax, text_x, text_y, row.country, bar_length, angle)

ax.text(1 - LIMIT, LIMIT - 2, "+ main title", fontsize=58)

# Add general functions here
draw_reference_line(ax, 2.0, 0.06, INNER_PADDING)
draw_reference_line(ax, 4.0, 0.06, INNER_PADDING)
draw_reference_line(ax, 6.0, 0.06, INNER_PADDING)
plt.title("World Happiness Report 2022".replace(" ", "\n"), x=0.5, y=0.5, va="center", ha="center", fontsize=64,
          linespacing=1.5)

add_legend(
    labels=["High income", "Upper middle income", "Lower middle income", "Low income", "Unknown"],
    colors=["#468FA8", "#62466B", "#E5625E", "#6B0F1A", "#909090"],
    title="Income level according to the World Bank\n"
)

plt.axis("off")
plt.tight_layout()
plt.show()
