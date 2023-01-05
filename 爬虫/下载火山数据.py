# -*- codeing = utf-8 -*-
# @Time :2022/11/29 16:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载电离层格网文件.py
import json
import time

import requests
from lxml import etree
from requests import utils

"""
正确下载链接
https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/volcanoes
"""


class volcanoDownload(object):
    def __init__(self):
        self.url = "https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/volcanoes"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/88.0.4324.190 Safari/537.36 "
        }

        # 产生随机的User - Agent请求头进行访问
        # ua = UserAgent(verify_ssl=False)
        # for i in range(1, 30):
        #     self.headers = {
        #         'User-Agent': ua.random
        #     }

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers, timeout=30)  # 可能会被封ip
        print('准备获取token')
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="login"]/input[2]/@value')[0]
        print('token: ' + str(token) + '\n')
        '''
        下面是另一种处理获取token
        :param html:
        return: 获取csrftoken
        '''
        # soup = BeautifulSoup(response.text, 'html.parser')
        # res = soup.find("input", attrs={"name": "authenticity_token"})
        # token = res["value"]
        return token

    def getCookie(self):
        post_data = {
            'commit': 'Log in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'username': self.username,
            'password': self.password,
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)  # 模拟登录
        if (response.status_code == 200):
            print('模拟登录成功！\n')
            time.sleep(5)

        cookie = response.cookies  # 里面有首次登录得到的Set-Cookie
        cookie = utils.dict_from_cookiejar(cookie)
        # print(cookie)
        return cookie

    # 请求网站获取url
    def download(self, url):
        # toDo 添加代理，更新反扒
        print("下载时url为：" + url)
        try:

            response = requests.get(url, headers=self.headers, timeout=30)

            # 在出现 http 错误时引发异常
            response.raise_for_status()

            html = response.text
            # volcano_json = json.dumps(html)
            return html

        except requests.exceptions.HTTPError as e:
            print(e)

    def main(self):

        # 构建业务数据
        data = {
            # todo 添加数据来源、文件指纹
        }

        download = self.download(self.url)
        # print(download)




        list_ = []
        loads = json.loads(download)
        print(type(loads))
        load = loads["items"]
        for v in load:
            a = {}
            a["name"] = v.get("name")
            a["year"] = v.get("year")
            a["location"] = v.get("location")
            a["country"] = v.get("country")
            a["latitude"] = v.get("latitude")
            a["longitude"] = v.get("longitude")
            a["status"] = v.get("status")
            a["deathsTotal"] = v.get("deathsTotal")
            list_.append(a)
        dumps = json.dumps(list_)
        print(dumps)


if __name__ == '__main__':
    spider = volcanoDownload()
    spider.main()
