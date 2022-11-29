# -*- codeing = utf-8 -*-
# @Time :2022/11/29 15:57
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://blog.csdn.net/u013598957/article/details/118493249
# @File :  nasa_moids.py
import datetime
import json
import os
import random
import time

import requests
from dateutil.relativedelta import relativedelta

import autoClick

__author__ = 'Ray'

'''
Task：输入产品信息，附加筛选条件，自动爬取Modis遥感数据

观察/记录：
    1.数据一般延时更新，且所选区域在部分日期下没有数据
    2.仅hdf所在URL需要cookies，所以应模拟登录获取Cookies（其实短期内Cookies不变，如果不要求过高，可以手动输入Cookies）
    3.要用到中间URL，找规律

Tips：
    1.网络事先需要连接好，并保持稳定，否则不只会影响模拟点击。（看到一种说法是借助浏览器厂商差异，换FireFox，还未尝试）
    2.Modis网站的服务器运行状况良好
    3.解决访问时间过长，模拟点击报错问题!（循环尝试？）,下载URL卡死问题
    4.目前的访问和下载速度较慢，考虑异步，多线程下载或其他方式
    5.ban，代理池，访问频率（考虑要不要定期清除Cookie）
    6.符合使用需求
    7.后续维护问题，观察网站变化，也要靠考虑浏览器版本升级与驱动的兼容
'''


class Nasa:  # 面向对象编程，创建类
    def __init__(self):
        self.headers1 = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
            'Referer': 'https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD11A1--6/2021-02-22..2021-03-08/DB/97,30.1,107.1,21.2',
            'Host': 'ladsweb.modaps.eosdis.nasa.gov',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'}
        # 还未修改Referer!!
        # 留意下headers会不会变化
        # 当遇到403时，headers的内容越全越有希望，除了在get()方法中添加cookies参数，也可以在headers字典中添加cookies
        self.headers2 = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"}

    # 获取当前日期范围
    def getDate(self, if_range='last month', range=20):
        # example: '2021-02-22..2021-03-08'
        date = time.strftime('%Y-%m-%d', time.localtime())

        # 如果是范围筛选，还要考虑年份和月份的灵活变化
        if if_range == 'all':
            date = '2020-01-01..' + date
        else:
            date = str(datetime.date.today() + relativedelta(days=-30)) + '..' + str(date)

        print('Date range:' + str(date) + '\n')
        return date

    # 获取页面
    def getPage(self, url, cookie=None):
        try:
            re = requests.get(url, headers=self.headers1, timeout=(9.05, 6.05), cookies=cookie)
            print('已完成get指令')
            print(re.status_code)
            re.raise_for_status()
            re.encoding = re.apparent_encoding
            print('获取页面成功！准备return')
            # time.sleep(1)
            return re
        except requests.exceptions.RequestException as e:
            print(e)
            print('请求失败！您的网络状况可能存在一点问题，需重试')

    # 将开发者工具界面中，Headers里显示的cookie转换为字典
    def cookieToDict(self, cookie):
        cookie = cookie.split(';')
        cok = dict()
        for i in cookie:
            part = i.split('=')
            part[0] = part[0].strip(' ')
            cok[part[0]] = part[1]
        return cok

    # 通过间接爬取，下载数据文件
    def getHdf(self, data_kind, date_ranges, area, cookie):
        for kind in data_kind:
            url1 = 'https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product={}&collection={}&dateRanges={}&areaOfInterest={}&dayCoverage=true&dnboundCoverage=true'.format(
                data_kind[kind][0], data_kind[kind][1], date_ranges, area)
            url2_head = 'https://ladsweb.modaps.eosdis.nasa.gov'

            # 获取hdf的URL字段
            while True:
                try:
                    re = nasa.getPage(url1)
                    # print('str:\n' + re.text[:500] + '\n')  # 测试而已
                    text = json.loads(re.text, strict=False)
                    # text = re.json()
                    print(text)
                    print('\n')
                    file_url = []  # 存储fileURL的列表,每一个元素包括fileURL和对应日期

                    for i in text:
                        j = text[i]
                        f_url = j.get('fileURL')  # 神奇的地方，这里一开始用正常键值对访问，只有fileURL会显示KeyError
                        f_date = j.get('start').split(' ')[0]
                        file_url.append((f_url, f_date))

                    # 浏览器页面最多只能显示两千条数据，但是url1里会包含所有数据的url2
                    print(file_url)
                    file_length = len(file_url)
                    print('Length of hdf files:' + str(file_length) + '\n')
                    break

                except:
                    print('尝试爬取file URL失败，可能原因如下：1.url已更新；（2.cookies有误或失效；）3.网页json已更新')

            # 保持下载状态，这里指下载全部文件的一个周期
            while True:
                count = 1
                downloaded = 0
                skip = 0
                root = 'upload/'

                # 解决新的防卡死问题,考虑headers问题
                for i in file_url:
                    try:
                        path = root + i[1] + '/' + kind
                        if not os.path.exists(path):  # 如果文件目录不存在
                            os.makedirs(path)  # os.mkdir()只能创建一级目录，而os.makedirs()可以创建多级目录

                        url2 = url2_head + i[0]
                        filepath = path + url2.split("/")[-1]
                        if os.path.exists(filepath):
                            print(str(count) + '.文件已存在\n')
                            count += 1
                            skip += 1
                            continue

                        re = nasa.getPage(url2, cookie)
                        hdf = re.content
                        print(str(count) + '.已获取下载目标，准备下载')
                        with open(filepath, 'wb') as f:
                            f.write(hdf)
                            print('下载完成！\n')
                            f.close()
                            downloaded += 1
                    except:
                        print("下载第" + str(count) + "个文件失败，原因可能是连接出错\n")

                    count += 1
                    time.sleep(random.uniform(3, 4.5))

                if downloaded + skip >= file_length:
                    break
                # 遍历完一遍下载页面URL，长时间休眠一次
                time.sleep(random.uniform(480, 720))


