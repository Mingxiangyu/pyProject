# -*- codeing = utf-8 -*-
# @Time :2022/11/29 16:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载电离层格网文件.py
import hashlib
import json
import os

import requests
from fake_useragent import UserAgent
from lxml import etree
from requests import utils

SaveDir = "D:\RS_data\GNSS"

"""
正确下载链接
https://cddis.nasa.gov/archive/gnss/products/ionex/2022/007/igsg0070.22i.Z
"""


def get_file_md5_top10m(file_name):
    """
    根据前10兆计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()  # 创建md5对象
    with open(file_name, 'rb') as fobj:
        data = fobj.read(1024 * 1024 * 10)
        m.update(data)  # 更新md5对象
    return m.hexdigest()  # 返回md5对象


class gnssDownload(object):
    def __init__(self):
        self.login_url = 'https://urs.earthdata.nasa.gov'
        self.post_url = 'https://urs.earthdata.nasa.gov/login'
        # 测试用的logined_url
        # url = https://cddis.nasa.gov/archive/gnss/products/ionex/2021/004/igsg0040.21i.Z
        self.url = "https://cddis.nasa.gov/archive/gnss/products/ionex/{}/{}/igsg{}0.{}i.Z"
        self.session = requests.Session()  # 神奇，会话处理Cookie
        self.username = 'xymeng'  # 个人账户信息及密码
        self.password = '18844120269oooOOO'
        # 产生随机的User - Agent请求头进行访问
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 30):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }
        self.cookie = self.getCookie()

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers, timeout=30)  # 可能会被封ip
        print('准备获取token')
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="login"]/input[2]/@value')[0]
        print('token: ' + str(token) + '\n')
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
        print('模拟登录成功！\n')

        cookie = response.cookies  # 里面有首次登录得到的Set-Cookie
        cookie = utils.dict_from_cookiejar(cookie)
        print(cookie)
        print(type(cookie))
        print('\n')
        self.cookie = cookie
        return cookie

    # 请求网站获取url
    def download(self, url, out):
        # toDo 添加代理，更新反扒
        print("下载时url为：" + url)
        cookie = self.cookie
        response = self.session.get(self.url, headers=self.headers, timeout=30, cookies=cookie)
        with open(out, "wb") as code:
            # requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content来边下载边存硬盘
            for chunk in response.iter_content(chunk_size=1024):
                code.write(chunk)
            # code.write(response.content)

    def main(self, year, start_date_day, end_date_day):
        for day in range(start_date_day, end_date_day):
            day = str(day)
            day = day.zfill(3)
            year_suf = str(year)[-2:]
            url = self.url.format(year, day, day, year_suf)

            # 构建业务数据
            data = {
                # todo 添加数据来源、文件指纹
            }

            # 数据下载
            if not os.path.exists(SaveDir):
                os.makedirs(SaveDir)
            file_name = url.split('/')[-1]
            path = os.path.join(SaveDir, file_name)

            # 这一步判断本地是否存在该文件，如果不存在就下载，存在的话就跳过
            if not os.path.exists(path):
                print('downloading: ', path)
                self.download(url, path)
            else:
                # 如果存在，但是字节数为空，则重新下载 todo 如果字节数对应不上网站对数据的描述，是不是也可以重新下载
                if not os.path.getsize(path):
                    print('downloading: ', path)
                    self.download(url, path)
                else:
                    print('skipping: ', path)

            file_md5 = get_file_md5_top10m(path)
            print("数据md5为：" + file_md5)
            data["id"] = file_md5

            data_json = json.dumps(data)

            with open(SaveDir + "/" + "md5" + ".gnssjson", "wb") as f:
                # 写文件用bytes而不是str，所以要转码
                f.write(bytes(data_json, "utf-8"))


if __name__ == '__main__':
    spider = gnssDownload()
    year = 2022
    start_date_day = 1
    end_date_day = 10
    spider.main(year, start_date_day, end_date_day)
