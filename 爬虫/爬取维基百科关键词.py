import csv
import logging
import re
import urllib

import cchardet
import requests
from fake_useragent import UserAgent
from flask import Flask
from gerapy_auto_extractor import is_list
from gne import GeneralNewsExtractor
from lxml import etree
from readability import Document

DELETE_SET = ["\r", "\n", "\t"]


class Clearoutside(object):

    def __init__(self):
        self.url = "https://zh.wikipedia.org/wiki/{}"
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
                "accept": "*/*"
            }

    # 请求网站获取url
    # def get_html(self, url) -> str:
    #     # toDo 添加代理，更新反扒
    #     # proxies = {
    #     #     "http": "http://0.0.0.0:7890",
    #     #     "https": "https://0.0.0.0:7890"
    #     # }
    #     # resp = requests.get(url, timeout=8, proxies=proxies, headers=self.headers, allow_redirects=True)
    #     # content = resp.content
    #     response = requests.get(url, headers=self.headers)
    #     html = response.text
    #     # 获取响应字符串编码
    #     encoding = response.apparent_encoding
    #     # 获取字节形式的相应内容并用utf-8格式来解码
    #     # html = response.content.decode(encoding)
    #     return html

    # 请求网站获取url
    def get_html(self, url) -> str:
        # toDo 添加代理，更新反扒
        # proxies = {
        #     "http": "http://0.0.0.0:7890",
        #     "https": "https://0.0.0.0:7890"
        # }
        # resp = requests.get(url, timeout=8, proxies=proxies, headers=self.headers, allow_redirects=True)
        # content = resp.content
        response = requests.get(url, headers=self.headers, timeout=30)
        content = response.content
        # 获取响应字符串编码
        encoding = response.apparent_encoding
        encoding = cchardet.detect(content)['encoding']
        print("=============================================================")
        print(content.decode(encoding, errors="ignore"))
        print("=============================================================")

        return content.decode(encoding, errors="ignore")

    # 将解析后的文件写入csv中
    def writerCsv(self, day, data_dict, lon, lan):
        with open(f'./csv/{day, lon, lan}.csv', 'a', newline='', encoding='utf8') as f:
            csvwriter = csv.writer(f)
            for key, value in data_dict.items():
                csvwriter.writerow([key, value])

    def main(self, keyword):
        url = self.url.format(keyword)
        print("start download html:{}".format(url))
        html = self.get_html(url)
        # TODO 进行数据抽取
        baike_data = self.parse_html(html, "https://zh.wikipedia.org/wiki/")
        # json_baike = json.dumps(baike_data)
        # print(json_baike)
        # return json_baike
        return baike_data

    def _list_parse(self, base_url):
        node = etree.HTML(self)
        node_list = node.xpath('//a[starts-with(@href, "/")]|//a[starts-with(@href, "http")]')
        node_list_lenth = len(node_list)
        if node_list_lenth > 10:
            pre_num = int(node_list_lenth * 0.2)
            bak_num = int(node_list_lenth * 0.7)
            node_list = node_list[pre_num: bak_num]

        total_result = []

        for item in node_list:
            title = item.xpath("./text()")

            format_title = "".join(title).replace("\n", "").replace(" ", "").replace("\t", "").replace("\r",
                                                                                                       "").replace(
                "\t", "")

            if not format_title:
                continue

            url = item.xpath("./@href")
            abs_url = urllib.parse.urljoin(base_url, url[0])
            total_result.append({
                "title": format_title,
                "url": abs_url
            })

        return total_result

    # 解析url，获取数据（单词条解析）
    def parse_html(self, html, base_url):
        content_result = {}
        doc = Document(html)

        # 获取标题
        content_result["title"] = doc.title()

        # 清洗摘要
        summary = doc.summary(html_partial=True).replace("\n", "").replace("\r", "")
        # 去除摘要中特殊字符
        for a in DELETE_SET:
            summary = summary.replace(a, "")
        summary_node = etree.HTML(html)
        etree.strip_tags(summary_node, "div", "img", "a", "html", "body", "svg", "link")
        etree.strip_attributes(summary_node, "href", "src")
        content_result["summary"] = str(etree.tostring(summary_node, encoding="UTF-8"), encoding="utf-8")

        # 清洗正文
        # html_partial 意思是是否过滤掉返回结果中的 html 和 body 标签
        tag_content = doc.summary(html_partial=True)
        clear_content = etree.HTML(tag_content).xpath('string(.)')
        print(clear_content)
        content_result["text"] = clear_content

        list_page = is_list(html, threshold=0.97)
        if not list_page:
            try:
                detail = GeneralNewsExtractor().extract(html, host=base_url)
                content_result.update(detail)

                # 构建此条中图片
                images = detail["images"]
                if not images:
                    detail_node = etree.HTML(tag_content)
                    images = detail_node.xpath("//img/@src")
                new_images = []
                for i in images:
                    if i.startswith("http"):
                        if re.match("(.*jpeg.*|.*png.*|.*jpg.*)", i, re.I | re.M):
                            new_images.append(urllib.parse.urljoin(base_url, i))
                content_result["images"] = new_images
            except Exception as e:
                logging.exception(e)

        # TODO 进行列表抽取
        # list_result = _list_parse(html, host)
        # total_result["list"] = list_result

        return content_result


app = Flask(__name__)  # 创建flask实例


@app.route("/spider/<string:keyword>")
def spider(keyword):
    spider = Clearoutside()
    json_baike = spider.main(keyword)
    return json_baike


@app.route("/")
def hello():
    return " hello word"


if __name__ == '__main__':
    # 启动flask，提供http接口
    # 如果是docker部署，需要注意ip指定为0.0.0.0，flask默认ip为127.0.0.1，docker启动时，无法在宿主机访问！！
    app.run(host="0.0.0.0", port=int("8000"))
