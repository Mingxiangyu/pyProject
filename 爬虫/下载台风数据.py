# -*- codeing = utf-8 -*-
# @Time :2022/11/18 15:18
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://blog.csdn.net/qazwsxpy/article/details/127427409
# @link：https://www.heywhale.com/mw/project/5f79e83afab2e80030065a64/content
# @File :  下载台风数据.py
import json

import requests

# 这里是要导入台风的网址信息，我们需要在浏览器的检查页面找到url、User-Agent和Referer
url = "http://typhoon.zjwater.gov.cn/Api/TyphoonInfo/201319?callback=jQuery183013901695455458607_1600832880669&_=1600833055079"

req_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "Referer": "http://typhoon.zjwater.gov.cn/"
}

# 读取数据
r = requests.get(url, headers=req_header)
content_str = r.text[44:-3]
# 这个地方是最容易出错的，如果没有{，就读不出数据，这是因为本网页提供的数据如果读取成字符串格式前面少一个'{'，这个问题我解决了好久
mystring = '{' + content_str
# 将字符串转为json对象
content_json = json.loads(mystring)

# 在points外的一些变量，描述台风的整体信息
centerlat = content_json["centerlat"]
centerlng = content_json["centerlng"]
endtime = content_json["endtime"]
name = content_json["enname"]

# 创建csv文件
file_name = 'Usagi2013.csv'
mystring0 = 'name,lon,lat,movedirection,movespeed,power,pressure,speed,strong'
f = open(file_name, 'a')
f.write(mystring0)
f.write("\n")

# 读取变量名
for point in content_json["points"]:
    lat = point["lat"]  # 纬度
    lng = point["lng"]  # 经度
    movedirection = point["movedirection"]  # 移向
    movespeed = point["movespeed"]  # 移速
    power = point["power"]  # 风力值
    pressure = point["pressure"]  # 中心气压
    speed = point["speed"]  # 风速
    strong = point["strong"]  # 风力文本
    # time = point["time"]
    # radius10 = point["radius10"]
    # radius12 = point["radius12"]
    # radius7 = point["radius7"]
    # 使用 cursor() 方法创建一个游标对象 cursor
    params = (name, lng, lat, movedirection, movespeed, power, pressure, speed, strong)
    nums = [name, lng, lat, movedirection, movespeed, power, pressure, speed, strong]
    # print(params)
    str = ', '.join(params)
    f = open(file_name, 'a')  # 若文件不存在，系统自动创建。'a'表示可连续写入到文件，保留原内容，在原
    # 内容之后写入。可修改该模式（'w+','w','wb'等）
    f.write(str)  # 将字符串写入文件中
    f.write("\n")  # 换行
