# -*- codeing = utf-8 -*-
# @Time :2022/11/30 18:10
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  使用 cookiejar 自动获取登录后获得的cookie.py
"""
获取个人中心的页面
1.代码登录 登录成功 cookie（有效）
2.自动带着cookie去请求个人中心
cookiejar自动保存cookie
"""
import urllib.parse
import urllib.request
from http import cookiejar

# 添加cookie也要有cookie的处理器
# get：返回登录页面
# post：返回登录后的结果，账户已经登录进去了的页面

#  1.代码登录
# 1.1 登录的网址
login_url = "https://www.yaozh.com/login"
# 1.2 登录的参数
# Form Data
login_form_data = {
    "username": "dong123456",
    "pwd": "******",
    "formhash": "892EF2A017",
    "backurl": "https%253A%252F%252Fwww.yaozh.com%252F"
}
# 使用urllib.request时  post方法所携带的参数不能是字典形式
login_form_data_final = urllib.parse.urlencode(login_form_data)
# 1.3 发送登录请求POST，
# 自动保存cookie
cook_jar = cookiejar.CookieJar()
# 定义有添加 cookie功能的处理器
cook_handler = urllib.request.HTTPCookieProcessor(cook_jar)
# 根据处理器生成opener
opener = urllib.request.build_opener(cook_handler)
# 带着参数发送post请求,制作请求对象
# 添加请求头
headers = {
    "Users-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
}
# 此时headers里面还没有cookie，还没有登录
login_request = urllib.request.Request(login_url, headers=headers, data=login_form_data_final.encode("utf-8"))
# 如果登录成功。cookjar自动保存cookie，opener里面有cookjar，所以opener里有cookie
# 下面一步不需要返回数据，只要成功登陆就行
opener.open(login_request)

#  2.代码带着cookie去访问 个人中心
center_url = "http://www.yaozh.com/member/"
center_request = urllib.request.Request(center_url, headers=headers)
response = opener.open(center_url)
data = response.read()
with open("cookie_02.html", "wb") as f:
    f.write(data)
