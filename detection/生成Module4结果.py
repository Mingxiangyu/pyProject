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

def test():
    label_depth_cursor = label_collection.find()
    label_depth_list = list(label_depth_cursor[:])
    print(label_depth_list)

test()