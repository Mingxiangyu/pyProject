# -*- codeing = utf-8 -*-
# @Time :2022/11/29 15:58
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://blog.csdn.net/u013598957/article/details/118493249
# @File :  login.py
import time

import requests
from lxml import etree
from requests import utils

'''
1.每一次访问登录页面，token都会更新
2.如果先在earthdata正页登录，进入产品页面还需走确认登录流程
'''


class Login:
    def __init__(self):
        self.headers1 = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3"}
        self.headers2 = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
            'Referer': 'https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD11A1--6/2021-02-22..2021-03-08/DB/97,30.1,107.1,21.2',
            'Host': 'ladsweb.modaps.eosdis.nasa.gov',
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'}
        self.login_url = 'https://urs.earthdata.nasa.gov'
        self.post_url = 'https://urs.earthdata.nasa.gov/login'
        # 测试用的logined_url
        # self.logined_url = 'https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product=MOD11A1&collection=6&dateRanges=2021-02-22..2021-03-08&areaOfInterest=x97y30,x107y21&dayCoverage=true&dnboundCoverage=true'
        self.logined_url = 'https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD09/2013/002/MOD09.A2013002.0735.006.2015253193455.hdf'
        self.session = requests.Session()  # 神奇，会话处理Cookie
        self.username = 'xymeng'  # 个人账户信息及密码
        self.password = '18844120269oooOOO'

    def token(self):
        response = self.session.get(self.login_url, headers=self.headers1, timeout=30)  # 可能会被封ip
        print('准备获取token')
        selector = etree.HTML(response.text)
        token = selector.xpath('//*[@id="login"]/input[2]/@value')[0]  # 日了，获取属性不用text()
        print('token: ' + str(token) + '\n')
        return token

    def getCookie(self):
        pass

    def login(self, cookie={}):
        post_data = {
            'commit': 'Log in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'username': self.username,
            'password': self.password,
        }  # 'redirect_uri': self.logined_url

        response = self.session.post(self.post_url, data=post_data, headers=self.headers1)  # 模拟登录
        print('模拟登录成功！\n')

        cookie = response.cookies  # 里面有首次登录得到的Set-Cookie
        cookie = utils.dict_from_cookiejar(cookie)
        print(cookie)
        print(type(cookie))
        print('\n')
        time.sleep(1)

        response = self.session.get(self.logined_url, headers=self.headers2, timeout=30, cookies=cookie)
        time.sleep(1)
        # if response.status_code == 200:
        #     # 这里response headers里没看到cookie
        #     self.getHdf(response, cookie)


if __name__ == '__main__':
    log = Login()
    log.login()
