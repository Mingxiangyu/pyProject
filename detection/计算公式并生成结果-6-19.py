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
from pymongo import MongoClient

w = 0.25
v = -0.007

# toDo 修改N的识别逻辑

# toDo 井构表数据，待放入库中，从库中查询
l = {"type": 3, "start": 4.0667, "end": 897,
     "curve": [{"curve_type": 1, "Channel": "AD[15]", "W": 0.25, "V": -0.009, "LayerODin": 9.625, "LayerWtLbFt": 40,
                "LayerNomThkin": 0.395},
               {"curve_type": 2, "Channel": "AD[38]", "W": 0.25, "V": -0.006, "LayerODin": 13.375, "LayerWtLbFt": 72,
                "LayerNomThkin": 0.514},
               {"curve_type": 3, "Channel": "AD[54]", "W": 0.25, "V": -0.009, "LayerODin": 18.625, "LayerWtLbFt": 115,
                "LayerNomThkin": 0.594}]}
l1 = {"type": 2, "start": 897, "end": 4652.4,
      "curve": [{"curve_type": 1, "Channel": "AD[15]", "W": 0.25, "V": -0.009, "LayerODin": 9.625, "LayerWtLbFt": 40,
                 "LayerNomThkin": 0.395},
                {"curve_type": 2, "Channel": "AD[38]", "W": 0.42, "V": -0.001, "LayerODin": 13.375, "LayerWtLbFt": 72,
                 "LayerNomThkin": 0.514},
                {"curve_type": 3, "Channel": None, "W": 1, "V": 0}]}
