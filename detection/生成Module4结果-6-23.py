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
PipeSpecifications_collection = db['PipeSpecificationsMaster']
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


def searchDictionary(layerODin, layerWtLbFt, my_set):
    """
    查询字典集合中是否存在 LayerODin 值为 layerODin， LayerWtLbFt 值为 layerWtLbFt 的字典，
    如果存在则返回该字典，否则则返回空字典
    :param layerODin: 查询条件1
    :param layerWtLbFt: 查询条件2
    :param my_set: 字典集合
    :return: 字典
    """
    result = list(filter(lambda x: x.get("LayerODin") == layerODin and x.get("LayerWtLbFt") == layerWtLbFt, my_set))

    if len(result) > 0:
        print(result[0])
        return result[0]
    else:
        print("未找到匹配的字典")
        return {}


def get_grade(max_loss):
    if max_loss < 0:
        return "Special Joint"
    elif max_loss < 5:
        return "Negligible"
    elif max_loss < 10:
        return "Light"
    elif max_loss < 20:
        return "Moderate"
    else:
        return "Intensive"


def clean_data():
    print("开始清洗数据")
    data = []
    # 定义一个全局的结束参数，用来获取 管节 的起始值
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

                # 如果 label_depth_list 循环完毕，但是最后的 old_label_end_depth 还是没等于 l1_end （当前管节的底）则把这一段当做 N
                if not old_label_end_depth == l1_end:
                    # 记录 N 的数据
                    n_label_label = "N"

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
                    if not label_label == "B" and not label_label == "E":
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

                # 如果 label_depth_list 循环完毕，但是最后的 old_label_end_depth 还是没等于 l1_end （当前管节的底）则把这一段当做 N
                if not old_label_end_depth == l1_end:
                    # 记录 N 的数据
                    n_label_label = "N"

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
                    if not label_label == "C" and not label_label == "E":
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

                # 如果 label_depth_list 循环完毕，但是最后的 old_label_end_depth 还是没等于 l1_end （当前管节的底）则把这一段当做 N
                if not old_label_end_depth == l1_end:
                    # 记录 N 的数据
                    n_label_label = "N"

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
                label_item_start_end = label_start_end_item.get(channel)
                start_end_get = label_item_start_end.get("N")
                channel_start_end["channel_data"] = start_end_get
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


def rebuild_data(data):
    # 重新组装数据，key为 channelType，value为对应的起始值集合
    rebuild_data = []
    for layer in data:
        for layer_item in layer.get("layer_item", []):
            layerODin = layer_item.get("LayerODin")
            layerWtLbFt = layer_item.get("LayerWtLbFt")

            # 如果存在没有管柱信息的数据，直接跳过
            if not layerODin and not layerWtLbFt:
                continue

            # 通过 LayerODin LayerWtLbFt 获取 rebuild_data 是否已经存在该对象，如果存在，则往 channel_data 集合中追加数据，否则新建一个对象
            cleaned_item = searchDictionary(layerODin, layerWtLbFt, rebuild_data)

            cleaned_item["LayerNomThkin"] = layer_item.get("LayerNomThkin")
            cleaned_item["LayerODin"] = layerODin
            cleaned_item["LayerWtLbFt"] = layerWtLbFt

            # 获取该管柱内所有管节信息（顶底值）
            channel_data = cleaned_item.get("channel_data", [])
            # 如果该管柱没有顶底数据，则认为是一个新管柱，添加到集合中，
            if not channel_data:
                rebuild_data.append(cleaned_item)

            # 如果该管柱存在顶底数据，则追加即可
            channel_data.extend(layer_item.get("channel_data", []))
            cleaned_item["channel_data"] = channel_data

    return rebuild_data


rebuild_data = rebuild_data(data)


