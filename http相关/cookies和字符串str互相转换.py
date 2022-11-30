# -*- codeing = utf-8 -*-
# @Time :2022/11/30 18:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link:https://blog.csdn.net/qq_15603633/article/details/124972822
# @File :  cookies和字符串str互相转换.py
import json

import requests.utils


def save_cookies(files_path, _data):
    """" 保存cookies成文件
    files_path： 文件保存路径
    _data: 需要保存的参数
    """
    f = open(files_path, 'w', encoding='utf-8')
    cookies_dict = requests.utils.dict_from_cookiejar(_data)
    cookies_str = json.dumps(cookies_dict)
    f.write(cookies_str)
    f.close()
    print("----------保存成功--------------")


def get_cookies(files_path):
    """" 读取txt文件并还原cookies """
    with open(files_path, encoding='utf-8') as file:
        cookies_str = file.read()
        cookies_dict = json.loads(cookies_str)
        cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    return cookies
