# -*- codeing = utf-8 -*-
# @Time :2022/11/29 18:15
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
# @File :  配置连接以从支持 Earthdata 登录的服务器下载数据.py

import requests


# overriding requests.Session.rebuild_auth to mantain headers when redirected
class SessionWithHeaderRedirection(requests.Session):
    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):
        super().__init__()
        self.auth = (username, password)

    # 从库中覆盖以在重定向到 NASA 身份验证主机或从 NASA 身份验证主机重定向时保留标头。
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


# 使用将用于验证数据访问权限的用户凭据创建会话
username = "xymeng"
password = "18844120269oooOOO"
session = SessionWithHeaderRedirection(username, password)

# 我们希望检索的文件的 URL
url = "https://cddis.nasa.gov/archive/gnss/products/ionex/2021/004/igsg0040.21i.Z"
# url = "https://e4ftl01.cr.usgs.gov/MOLA/MYD17A3H.006/2002.01.01/MYD17A3H.A2002001.h13v13.006.2015153201337.hdf.xml"

# 从保存文件时要使用的 url 中提取文件名
filename = url[url.rfind('/') + 1:]

try:
    # 使用会话提交请求
    response = session.get(url, stream=True)
    print(response.status_code)

    # 在出现 http 错误时引发异常
    response.raise_for_status()

    # save the file
    with open(filename, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=1024 * 1024):
            fd.write(chunk)
except requests.exceptions.HTTPError as e:
    # handle any errors here
    print(e)
