# -*- codeing = utf-8 -*-
# @Time :2022/11/28 18:14
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://blog.csdn.net/LSH1628340121/article/details/126058913
# @File :  利用from data的数据提交账号密码.py
import requests

session = requests.session()
url = "https://passport.17k.com/ck/user/login"

data = {
    "loginName": "你的账号",
    "password": "你的密码"
}
session.post(url, data=data)
resp = session.get("https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919")
print(resp.json())
