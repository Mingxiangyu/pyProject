import csv

import requests
from fake_useragent import UserAgent
from flask import Flask
from lxml import etree


class Clearoutside(object):

    def __init__(self):
        self.url = "https://clearoutside.com/forecast/{}/{}"
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }

    # 请求网站获取url
    def get_html(self, url) -> str:
        # toDo 添加代理，更新反扒
        response = requests.get(url, headers=self.headers)
        html = response.text
        return html

    # 解析url，获取数据
    def parse_html(self, html):
        target = etree.HTML(html)

        day_list = target.xpath('//div[@id="forecast"]/div')
        # print(f"日期列表长度为：{len(day_list)}")

        # 声明返回字典，key为日期，value为数剧
        day_data_dict = {}

        # 获取每天的所有数据
        for i in range(len(day_list)):
            day = None
            # 数据字典，key为数据类型，value为数据值列表
            data_dict = {}

            # 获取当天的div列表
            day_data_list = day_list[i].xpath('./div')
            print(f"day_data_list长度有：{len(day_data_list)}")

            # 当天日期
            for day_data in day_data_list:
                # 获取class属性，判断当前div为那个标签
                day_data_class_list = day_data.xpath("./@class")
                # print(f"当前div标签class属性为：{day_data_class_list}")
                day_data_class = None
                # 如果class属性不为空，则取第一个值（也只有第一个值）
                if day_data_class_list:
                    day_data_class = day_data_class_list[0]
                # 获取日期 toDO 后续fc_day_date改为变量
                if day_data_class == "fc_day_date":
                    day = str(day_data.xpath("./text()")[0])
                    # print(f"当前日期为：{day},类型为{type(day)}")
                # 获取小时列表
                elif day_data_class == "fc_hours fc_hour_ratings":
                    hour_list = day_data.xpath("./ul/li/text()")
                    # print(f"小时列表为：{type(hour_list)},{len(hour_list)}")
                    # 将当地时间列表也放入字典中 toDO 后续可能需要进行时区转换
                    data_dict["hour_list"] = hour_list
                # 获取数据
                elif day_data_class == "fc_detail hidden-xs":
                    div_list = day_data.xpath("./div")
                    # 获取div数据列表 循环遍历获取每一类型
                    for div in div_list:
                        # 字典key为该数据类型（云量，风速等）
                        div_data_type = div.xpath("./span/span/text()")[0]
                        # print(f"该行类别为：{div_data_type}")

                        # 字典value为该数据集合
                        div_data_list = div.xpath("./div/ul/li/text()")
                        # print(f"数据列表类型为：{type(div_data_list)},长度为：{len(div_data_list)}")
                        data_dict[div_data_type] = div_data_list
                    print(data_dict)

            day_data_dict[day] = data_dict
        return day_data_dict

    # 将解析后的文件写入csv中
    def writerCsv(self, day, data_dict, lon, lan):
        with open(f'./csv/{day, lon, lan}.csv', 'a', newline='', encoding='utf8') as f:
            csvwriter = csv.writer(f)
            for key, value in data_dict.items():
                csvwriter.writerow([key, value])

    def main(self, lon_start, lon_end, lan_start, lan_end):
        # TOdo 将已采集过的经纬度+时间持久化，避免重复采集
        # 经纬度步进值
        step_value = 1
        # 经度初始值
        # lon_start = 20
        # 经度结束值
        # lon_end = 21
        while lon_start < lon_end:
            # 纬度初始值
            # lan_start = 120
            # 纬度结束值
            # lan_end = 121
            while lan_start < lan_end:
                url = self.url.format(lon_start, lan_start)
                print("start download html:{}".format(url))
                html = self.get_html(url)
                day_data_list = self.parse_html(html)
                print(day_data_list)
                for day_data_key, day_data_value in day_data_list.items():
                    self.writerCsv(day_data_key, day_data_value, lon_start, lan_start)
                # 纬度步进值
                lan_start += step_value
            # 经度步进值
            lon_start += step_value


app = Flask(__name__)  # 创建flask实例

@app.route("/spider/<float:lon_start>/<float:lon_end>/<float:lan_start>/<float:lan_end>")
def spider(lon_start, lon_end, lan_start, lan_end):
    spider = Clearoutside()
    spider.main(lon_start, lon_end, lan_start, lan_end)
    return "hello,world"


if __name__ == '__main__':
    # 启动flask，提供http接口
    app.run()
