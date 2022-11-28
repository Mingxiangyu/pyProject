# -*- codeing = utf-8 -*-
# @Time :2022/11/28 17:53
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://wap.sciencenet.cn/blog-3367669-1191430.html?mobile=1
# @File :  下载Modis等卫星数据.py
import os
import time
from netrc import netrc

import requests

saveDir = ""
# 登录的授权文件路径，如果想省事也可以将你的requests的auth直接添加你的账户名和密码： request.get(...,auth=('username','password'),...)
netrcDir = ""
# 待下载数据的下载链接
f = ''
# 数据的存在位置saveDir = 'C:\\Users\\YchZhu\\Downloads'# 数据的保存名称：和数据下载名称一致
saveName = os.path.join(saveDir, f.split('/')[-1].strip())  # 授权信息的存放路径netrcDir = os.path.expanduser("~\.netrc")
# 带授权的网址
urs = 'Earthdata Login'  # Earthdata URL to call for authentication
# Create and submit request and download file
with requests.get(f.strip(), stream=True,
                  auth=(netrc(netrcDir).authenticators(urs)[0], netrc(netrcDir).authenticators(urs)[2])) as response:
    if response.status_code != 200:
        print("{} not downloaded. Verify that your username and password are correct in {}")
    else:
        start = time.time()  # 开始时间
        size = 0  # data of download
        content_size = int(response.headers['Content-Length'])  # 总大小
        print('file size:' + str(content_size) + ' bytes')
        print('[文件大小]：%0.2f MB' % (content_size / 1024 / 1024))

        response.raw.decode_content = True
        content = response.raw
        with open(saveName, 'wb') as d:
            while True:
                chunk = content.read(16 * 1024)
                if not chunk:
                    break
                d.write(chunk)
                size += len(chunk)  # 已下载数据大小
                # 显示下载进度条
                print(
                    '\r' + '[下载进度]：%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end='')

        print('Downloaded file: {}'.format(saveName))
        end = time.time()  # 结束时间
        print('\n' + "全部下载完成！用时%0.2f秒" % (end - start))
