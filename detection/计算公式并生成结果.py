# -*- codeing = utf-8 -*-
# @Time :2023/6/3 23:41
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  test.py
import csv
import math

import pymongo
# 上一条label的截止深度
from pymongo import MongoClient

w = 0.25
v = -0.007

# toDo 修改N的识别逻辑

# toDo 井构表数据，待放入库中，从库中查询
# l = {"type": 3, "start": 4.0667, "end": 897}
# l1 = {"type": 2, "start": 897, "end": 4652.4}
l = {"type": 3, "start": 4.0667, "end": 897,
     "curve": [{"curve_type": 1, "Channel": "AD[15]", "W": 0.25, "V": -0.009},
               {"curve_type": 2, "Channel": "AD[38]", "W": 0.25, "V": -0.006},
               {"curve_type": 3, "Channel": "AD[54]", "W": 0.25, "V": -0.009}]}
l1 = {"type": 2, "start": 897, "end": 4652.4,
      "curve": [{"curve_type": 1, "Channel": "AD[15]", "W": 0.25, "V": -0.009},
                {"curve_type": 2, "Channel": "AD[38]", "W": 0.42, "V": -0.001},
                {"curve_type": 3, "Channel": None, "W": 1, "V": 0}]}
l2 = {"type": 1, "start": 4652.4, "end": 5149.667,
      "curve": [{"curve_type": 1, "Channel": "AD[25]", "W": 0.25, "V": -0.007},
                {"curve_type": 2, "Channel": None, "W": 1, "V": 0},
                {"curve_type": 3, "Channel": None, "W": 1, "V": 0}]}
layer = [l, l1, l2]

# 连接 MongoDB 数据库
client = MongoClient(
    # 主机
    host="localhost",
    # 端口
    port=27017,
    # 用户名
    # username="root",
    # 密码
    # password="123456",
    # 需要用户名和密码进行身份认证的数据库
)
# 获取数据库
db = client["mydatabase"]
# 获取曲线数据 las 表数据
lascurve_collection = db['lascurve']
# 添加索引
lascurve_collection.create_index([("Depth", pymongo.ASCENDING)])
# 获取label（标签表）数据
label_collection = db['label']


def getAvg(data):
    """
    获取均值
    :param data:
    :return:
    """
    if data:
        avg = sum(data) / len(data)
        print(f"avg = {avg}\n")
        return avg


def is_between(a, x, b):
    """
    判断 x 是否在 a 和 b 之间
    :param a: 小数
    :param x: 判断数
    :param b:  大数
    :return: true or false
    """
    if math.isnan(a):
        print("a不是数")
        a = 0
    if math.isnan(b):
        print("b不是数")
        b = 0
    return min(a, b) <= x <= max(a, b)


def getCalculate(layer_type, label_label, a_jun, b_jun, c_jun, e_jun, n_jun, w, v, curve_value):
    """
        进行计算
        :param layer_type: 井构类型，1类，2类，3类等
        :param label_label:  管节标签，A，B，C
        :param a_jun:  a均值
        :param b_jun:
        :param c_jun:
        :param e_jun:
        :param n_jun:
        :param w: 计算参数1
        :param v: 计算参数2
        :param curve_value: 曲线中当前值
        :return:
    """
    # 参数和计算公式的字典
    params = {
        1: {
            "N": {"params": [a_jun, e_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, e_jun, n_jun: w * (
                    1 / w - 1 / 2 + curve_value / n_jun - (a_jun + e_jun) / 2) + v},
            "E": {"params": [e_jun, n_jun], "formula": lambda w, v, curve_value, e_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v},
            "A": {"params": [a_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v}
        },
        2: {
            "N": {"params": [a_jun, b_jun, e_jun, n_jun],
                  "formula": lambda w, v, curve_value, a_jun, b_jun, e_jun, n_jun: w * (
                          1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + e_jun) / 2) + v},
            "E": {"params": [e_jun, n_jun], "formula": lambda w, v, curve_value, e_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v},
            "B": {"params": [b_jun, n_jun], "formula": lambda w, v, curve_value, b_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v},
            "A": {"params": [a_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v}
        },
        3: {
            "N": {"params": [a_jun, b_jun, c_jun, e_jun, n_jun],
                  "formula": lambda w, v, curve_value, a_jun, b_jun, c_jun, e_jun, n_jun: w * (
                          1 / w - 1 / 2 + curve_value / n_jun - (a_jun + b_jun + c_jun + e_jun) / 2) + v},
            "E": {"params": [e_jun, n_jun], "formula": lambda w, v, curve_value, e_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (e_jun) / 2) + v},
            "C": {"params": [c_jun, n_jun], "formula": lambda w, v, curve_value, c_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (c_jun) / 2) + v},
            "B": {"params": [b_jun, n_jun], "formula": lambda w, v, curve_value, b_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (b_jun) / 2) + v},
            "A": {"params": [a_jun, n_jun], "formula": lambda w, v, curve_value, a_jun, n_jun: w * (
                    1 / w - 3 / 2 + curve_value / n_jun + (a_jun) / 2) + v}
        }
    }
    # 获取对应的参数和计算公式
    params_dict = params.get(layer_type, {}).get(label_label, None)
    if params_dict is None:
        return None
    params_list = params_dict["params"]
    formula = params_dict["formula"]
    # 使用参数和计算公式计算结果
    calculate = formula(w, v, curve_value, *params_list)
    return calculate


