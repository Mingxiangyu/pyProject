# -*- codeing = utf-8 -*-
# @Time :2022/11/29 16:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载电离层格网文件.py
import hashlib
import json
import os
import time

import requests
from lxml import etree
from requests import utils

SaveDir = "D:\RS_data\GNSS"

"""
正确下载链接
https://cddis.nasa.gov/archive/gnss/products/ionex/2022/007/igsg0070.22i.Z
"""


# overriding requests.Session.rebuild_auth to mantain headers when redirected
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # Overrides from the library to keep headers when redirected to or from
    # the NASA auth host.
    def rebuild_auth(self, prepared_request, response):
        headers = prepared_request.headers
        url = prepared_request.url
        if 'Authorization' in headers:
            original_parsed = requests.utils.urlparse(response.request.url)
            redirect_parsed = requests.utils.urlparse(url)
            if (original_parsed.hostname != redirect_parsed.hostname) \
                    and redirect_parsed.hostname != self.AUTH_HOST \
                    and original_parsed.hostname != self.AUTH_HOST:
                del headers['Authorization']
        return


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
        self.url = "https://cddis.nasa.gov/archive/gnss/products/ionex/{}/{}/igsg{}0.{}i.Z"
        self.username = 'xymeng'  # 个人账户信息及密码
        self.password = '18844120269oooOOO'
        self.session = SessionWithHeaderRedirection(self.username, self.password)
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
        self.cookie = self.getCookie()

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
    def download(self, url, out):
        # toDo 添加代理，更新反扒
        print("下载时url为：" + url)
        try:
            # 手动设置cookie
            # http_cookie = "_ga=GA1.4.481246173.1668751269; urs_guid_ops=59ebdaa8-a5d1-4fdf-b239-cfc272bf5d9a; _ga_WXLRFJLP5B=GS1.1.1669018357.1.1.1669018937.0.0.0; _ga_KQRB4LHBVM=GS1.1.1669178700.2.0.1669178700.0.0.0; _ga_GPQT4GL86Z=GS1.1.1669178700.2.0.1669179000.0.0.0; _gid=GA1.2.38923508.1669612982; _gid=GA1.4.38923508.1669612982; _ga_RLWG0EH56X=GS1.1.1669712745.8.1.1669713568.0.0.0; _ga_EG7FB6W5DL=GS1.1.1669713571.4.1.1669716573.0.0.0; _ga_76MJEEGE07=GS1.1.1669716894.1.1.1669717150.0.0.0; _gat_UA-62340125-2=1; _gat_GSA_ENOR0=1; _urs-gui_session=ab66c1b30d002262686c4b104d5d849c; _ga=GA1.1.481246173.1668751269; _ga_T0WYSFJPBT=GS1.1.1669776021.11.1.1669776479.0.0.0"
            # cookie = {item.split('=')[0]: item.split('=')[1] for item in http_cookie.split('; ')}
            # response = requests.get(url, headers=self.headers, timeout=30, cookies=cookie)

            # 模拟登录获取cookie
            # cookie = self.cookie
            # response = self.session.get(url, headers=self.headers, timeout=30, cookies=cookie)

            response = self.session.get(url, headers=self.headers, timeout=30)

            # 在出现 http 错误时引发异常
            response.raise_for_status()

            with open(out, "wb") as code:
                # requests.get(url)默认是下载在内存中的，下载完成才存到硬盘上，可以用Response.iter_content来边下载边存硬盘
                for chunk in response.iter_content(chunk_size=1024):
                    code.write(chunk)
        except requests.exceptions.HTTPError as e:
            print(e)

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