l2 = {"type": 1, "start": 4652.4, "end": 5149.667,
      "curve": [{"curve_type": 1, "Channel": "AD[25]", "W": 0.25, "V": -0.007, "LayerODin": 9.625, "LayerWtLbFt": 40,
                 "LayerNomThkin": 0.395},
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
    print("开始清洗数据")
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

        # 定义一个字典，存储当前 layer 下所有 curve（Channel） 的数据
        channel_itme = {}

        # 定义一个字典，存储当前 layer 下所有 curve（Channel） 的起始数据
        label_start_end_item = {}

        # 循环曲线参数
        for curve_item in curve_list:
            # 定义一个上一个 label 的底深度值，初始值为 上一个 layer 的底深度值
            old_label_end_depth = old_EndDepth

            # 获取本次使用哪条曲线
            curve_name = curve_item.get("Channel")
            # 获取当前是第几类曲线
            curve_type = curve_item.get("curve_type")

            # 根据不同类型曲线，获取不同的N
            if curve_type == 1:
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的数据<标签：数据集合>
                label_item = {}
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的起始数据
                label_item_start_end = {}
                # 循环 label 结果
                for lable_depth in label_depth_list:
                    label_label = lable_depth.get("Label")

                    # 如果当前 Label 不是E或A，则直接跳过
                    if not label_label == "A" and not label_label == "E":
                        continue

                    # 获取当前 label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    # 如果 old_label_end_depth 的值比 label_start 还大，则认为当前 label 不用计算 N 的数据，只计算当前 label 数据即可
                    if old_label_end_depth > label_start:
                        pass
                    else:
                        # 记录 N 的数据
                        n_label_label = "N"
                        # 获取las文件中起始深度为 old_label_end_depth ，label_start 的所有行数据
                        n_query = {'Depth': {'$gte': old_label_end_depth, '$lte': label_start}}
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

                        # 当前 N 的起始深度值
                        n_label_start_end = {
                            "label_start": old_label_end_depth,
                            "label_end": label_start
                        }

                        # 将当前 n_label 的起始值记录下
                        n_start_end = label_item_start_end.get(n_label_label)
                        if n_start_end:
                            label_item_start_end[n_label_label].append(n_label_start_end)
                        else:
                            label_item_start_end[n_label_label] = []
                            label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新 old_label_end_depth
                    old_label_end_depth = label_end

                    # 记录当前 label 的数据
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

                # 如果 label_depth_list 循环完毕，但是最后的 old_label_end_depth 还是没等于 l1_end （当前管节的底）则把这一段当做 N
                if not old_label_end_depth == l1_end:
                    # 记录 N 的数据
                    n_label_label = "N"
                    # 获取las文件中起始深度为 old_label_end_depth ，label_start 的所有行数据
                    n_query = {'Depth': {'$gte': old_label_end_depth, '$lte': l1_end}}
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

                    # 当前 N 的起始深度值
                    n_label_start_end = {
                        "label_start": old_label_end_depth,
                        "label_end": l1_end
                    }

                    # 将当前 n_label 的起始值记录下
                    n_start_end = label_item_start_end.get(n_label_label)
                    if n_start_end:
                        label_item_start_end[n_label_label].append(n_label_start_end)
                    else:
                        label_item_start_end[n_label_label] = []
                        label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新 old_label_end_depth
                    old_label_end_depth = l1_end

                channel_itme[curve_name] = label_item
                label_start_end_item[curve_name] = label_item_start_end

            if curve_type == 2:
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的数据<标签：数据集合>
                label_item = {}
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的起始数据
                label_item_start_end = {}
                # 循环 label 结果
                for lable_depth in label_depth_list:
                    label_label = lable_depth.get("Label")

                    # 如果当前 Label 不是E或A，则直接跳过
                    if not label_label == "A" and not label_label == "B" and not label_label == "E":
                        continue

                    # 获取当前 label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    # 如果 old_label_end_depth 的值比 label_start 还大，则认为当前 label 不用计算 N 的数据，只计算当前 label 数据即可
                    if old_label_end_depth > label_start:
                        pass
                    else:
                        # 记录 N 的数据
                        n_label_label = "N"
                        # 获取las文件中起始深度为 old_label_end_depth ，label_start 的所有行数据
                        n_query = {'Depth': {'$gte': old_label_end_depth, '$lte': label_start}}
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

                        # 当前 N 的起始深度值
                        n_label_start_end = {
                            "label_start": old_label_end_depth,
                            "label_end": label_start
                        }

                        # 将当前 n_label 的起始值记录下
                        n_start_end = label_item_start_end.get(n_label_label)
                        if n_start_end:
                            label_item_start_end[n_label_label].append(n_label_start_end)
                        else:
                            label_item_start_end[n_label_label] = []
                            label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新 old_label_end_depth
                    old_label_end_depth = label_end

                    # 记录当前 label 的数据
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

                # 如果 label_depth_list 循环完毕，但是最后的 old_label_end_depth 还是没等于 l1_end （当前管节的底）则把这一段当做 N
                if not old_label_end_depth == l1_end:
                    # 记录 N 的数据
                    n_label_label = "N"
                    # 获取las文件中起始深度为 old_label_end_depth ，label_start 的所有行数据
                    n_query = {'Depth': {'$gte': old_label_end_depth, '$lte': l1_end}}
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

                    # 当前 N 的起始深度值
                    n_label_start_end = {
                        "label_start": old_label_end_depth,
                        "label_end": l1_end
                    }

                    # 将当前 n_label 的起始值记录下
                    n_start_end = label_item_start_end.get(n_label_label)
                    if n_start_end:
                        label_item_start_end[n_label_label].append(n_label_start_end)
                    else:
                        label_item_start_end[n_label_label] = []
                        label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新 old_label_end_depth
                    old_label_end_depth = l1_end

                channel_itme[curve_name] = label_item
                label_start_end_item[curve_name] = label_item_start_end

            if curve_type == 3:
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的数据<标签：数据集合>
                label_item = {}
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的起始数据
                label_item_start_end = {}
                # 循环 label 结果
                for lable_depth in label_depth_list:
                    label_label = lable_depth.get("Label")

                    # 如果当前 Label 不是E或A，则直接跳过
                    if not label_label == "A" and not label_label == "B" and not label_label == "C" and not label_label == "E":
                        continue

                    # 获取当前 label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    # 如果 old_label_end_depth 的值比 label_start 还大，则认为当前 label 不用计算 N 的数据，只计算当前 label 数据即可
                    if old_label_end_depth > label_start:
                        pass
                    else:
                        # 记录 N 的数据
                        n_label_label = "N"
                        # 获取las文件中起始深度为 old_label_end_depth ，label_start 的所有行数据
                        n_query = {'Depth': {'$gte': old_label_end_depth, '$lte': label_start}}
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

                        # 当前 N 的起始深度值
                        n_label_start_end = {
                            "label_start": old_label_end_depth,
                            "label_end": label_start
                        }

                        # 将当前 n_label 的起始值记录下
                        n_start_end = label_item_start_end.get(n_label_label)
                        if n_start_end:
                            label_item_start_end[n_label_label].append(n_label_start_end)
                        else:
                            label_item_start_end[n_label_label] = []
                            label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新 old_label_end_depth
                    old_label_end_depth = label_end

                    # 记录当前 label 的数据
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

                # 如果 label_depth_list 循环完毕，但是最后的 old_label_end_depth 还是没等于 l1_end （当前管节的底）则把这一段当做 N
                if not old_label_end_depth == l1_end:
                    # 记录 N 的数据
                    n_label_label = "N"
                    # 获取las文件中起始深度为 old_label_end_depth ，label_start 的所有行数据
                    n_query = {'Depth': {'$gte': old_label_end_depth, '$lte': l1_end}}
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

                    # 当前 N 的起始深度值
                    n_label_start_end = {
                        "label_start": old_label_end_depth,
                        "label_end": l1_end
                    }

                    # 将当前 n_label 的起始值记录下
                    n_start_end = label_item_start_end.get(n_label_label)
                    if n_start_end:
                        label_item_start_end[n_label_label].append(n_label_start_end)
                    else:
                        label_item_start_end[n_label_label] = []
                        label_item_start_end[n_label_label].append(n_label_start_end)

                    # 更新 old_label_end_depth
                    old_label_end_depth = l1_end

                channel_itme[curve_name] = label_item
                label_start_end_item[curve_name] = label_item_start_end

        # 该 layer 内 各曲线 循环完后更新全局 old_EndDepth 值，避免下一次 layer 的 old_label_end_depth 获取 old_EndDepth 值从0开始
        old_EndDepth = old_label_end_depth

        # 当前井构（L1）下所有标签的集合
        layer_item = []
        # 重新组装数据结构
        for channel, channel_value in channel_itme.items():
            # 获取管柱信息
            channel_w = None
            channel_v = None
            LayerODin = None
            LayerWtLbFt = None
            LayerNomThkin = None
            for curve_item in curve_list:
                if channel == curve_item.get('Channel'):
                    # 获取管柱信息
                    channel_w = curve_item.get("W")
                    channel_v = curve_item.get("V")
                    LayerODin = curve_item.get("LayerODin")
                    LayerWtLbFt = curve_item.get("LayerWtLbFt")
                    LayerNomThkin = curve_item.get("LayerNomThkin")
                    break

            channel_start_end = {
                "layer": l1_type,
                "channel_name": channel,
                "W": channel_w,
                "V": channel_v,
                "LayerODin": LayerODin,
                "LayerWtLbFt": LayerWtLbFt,
                "LayerNomThkin": LayerNomThkin,
            }
            channel_label_list = []
            # 如果该 channel（曲线） 是空的，则直接对data复制为空
            if channel:
                for label, value in channel_value.items():
                    label_item_start_end = label_start_end_item.get(channel)
                    start_end_get = label_item_start_end.get(label)
                    channel_label = {
                        "layer": l1_type,
                        "LayerODin": LayerODin,
                        "LayerWtLbFt": LayerWtLbFt,
                        "LayerNomThkin": LayerNomThkin,
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
            "layer_item": layer_item,
        }
        data.append(layer_data)
    return data


data = clean_data()


def curve_value_calculate(data, curve_depth, las_curve):
    """
    计算值每个深度的值
    :param data:  清洗后的las数据
    :param curve_depth: 曲线深度
    :param las_curve:  曲线深度对象
    :return:
    """

    # 定义对象接收该数据参数 方便后续查看
    depth_item_dict = {"Depth": curve_depth}

    for layer_data in data:
        layer_start = layer_data.get("layer_start")
        layer_end = layer_data.get("layer_end")
        # 如果曲线值不在当前 layer 中，则跳过，进行下次判断
        # toDO 判断如果当前是N，即没显示在layer中的深度值，应该如何判断
        if not is_between(layer_start, curve_depth, layer_end):
            continue

        # 记录当前深度属于哪个层级  方便后续查看
        layer_type = layer_data.get("layer_type")
        depth_item_dict["layer_type"] = layer_type
        # 将子字典放入字典中
        depth_channel_item_dict_list = []

        # 获取当前 layer 中所有 channel 标签集合
        channel_list = layer_data.get("layer_item")
        # 循环所有 channel
        for channel_item_data in channel_list:
            # 获取当前 channel 中所有 label 标签集合
            channel_data = channel_item_data.get('channel_data')
            channel_w = channel_item_data.get('W')
            channel_v = channel_item_data.get('V')

            # 记录当前 曲线值 属于哪个曲线，以及管道的信息  方便后续查看，放在一个子字典中，避免后续下一个曲线覆盖了
            channel_name = channel_item_data.get("channel_name")
            LayerODin = channel_item_data.get("LayerODin")
            LayerWtLbFt = channel_item_data.get("LayerWtLbFt")
            LayerNomThkin = channel_item_data.get("LayerNomThkin")
            depth_channel_item_dict = {"channel_name": channel_name}
            depth_channel_item_dict["LayerODin"] = LayerODin
            depth_channel_item_dict["LayerWtLbFt"] = LayerWtLbFt
            depth_channel_item_dict["LayerNomThkin"] = LayerNomThkin
            depth_channel_item_dict["LayerNomThkin"] = LayerNomThkin
            depth_channel_item_dict["label_type"] = None
            depth_channel_item_dict["curen_calculate"] = None

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

            # 循环曲线数据
            for label_item in channel_data:
                # 获取当前 label 下所有起始深度集合
                label_start_end = label_item.get("label_start_end")
                for label_start_end_item in label_start_end:
                    label_start = label_start_end_item.get("label_start")
                    label_end = label_start_end_item.get("label_end")

                    # 判断当前深度是否在该 label 下
                    if is_between(label_start, curve_depth, label_end):
                        layer_type = label_item.get("layer")
                        label_type = label_item.get('label_type')

                        # 记录曲线值相关信息  方便后续查看
                        depth_channel_item_dict["label_type"] = label_type

                        # 获取本次曲线名称
                        channel_name = label_item.get('channel_name')
                        curve_value = las_curve.get(channel_name)
                        calculate = getCalculate(layer_type=layer_type, label_label=label_type,
                                                 a_jun=a_jun, b_jun=b_jun, c_jun=c_jun, e_jun=e_jun, n_jun=n_jun,
                                                 w=channel_w, v=channel_v, curve_value=curve_value)
                        # 记录曲线值相关信息  方便后续查看
                        depth_channel_item_dict["curen_calculate"] = calculate
                        depth_channel_item_dict_list.append(depth_channel_item_dict)
                        break
                else:
                    continue  # 内层循环未被 break，继续执行外层循环
                break
                # 如果深度在所有都没有，则返回

            depth_item_dict["channel_item_dict"] = depth_channel_item_dict_list

    return depth_item_dict


def flatten_value(dic):
    """
    递归获取这个字典中所有value（包含子字典）
    :param dic:
    :return:
    """
    result = []
    for value in dic.values():
        if isinstance(value, dict):
            result.extend(flatten_value(value))
        elif isinstance(value, list):
            for elem in value:
                result.extend(flatten_value(elem))
        else:
            result.append(value)
    return result


def flatten_key(dic):
    result = []
    for key in dic.keys():
        value = dic[key]
        if isinstance(value, dict):
            result.extend(flatten_key(value))
        elif isinstance(value, list):
            for elem in value:
                result.extend(flatten_key(elem))
        else:
            result.append(key)
    return result


def write_data(data):
    las_curve_list = lascurve_collection.find()
    depth_list = []
    depth_header_list = []
    for las_curve in las_curve_list:
        curve_depth = las_curve.get("Depth")

        depth_item_dict = curve_value_calculate(data, curve_depth, las_curve)

        # toDo 如果数据前面没有，后面有值，用不用前面补None
        depth_item_list = flatten_value(depth_item_dict)
        depth_list.append(depth_item_list)

        # 添加csv表头
        if len(depth_header_list) < len(depth_item_list):
            depth_header_list = flatten_key(depth_item_dict)

    print("开始写入数据")
    # toDo 存储到数据库中
    # 将列表数据存储到 CSV 文件中
    with open('my_list.csv', 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(depth_header_list)
        for i in range(len(depth_list)):
            # merged_list = curve_depth_list[i] + list(curve_value_list)
            # writer.writerow(merged_list)
            writer.writerow(depth_list[i])


write_data(data)