def clean_data():
    data = []
    # 定义一个全局的结束参数，用来获取 N(管节) 的起始值
    old_EndDepth = 0
    # 循环 layer 数据
    for layer_value in layer:
        #     获取当前layer的起始深度
        l1_start = layer_value.get("start")
        l1_end = layer_value.get("end")
        l1_type = layer_value.get("type")
        # 获取当前layer的曲线参数
        curve_list = layer_value.get("curve")

        #     将起始深度当做查询参数进行 label 查询
        query = {'StartDepth': {'$gte': l1_start}, "EndDepth": {'$lte': l1_end}}
        Depth = label_collection.find(query)
        label_depth_list = list(Depth[:])
        print(label_depth_list)
        print("\n")

        # 定义一个字典，存储当前 layer 下所有 curve（Channel） 的数据
        channel_itme = {}

        label_item_start_end = {}

        # 循环曲线参数
        for curve_item in curve_list:
            # 定义一个当前 layer 的的结束参数，用来获取 N(管节) 的起始值
            layer_old_endDepth = old_EndDepth

            # 获取本次使用哪条曲线
            curve_name = curve_item.get("Channel")
            # 获取当前是第几类曲线
            curve_type = curve_item.get("curve_type")

            # 根据不同类型曲线，获取不同的N
            if curve_type == 1:
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的数据<标签：数据集合>
                label_item = {}
                # 循环 label 结果
                for lable_depth in label_depth_list:
                    label_label = lable_depth.get("Label")

                    # 如果当前 Label 不是E或A，则直接跳过
                    if not label_label == "A" and not label_label == "E":
                        continue

                    # 获取当前label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    n_label_label = "N"
                    # 获取las文件中起始深度为 layer_old_endDepth ，label_start 的所有行数据
                    n_query = {'Depth': {'$gte': layer_old_endDepth, '$lte': label_start}}
                    n_Depth = lascurve_collection.find(n_query)
                    n_Depth_list = [doc for doc in n_Depth]

                    # 取出指定曲线 curve 那一列的值
                    n_curve_list = [n_Depth_Value.get(curve_name) for n_Depth_Value in n_Depth_list]

                    # 判断当前label是否存在，如果存在则 extend（合并两个集合值），如果不存在则创建个新字典
                    n_judge_ = label_item.get(n_label_label)
                    if n_judge_:
                        n_judge_.extend(n_curve_list)
                    else:
                        label_item[n_label_label] = n_curve_list

                    # 当前标签（label）的起始深度值
                    n_label_start_end = {
                        "label_start": layer_old_endDepth,
                        "label_end": label_start
                    }

                    # 将当前 n_label 的起始值记录下
                    n_start_end = label_item_start_end.get(n_label_label)
                    if n_start_end:
                        label_item_start_end[n_label_label].append(n_label_start_end)
                    else:
                        label_item_start_end[n_label_label] = []
                        label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新上一条Label的截止深度
                    layer_old_endDepth = label_end

                    # 当前标签（label）的起始深度值
                    label_start_end = {
                        "label_start": label_start,
                        "label_end": label_end
                    }

                    # 将当前 label 的起始值记录下
                    start_end = label_item_start_end.get(label_label)
                    if start_end:
                        label_item_start_end[label_label].append(label_start_end)
                    else:
                        label_item_start_end[label_label] = []
                        label_item_start_end[label_label].append(label_start_end)

                    # 获取las文件中起始深度为 StartDepth ，EndDepth 的所有行数据
                    query = {'Depth': {'$gte': label_start, '$lte': label_end}}
                    Depth = lascurve_collection.find(query)

                    Depth_list = [doc for doc in Depth]
                    # 取出指定曲线 curve 那一列的值
                    curve_list_ = [Depth_Value.get(curve_name) for Depth_Value in Depth_list]

                    # 判断当前label是否存在，如果存在则 extend（合并两个集合值），如果不存在则创建个新字典
                    judge_ = label_item.get(label_label)
                    if judge_:
                        judge_.extend(curve_list_)
                    else:
                        label_item[label_label] = curve_list_
                channel_itme[curve_name] = label_item

            if curve_type == 2:
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的数据<标签：数据集合>
                label_item = {}
                # 循环 label 结果
                for lable_depth in label_depth_list:
                    label_label = lable_depth.get("Label")

                    # 如果当前 Label 不是E或A，则直接跳过
                    if not label_label == "A" and not label_label == "B" and not label_label == "E":
                        continue

                    # 获取当前label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    n_label_label = "N"
                    # 获取las文件中起始深度为 layer_old_endDepth ，label_start 的所有行数据
                    n_query = {'Depth': {'$gte': layer_old_endDepth, '$lte': label_start}}
                    n_Depth = lascurve_collection.find(n_query)
                    n_Depth_list = [doc for doc in n_Depth]

                    # 取出指定曲线 curve 那一列的值
                    n_curve_list = [n_Depth_Value.get(curve_name) for n_Depth_Value in n_Depth_list]

                    # 判断当前label是否存在，如果存在则 extend（合并两个集合值），如果不存在则创建个新字典
                    n_judge_ = label_item.get(n_label_label)
                    if n_judge_:
                        n_judge_.extend(n_curve_list)
                    else:
                        label_item[n_label_label] = n_curve_list

                    # 当前标签（label）的起始深度值
                    n_label_start_end = {
                        "label_start": layer_old_endDepth,
                        "label_end": label_start
                    }

                    # 将当前 n_label 的起始值记录下
                    n_start_end = label_item_start_end.get(n_label_label)
                    if n_start_end:
                        label_item_start_end[n_label_label].append(n_label_start_end)
                    else:
                        label_item_start_end[n_label_label] = []
                        label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新上一条Label的截止深度
                    layer_old_endDepth = label_end

                    # 当前标签（label）的起始深度值
                    label_start_end = {
                        "label_start": label_start,
                        "label_end": label_end
                    }

                    # 将当前 label 的起始值记录下
                    start_end = label_item_start_end.get(label_label)
                    if start_end:
                        label_item_start_end[label_label].append(label_start_end)
                    else:
                        label_item_start_end[label_label] = []
                        label_item_start_end[label_label].append(label_start_end)

                    # 获取las文件中起始深度为 StartDepth ，EndDepth 的所有行数据
                    query = {'Depth': {'$gte': label_start, '$lte': label_end}}
                    Depth = lascurve_collection.find(query)

                    Depth_list = [doc for doc in Depth]
                    # 取出指定曲线 curve 那一列的值
                    curve_list_ = [Depth_Value.get(curve_name) for Depth_Value in Depth_list]

                    # 判断当前label是否存在，如果存在则 extend（合并两个集合值），如果不存在则创建个新字典
                    judge_ = label_item.get(label_label)
                    if judge_:
                        judge_.extend(curve_list_)
                    else:
                        label_item[label_label] = curve_list_
                channel_itme[curve_name] = label_item

            if curve_type == 3:
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的数据<标签：数据集合>
                label_item = {}
                # 循环 label 结果
                for lable_depth in label_depth_list:
                    label_label = lable_depth.get("Label")

                    # 如果当前 Label 不是E或A，则直接跳过
                    if not label_label == "A" and not label_label == "B" and not label_label == "C" and not label_label == "E":
                        continue

                    # 获取当前label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    n_label_label = "N"
                    # 获取las文件中起始深度为 layer_old_endDepth ，label_start 的所有行数据
                    n_query = {'Depth': {'$gte': layer_old_endDepth, '$lte': label_start}}
                    n_Depth = lascurve_collection.find(n_query)
                    n_Depth_list = [doc for doc in n_Depth]

                    # 取出指定曲线 curve 那一列的值
                    n_curve_list = [n_Depth_Value.get(curve_name) for n_Depth_Value in n_Depth_list]

                    # 判断当前label是否存在，如果存在则 extend（合并两个集合值），如果不存在则创建个新字典
                    n_judge_ = label_item.get(n_label_label)
                    if n_judge_:
                        n_judge_.extend(n_curve_list)
                    else:
                        label_item[n_label_label] = n_curve_list

                    # 当前标签（label）的起始深度值
                    n_label_start_end = {
                        "label_start": layer_old_endDepth,
                        "label_end": label_start
                    }

                    # 将当前 n_label 的起始值记录下
                    n_start_end = label_item_start_end.get(n_label_label)
                    if n_start_end:
                        label_item_start_end[n_label_label].append(n_label_start_end)
                    else:
                        label_item_start_end[n_label_label] = []
                        label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新上一条Label的截止深度
                    layer_old_endDepth = label_end

                    # 当前标签（label）的起始深度值
                    label_start_end = {
                        "label_start": label_start,
                        "label_end": label_end
                    }

                    # 将当前 label 的起始值记录下
                    start_end = label_item_start_end.get(label_label)
                    if start_end:
                        label_item_start_end[label_label].append(label_start_end)
                    else:
                        label_item_start_end[label_label] = []
                        label_item_start_end[label_label].append(label_start_end)

                    # 获取las文件中起始深度为 StartDepth ，EndDepth 的所有行数据
                    query = {'Depth': {'$gte': label_start, '$lte': label_end}}
                    Depth = lascurve_collection.find(query)

                    Depth_list = [doc for doc in Depth]
                    # 取出指定曲线 curve 那一列的值
                    curve_list_ = [Depth_Value.get(curve_name) for Depth_Value in Depth_list]

                    # 判断当前label是否存在，如果存在则 extend（合并两个集合值），如果不存在则创建个新字典
                    judge_ = label_item.get(label_label)
                    if judge_:
                        judge_.extend(curve_list_)
                    else:
                        label_item[label_label] = curve_list_
                channel_itme[curve_name] = label_item
            # 如果曲线名称为空，则当前曲线不进行后续计算
            # if not curve_name:
            #     continue

        # 该 layer 内 各曲线 循环完后更新全局old_EndDepth 值，避免下一次 layer 获取 old_EndDepth 值从0开始
        old_EndDepth = layer_old_endDepth

        # 当前井构（L1）下所有标签的集合
        layer_item = []
        # 重新组装数据结构
        for channel, channel_value in channel_itme.items():
            channel_w = None
            channel_v = None
            for curve_item in curve_list:
                if channel == curve_item.get('Channel'):
                    channel_w = curve_item.get("W")
                    channel_v = curve_item.get("V")
                    break

            channel_start_end = {
                "layer": l1_type,
                "channel_name": channel,
                "W": channel_w,
                "V": channel_v
            }
            channel_label_list = []
            # 如果该 channel（曲线） 是空的，则直接对data复制为空
            if channel:
                for label, value in channel_value.items():
                    start_end_get = label_item_start_end.get(label)
                    channel_label = {
                        "layer": l1_type,
                        "channel_name": channel,
                        "label_type": label,
                        "label_start_end": start_end_get,
                        "data": value,
                        "avg": getAvg(value)
                    }
                    channel_label_list.append(channel_label)
            channel_start_end["channel_data"] = channel_label_list
            layer_item.append(channel_start_end)

        layer_data = {
            "layer_start": l1_start,
            "layer_end": l1_end,
            "layer_type": l1_type,
            "layer_item": layer_item
        }
        data.append(layer_data)
    return data


