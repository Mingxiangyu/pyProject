# -*- codeing = utf-8 -*-
# @Time :2023/6/3 23:41
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  test.py

# 上一条label的截止深度
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

# toDo 井构表数据，待放入库中，从库中查询
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


def test():
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

            # 根据不同类型曲线，获取不同的N
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

            # 根据不同类型曲线，获取不同的N
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

            print(label_item_start_end)
            print("\n")
        old_EndDepth = layer_old_endDepth



test()
