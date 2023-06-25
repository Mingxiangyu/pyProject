# -*- codeing = utf-8 -*-
# @Time :2023/5/29 0:03
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://blog.csdn.net/qq_45268814/article/details/125937255
# @File :  将csv存储到MongoDB.py
import pandas as pd
from pymongo import MongoClient


df = pd.read_csv('E:\WorkSpace\pyWorkSpace\pyProject\detection\Case-3_Edited_Raw_las.csv', encoding='utf-8')

# 将 DataFrame 对象转换为 JSON 格式
data_json = df.to_dict(orient='records')

# 连接 MongoDB 数据库
client = MongoClient(
    # 主机
    host="localhost",
    # 端口
    port=27017
    # ,
    # # 用户名
    # username="root",
    # # 密码
    # password="123456",
    # 需要用户名和密码进行身份认证的数据库
)
db = client["mydatabase"]
# las曲线表
collection = db['lascurve']

# 插入数据到 MongoDB 中
# collection.insert_many(data_json)

df = pd.read_csv('G:\软件备份\Project\测井\项目所需\Case-3文件及说明\Case-3_Label.csv', encoding='utf-8')
data_json = df.to_dict(orient='records')
db = client["mydatabase"]
# 标签表
collection = db['label']
# collection.insert_many(data_json)


df = pd.read_csv("E:\WorkSpace\pyWorkSpace\pyProject\detection\my_list.csv", encoding='utf-8')
data_json = df.to_dict(orient='records')
db = client["mydatabase"]
# 标签表
collection = db['Calculate']
collection.insert_many(data_json)


df = pd.read_csv("G:\软件备份\Project\测井\项目所需\Case-3文件及说明\API_PipeSpecificationsMaster.csv", encoding='utf-8')
data_json = df.to_dict(orient='records')
db = client["mydatabase"]
# 标签表
collection = db['PipeSpecificationsMaster']
# collection.insert_many(data_json)