data = clean_data()


def curve_value_calculate(data, curve_depth, las_curve):
    calculate_list = []
    depth_list = []
    for layer_data in data:
        layer_start = layer_data.get("layer_start")
        layer_end = layer_data.get("layer_end")
        # 如果曲线值不在当前 layer 中，则跳过，进行下次判断
        # toDO 判断如果当前是N，即没显示在layer中的深度值，应该如何判断
        if not is_between(layer_start, curve_depth, layer_end):
            continue

        # 获取当前 layer 中所有 label 标签集合
        layer_item = layer_data.get("layer_item")
        for layer_data in layer_item:
            channel_data = layer_data.get('channel_data')
            channel_w = layer_data.get('W')
            channel_v = layer_data.get('V')

            # 因为下面计算可能用上所有均值，所以提前获取所有均值
            n_jun, a_jun, b_jun, c_jun, e_jun = [0 for i in range(5)]
            for label_item in channel_data:
                if label_item.get("label_type") == "N":
                    n_jun = label_item.get("avg")
                elif label_item.get("label_type") == "A":
                    a_jun = label_item.get("avg")
                elif label_item.get("label_type") == "B":
                    b_jun = label_item.get("avg")
                elif label_item.get("label_type") == "C":
                    c_jun = label_item.get("avg")
                elif label_item.get("label_type") == "E":
                    e_jun = label_item.get("avg")

            for label_item in channel_data:
                # 获取当前 label 下所有起始深度集合
                label_start_end = label_item.get("label_start_end")
                for label_start_end_item in label_start_end:
                    label_start = label_start_end_item.get("label_start")
                    label_end = label_start_end_item.get("label_end")

                    # 添加该深度数据值，方便后续查看
                    if not depth_list:
                        depth_list.append(curve_depth)
                        depth_list.append(label_item.get("layer"))

                    # 判断当前深度是否在该 label 下
                    if is_between(label_start, curve_depth, label_end):
                        layer_type = label_item.get("layer")
                        label_type = label_item.get('label_type')

                        if not len(depth_list) > 2:
                            # 如果 depth_list 的size不大于2，则证明还没有添加 label_type
                            depth_list.append(label_item.get('label_type'))

                        # 获取本次曲线名称
                        channel_name = label_item.get('channel_name')
                        curve_value = las_curve.get(channel_name)
                        calculate = getCalculate(layer_type=layer_type, label_label=label_type,
                                                 a_jun=a_jun, b_jun=b_jun, c_jun=c_jun, e_jun=e_jun, n_jun=n_jun,
                                                 w=channel_w, v=channel_v, curve_value=curve_value)
                        # 得到计算结果后返回
                        calculate_list.append(calculate)
                        break
                else:
                    continue  # 内层循环未被 break，继续执行外层循环
                break
                # 如果深度在所有都没有，则返回

    return calculate_list, depth_list


def write_data(data):
    curve_value_list = []
    curve_depth_list = []
    las_curve_list = lascurve_collection.find()
    for las_curve in las_curve_list:
        curve_depth = las_curve.get("Depth")

        calculate, depth_list = curve_value_calculate(data, curve_depth, las_curve)
        curve_value_list.append(calculate)
        curve_depth_list.append(depth_list)
    # toDo 存储到数据库中
    # 将列表数据存储到 CSV 文件中
    with open('my_list.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        csv_h0eader = ["Depth", "Layer", "Lable", "Curve1", "Curve2", "Curve3"]
        writer.writerow(csv_h0eader)
        for i in range(len(curve_depth_list)):
            writer.writerow([row for row in curve_depth_list[i]] + [row for row in curve_value_list[i]])


write_data(data)
