# -*- codeing = utf-8 -*-
# @Time :2023/6/3 23:41
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  test.py

# 上一条label的截止深度
import csv

from pymongo import MongoClient

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
# 获取label（标签表）数据
label_collection = db['label']
# 获取管道规范数据
PipeSpecifications_collection = db['pipe_specification']
# 获取公式计算结果
calculate_collection = db['Calculate']

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

        #     将起始深度当做查询参数进行 label 查询
        query = {'StartDepth': {'$gte': l1_start}, "EndDepth": {'$lte': l1_end}}
        Depth = label_collection.find(query)
        label_depth_list = list(Depth[:])

        # 定义一个字典，存储当前 layer 下所有 curve（Channel） 的数据
        channel_itme = {}

        # 定义一个字典，存储当前 layer 下所有 curve（Channel） 的起始数据
        label_start_end_item = {}

        # 获取当前layer的曲线参数
        curve_list = layer_value.get("curve")
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
                # 定义一个字典，存储当前 layer 下当前 curve（Channel） 下所有标签和对应的起始数据
                label_item_start_end = {}
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
                channel_itme[curve_name] = label_item
                label_start_end_item[curve_name] = label_item_start_end

            # 根据不同类型曲线，获取不同的N
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

                    # 获取当前label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    n_label_label = "N"

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

                channel_itme[curve_name] = label_item
                label_start_end_item[curve_name] = label_item_start_end

            # 根据不同类型曲线，获取不同的N
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

                    # 获取当前label 的起始值
                    label_start = lable_depth.get("StartDepth")
                    label_end = lable_depth.get("EndDepth")

                    n_label_label = "N"

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

                channel_itme[curve_name] = label_item
                label_start_end_item[curve_name] = label_item_start_end

            print(label_start_end_item)
            print("\n")
        old_EndDepth = layer_old_endDepth

        # 当前井构（L1）下所有标签的集合
        layer_item = []
        # 重新组装数据结构
        for channel, channel_value in channel_itme.items():
            channel_w = None
            channel_v = None
            curve_type = None
            for curve_item in curve_list:
                if channel == curve_item.get('Channel'):
                    channel_w = curve_item.get("W")
                    channel_v = curve_item.get("V")
                    curve_type = curve_item.get("curve_type")
                    break

            channel_start_end = {
                "layer": l1_type,
                "channel_name": channel,
                "curve_type": curve_type,
                "W": channel_w,
                "V": channel_v
            }
            # 如果该 channel（曲线） 是空的，则直接对data复制为空
            if channel:
                label_item_start_end = label_start_end_item.get(channel)
                start_end_get = label_item_start_end.get("N")
                channel_start_end["channel_data"] = start_end_get
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


def rebuild_data(data):
    # 重新组装数据，key为 channelType，value为对应的起始值集合
    channel_start_end = {}
    for layer in data:
        layer_item = layer.get("layer_item")
        for layer_item_data in layer_item:
            layer_item_start_end_list = layer_item_data.get("channel_data")

            # 如果起始数据集合为空，则直接跳过
            if not layer_item_start_end_list:
                continue

            curve_type = layer_item_data.get("curve_type")
            # 将当前 n_label 的起始值记录下
            start_end = channel_start_end.get(curve_type)
            if start_end:
                channel_start_end[curve_type].extend(layer_item_start_end_list)
            else:
                channel_start_end[curve_type] = []
                channel_start_end[curve_type].extend(layer_item_start_end_list)
    return channel_start_end


rebuild_data = rebuild_data(data)


def write_data(rebuild_data):
    for channel_start_end_key in rebuild_data:
        print(channel_start_end_key)
        start_end = rebuild_data.get(channel_start_end_key)

        row = []
        for start_end_item in start_end:
            top = start_end_item.get("label_start")
            bottom = start_end_item.get("label_end")
            length = bottom - top
            # toDo 后续传输进来
            nom_od = 9.625
            weight = 40

            PipeSpecifications_query = {'OD Ins': {'$eq': nom_od}, "Weight (lb/ft)": {'$eq': weight}}
            PipeSpecifications = PipeSpecifications_collection.find(PipeSpecifications_query)
            PipeSpecifications = list(PipeSpecifications)
            PipeSpecifications = PipeSpecifications[0]

            thickness = PipeSpecifications.get("Wall Thickness")

            # toDo 需要修改，是大于等于还是大于
            calculate_query = {'Depth': {'$gte': top, '$lte': bottom}}
            calculate_list = calculate_collection.find(calculate_query)
            collection_list = list(calculate_list)

            if channel_start_end_key == 1:
                collection_list.sort(key=lambda p: p.Curve1)
            if channel_start_end_key == 2:
                collection_list.sort(key=lambda p: p.Curve2)
            if channel_start_end_key == 3:
                collection_list.sort(key=lambda p: p.Curve3)

            print(collection_list)

        with open('Joint Analysis.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            csv_h0eader = ["Depth", "Layer", "Lable", "Curve1", "Curve2", "Curve3"]
            writer.writerow(csv_h0eader)
            for i in range(len(row)):
                writer.writerow([row_data for row_data in row[i]] )

        # for layer_item_start_end in layer_item_start_end_list:


write_data(rebuild_data)
