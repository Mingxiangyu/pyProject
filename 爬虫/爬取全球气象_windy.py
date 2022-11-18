import base64
import csv
import json

import requests
from fake_useragent import UserAgent
from flask import Flask


class Clearoutside(object):

    def __init__(self):
        self.url = "https://node.windy.com/Zm9yZWNhc3Q/ZWNtd2Y/"
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
        """
        日期和时刻 data.origDate
        温度 data.temp
        降雨 data.mm
        风速 data.wind
        风向 data.windDir
        露点 data.dewPoint
        阵风 data.gust
        气压 data.pressure
        相对湿度 data.rh
        雨量， data.rain 单位 ml
        """
        print(html)
        pass

    # 将解析后的文件写入csv中
    def writer_csv(self, day, data_dict, lon, lan):
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
                path = "point/ecmwf/v2.7/{}/{}?"
                # 添加经纬度
                path = path.format(lan_start, lon_start)
                print(path)
                # 构建请求后续
                path_suf = "source=detail&step=3&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
                           ".eyJpYXQiOjE2NTcxNTg0OTYsImluZiI6eyJpcCI6IjU4LjE3Ny4xNTcuMTU0IiwidWEiOiJNb3ppbGxhXC81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXRcLzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZVwvMTAwLjAuNDg5Ni43NSBTYWZhcmlcLzUzNy4zNiJ9LCJleHAiOjE2NTczMzEyOTZ9.j0iPybI-z7twpoS29LeVGKUzAmVHbRAd4M3vrFmP7zQ&token2=pending&uid=921cfb71-1e7d-5f80-4399-86a4d8ca92a3&sc=22&pr=1&v=36.0.0&poc=102 "
                url_path = path + path_suf
                # 进行字符串转字节，否则base64没法运行
                url_path = url_path.encode()
                base64_url_path_buf = base64.b64encode(url_path)
                base64_url_path = base64_url_path_buf.decode('utf-8', errors='ignore')
                print("decoded text is \n" + base64_url_path)

                url = self.url + base64_url_path
                # 获取网站base64加密后的响应结果
                html = self.get_html(url)
                decode_html = base64.b64decode(html)
                data = json.loads(decode_html)
                print(data)

                day_data_list = self.parse_html(data)
                # print(day_data_list)
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
