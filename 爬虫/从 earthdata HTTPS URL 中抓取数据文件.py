# coding=utf-8
# -*- codeing = utf-8 -*-
# @Time :2022/11/30 15:11
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  从 earthdata HTTPS URL 中抓取数据文件.py

"""
 该脚本 NSIDC_parse_HTML_BatchDL.py 定义了一个 HTML 解析器，
 用于从 earthdata HTTPS URL 中抓取数据文件，并将所有文件批量下载到您的工作目录。
 此代码改编自  https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python
"""

import os
import sys
import urllib
from urllib import request

cookie_jar = None

if sys.version_info.major == 2:
    from HTMLParser import HTMLParser
    from cookielib import CookieJar

    cookie_jar = CookieJar()
else:
    from html.parser import HTMLParser  # python3
    from http import cookiejar  # python3

    cookie_jar = cookiejar.CookieJar()


# 定义一个自定义的 HTML 解析器来抓取 HTML 数据表的内容
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inLink = False
        self.dataList = []
        self.directory = '/'
        self.indexcol = ';'
        self.Counter = 0

    def handle_starttag(self, tag, attrs):
        self.inLink = False
        if tag == 'table':
            self.Counter += 1
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    if self.directory in value or self.indexcol in value:
                        break
                    else:
                        self.inLink = True
                        self.lasttag = tag

    def handle_endtag(self, tag):
        if tag == 'table':
            self.Counter += 1

    def handle_data(self, data):
        if self.Counter == 1:
            if self.lasttag == 'a' and self.inLink and data.strip():
                self.dataList.append(data)


parser = MyHTMLParser()


# 定义批量下载函数
def BatchJob(Files, cookie_jar):
    for dat in Files:
        print("downloading: ", dat)
        # 如果是python2走这个，否则走下面
        url_dat = url + dat
        if sys.version_info.major == 2:
            import urllib2
            job_request = urllib2.Request(url_dat)
            job_request.add_header('cookie', cookie_jar)  # 将保存的 cookie 传递到其他 HTTP 请求中
            JobRedirect_url = urllib2.urlopen(job_request).geturl() + '&app_type=401'

            # 在修改后的重定向 url 请求资源
            Request = urllib2.Request(JobRedirect_url)
            Response = urllib2.urlopen(Request)
            f = open(dat, 'wb')
            f.write(Response.read())
            f.close()
            Response.close()
        else:
            job_request = urllib.request.Request(url_dat)
            # cookies_dict = requests.utils.dict_from_cookiejar(cookie_jar)
            # cookies_str = json.dumps(cookies_dict)
            # job_request.add_header('cookie', cookies_str)
            urlopen = urllib.request.urlopen(job_request)
            # JobRedirect_url = urlopen.geturl() + '&app_type=401'
            #
            # 在修改后的重定向 url 请求资源
            # Request = urllib.request.Request(JobRedirect_url)
            # Response = urllib.request.urlopen(Request)
            f = open(dat, 'wb')
            f.write(urlopen.read())
            # f.write(Response.read())
            f.close()
            urlopen.close()

    print("Files downloaded to: ", os.path.dirname(os.path.realpath(__file__)))


# ===============================================================================
# 以下代码块用于 HTTPS 身份验证
# ===============================================================================

# 将用于验证数据访问权限的用户凭据
username = "xymeng"
password = "18844120269oooOOO"

# 包含您要批量下载的文件的目录的完整 URL
url = "https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0192_seaice_trends_climo_v3/total-ice-area-extent/nasateam/"

# 创建一个密码管理器来处理从返回的 401 响应
if sys.version_info.major == 2:
    import urllib2

    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
else:

    password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()

password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)

# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.


if sys.version_info.major == 2:
    import urllib2

    opener = urllib2.build_opener(
        urllib2.HTTPBasicAuthHandler(password_manager),
        # urllib2.HTTPHandler(debuglevel=1),    # 取消注释这两行看看
        # urllib2.HTTPSHandler(debuglevel=1),   # 请求响应的详细信息
        urllib2.HTTPCookieProcessor(cookie_jar))
    urllib2.install_opener(opener)
else:

    opener = urllib.request.build_opener(
        urllib.request.HTTPBasicAuthHandler(password_manager),
        # urllib.request.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
        # urllib.request.HTTPSHandler(debuglevel=1),   # details of the requests/responses
        urllib.request.HTTPCookieProcessor(cookie_jar))
    urllib.request.install_opener(opener)

# Create and submit the requests. There are a wide range of exceptions that
# can be thrown here, including HTTPError and URLError. These should be
# caught and handled.

# ===============================================================================
# 打开请求以获取目录中的文件名。打印可选
# ===============================================================================
DirBody = None

if sys.version_info.major == 2:
    import urllib2

    DirRequest = urllib2.Request(url)
    DirResponse = urllib2.urlopen(DirRequest)

    # 获取重定向 url 并附加 'app_type=401' 以执行基本的 http 身份验证
    DirRedirect_url = DirResponse.geturl()
    DirRedirect_url += '&app_type=401'

    # 在修改后的重定向 url 请求资源
    DirRequest = urllib2.Request(DirRedirect_url)
    DirResponse = urllib2.urlopen(DirRequest)
    DirBody = DirResponse.read(DirResponse)


else:
    DirRequest = urllib.request.Request(url)
    DirResponse = urllib.request.urlopen(DirRequest)

    # 获取重定向 url 并附加 'app_type=401' 以执行基本的 http 身份验证
    DirRedirect_url = DirResponse.geturl()
    DirRedirect_url += '&app_type=401'

    # 在修改后的重定向 url 请求资源
    DirRequest = urllib.request.Request(DirRedirect_url)
    DirResponse = urllib.request.urlopen(DirRequest)
    DirBody = DirResponse.read()
    DirBody = DirBody.decode("utf8")

# 使用上面定义的 HTML 解析器打印包含数据的目录的内容
parser.feed(DirBody)
Files = parser.dataList

# 显示在 HTMLParser 类中声明的 python 列表的内容 print Files
# 取消注释以打印文件列表

# ===============================================================================
# 调用函数下载url中所有文件
# ===============================================================================
BatchJob(Files, cookie_jar)  # 注释掉以防止下载到您的工作目录