def write_data(rebuild_data):
    #  每一根管柱写一个表
    for channel in rebuild_data:
        # 管柱信息
        layerODin = channel.get("LayerODin")
        layerWtLbFt = channel.get("LayerWtLbFt")
        start_end = channel.get("channel_data")

        # 查询管柱规范信息 todo 如果尺寸不对，直接返回异常，不进行计算，如果重量不对，则基于该尺寸找最接近的重量
        PipeSpecifications_query = {'OD Ins': {'$eq': layerODin}, "Weight (lb/ft)": {'$eq': layerWtLbFt}}
        PipeSpecifications = PipeSpecifications_collection.find(PipeSpecifications_query)
        PipeSpecifications = list(PipeSpecifications)
        PipeSpecifications = PipeSpecifications[0]

        # 管柱信息
        thickness_ins = PipeSpecifications.get("Wall Thickness ins")
        thickness_mm = PipeSpecifications.get("Wall Thickness mm")

        itemNO = 0
        # 准备csv的数据
        header = []
        row = []
        for start_end_item in start_end:
            data = []
            itemNO += 1
            data.append(itemNO)
            if "Item" not in header:   header.append("Item")

            # 管节信息
            top = start_end_item.get("label_start")
            bottom = start_end_item.get("label_end")
            length = bottom - top

            data.append(top)
            if "Top" not in header:  header.append("Top")
            data.append(bottom)
            if "Bottom" not in header:  header.append("Bottom")
            data.append(length)
            if "Length" not in header:  header.append("Length")

            data.append(layerODin)
            if "NomOD" not in header:  header.append("NomOD")
            data.append(layerWtLbFt)
            if "Weight" not in header:  header.append("Weight")
            data.append(thickness_ins)
            if "TNom" not in header:  header.append("TNom")

            # toDo 需要修改，是大于等于还是大于
            # 获取该管节的计算后信息
            calculate_query = {'Depth': {'$gte': top, '$lte': bottom}}
            calculate_list = calculate_collection.find(calculate_query)
            calculate_list = list(calculate_list)

            # 统计该管节内所有数据的深度和value信息
            calculate_data_list = []
            for calculate in calculate_list:
                channel_item_dict = calculate.get("channel_item_dict")
                if not channel_item_dict:
                    continue

                Depth = calculate.get("Depth")
                for channel_item in channel_item_dict:
                    channel_layerODin = channel_item.get("LayerODin")
                    channel_layerWtLbFt = channel_item.get("LayerWtLbFt")

                    if channel_layerODin == layerODin and channel_layerWtLbFt == layerWtLbFt:
                        calculate_data = {"Depth": Depth}
                        calculate_data["curve_calculate"] = channel_item.get("curve_calculate")
                        calculate_data_list.append(calculate_data)
                        break

            max_calculate_dict = max(calculate_data_list, key=lambda x: x["curve_calculate"])
            max_calculate_value = max_calculate_dict.get("curve_calculate")
            # 获取最小损失百分比，剩余（计算结果）的最大即是损失的最小
            minLoss = 100 - max_calculate_value

            min_calculate_dict = min(calculate_data_list, key=lambda x: x["curve_calculate"])
            min_calculate_depth = min_calculate_dict.get("Depth")
            min_calculate_value = min_calculate_dict.get("curve_calculate")
            # 获取最大损失百分比，剩余（计算结果）的最小即是损失的最大
            maxLoss = 100 - min_calculate_value

            data.append(maxLoss)
            if "MaxLoss%" not in header:  header.append("MaxLoss%")
            data.append(min_calculate_depth)
            if "DptMxLos" not in header:  header.append("DptMxLos")

            total_calculate = sum(d["curve_calculate"] for d in calculate_data_list)
            average_calculate_value = total_calculate / len(calculate_data_list)
            # 获取平均损失百分比，剩余（计算结果）的最小即是损失的最大
            avLoss = 100 - average_calculate_value

            data.append(avLoss)
            if "AvLoss%" not in header:  header.append("AvLoss%")

            defect = maxLoss - minLoss

            data.append(defect)
            if "Defect%" not in header:  header.append("Defect%")

            # 获取该管节最小值
            minimal_thickness = thickness_ins * (100 - maxLoss) / 100

            data.append(minimal_thickness)
            if "TMin" not in header:  header.append("TMin")

            # 获取该管节最大值
            maximal_thickness = thickness_ins * (100 - minLoss) / 100

            data.append(maximal_thickness)
            if "TMax" not in header:  header.append("TMax")

            # 获取该管节平均值
            average_thickness = thickness_ins * (100 - avLoss) / 100

            data.append(average_thickness)
            if "TAvg" not in header:  header.append("TAvg")

            # 获取该管节平均损失值
            TRmn = thickness_ins - thickness_ins * (100 - avLoss) / 100

            data.append(TRmn)
            if "TRmn" not in header:  header.append("TRmn")

            grade = get_grade(maxLoss)

            data.append(grade)
            if "Grade" not in header:  header.append("Grade")

            row.append(data)

        with open(f'Joint Analysis{layerODin}-{layerWtLbFt}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for i in range(len(row)):
                writer.writerow([row_data for row_data in row[i]])


write_data(rebuild_data)