# 获取访问下载URL时Request Headers中的Cookie
def getCookie(driver_path, date_range, area_of_interest, username, password):
    auto = autoClick.GetCookie(driver_path, date_range, area_of_interest, username, password)
    cookie = auto.autoClick()
    print('已获取cookie')

    # 整合得到Request Headers中的Cookie
    request_cookie = dict()
    for i in cookie:
        request_cookie[i['name']] = i['value']
    assert (request_cookie != {})
    print(request_cookie)
    return request_cookie


if __name__ == '__main__':
    # nasa = Nasa()
    # date = nasa.getDate()
    # area1 = '97,30,107,21'
    # path = "chromedriver.exe"
    # user = '......'  # 个人账户及密码信息！
    # code = '......'
    # kind = {'upload/Surface temperature/': ['MOD11A1', 6],
    #         'upload/Terra surface reflectance/': ['MOD09A1', 61]}
    # area2 = 'x97y30,x107y21'  # 文件url信息所在的url中，area信息格式与产品交互页面不同
    # cookie = ''
    #
    # # 暂定每天爬取1次Cookie，3次遥感数据
    # while True:
    #     if (datetime.datetime.now().hour == 0) and (datetime.datetime.now().minute == 00):
    #         cookie = getCookie(path, date, area1, user, code)
    #         time.sleep(3)
    #         nasa.getHdf(kind, date, area2, cookie)
    #         time.sleep(300)
    #         # 考虑计时任务
    #
    #     if datetime.datetime.now().hour == 4 or datetime.datetime.now().hour == 8:
    #         if datetime.datetime.now().minute == 00:
    #             nasa.getHdf(kind, date, area2, cookie)
    #             time.sleep(600)

    nasa = Nasa()
    date = nasa.getDate()
    area = '97,30,107,21'

    path = "chromedriver.exe"
    user = '......'  # 个人账户及密码信息！
    code = '......'

    cookie = getCookie(path, date, area, user, code)
    time.sleep(3)

    kind = {'Surface temperature/': ['MOD11A1', 6], 'Terra surface reflectance/': ['MOD09A1', 61]}  # 后续维护问题，观察网站变化
    area = 'x97y30,x107y21'  # 文件url信息所在的url中，area信息格式与产品交互页面不同
    nasa.getHdf(kind, date, area, cookie)

'''
知识笔记：
在爬虫中，有时候处理需要登录才能访问的页面时，我们一般会直接将登录成功后获得的Cookies
放在请求头里面直接请求，一般不必重新登录（如果Cookies稳定不变）。

当浏览器下一次请求该网站时，浏览器会把此Cookies放到请求头一起提交给服务器，
Cookies携带了会话ID信息，服务器检查它即可找到对应的会话，再对其判断以辨认用户状态

如果传给服务器的Cookies无效，或者会话过期，则不能继续访问页面。

因此，Cookies需与对话配合，一个处于客户端，一个处于服务端。

每次通过HTTP协议访问一个资源的时候，浏览器都会自动在请求的header中加入你在这个域名下的所有cookies。
服务器在收到请求后可以根据是否有cookies以及cookies的值来判断你的身份，从而返回不同的资源。
（在登陆页面登陆后，服务器会会给你分配一个cookie，并放入返回的response的header中。
你的浏览器会储存这个cookie并在每次访问这个网站时都加入request的header中。
同时，服务器也会对给你分配的cookie的值进行配对存储，这样就能通过你的cookie过得你的身份了。）

当遇到403时，headers的内容越全越有希望，除了在get()方法中添加cookies参数，也可以在headers字典中添加cookies。

- 模拟登录：
    （requests.Session()可以维持一个会话，并且自动处理Cookies）
    1.利用网页开发工具,勾选preserve log；

    2.清空Cookies，初次登陆，一般是查看Network里的第一个请求，观察Request Headers 
    和 Form Data里的独特信息，他们就是模拟登录需要的信息;
    同时，也可以看到登陆后Response Headers中会有一个Set-Cookie，一般会与其他Cookie有关;

    3.退出登录，清空Cookies，回到登录页面，
    在Elements里找token。其他信息一般也可以通过这两项获得；

    4.终极：selenium模拟浏览器登录后（能否先seesion登录），先尝试获取Cookies。

- 模拟点击：
    需用代码精确模拟使用浏览器时的一系列操作。注意精确！

'''
