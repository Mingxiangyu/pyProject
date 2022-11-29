# -*- codeing = utf-8 -*-
# @Time :2022/11/28 18:13
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://blog.csdn.net/LSH1628340121/article/details/126058913
# @File :  利用Cookie实现登陆.py
import requests

headers = {
    "Cookie": "你登陆后网页的Cookie"
}
url = 'https://user.17k.com/ck/author/shelf?page=1&appKey=2406394919'
response = requests.get(url,headers=headers)
response.encoding = 'utf-8'
print(response.json())
