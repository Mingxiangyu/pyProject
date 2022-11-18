# -*- codeing = utf-8 -*-
# @Time :2022/11/18 15:21
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://blog.csdn.net/qazwsxpy/article/details/127427409
# 原文链接：https://www.heywhale.com/mw/project/61ae12a83c18f70018b5947a
# @File :  天气雷达基本反射率图像下载.py
import os
import urllib.request
import warnings

import pandas as pd
from PIL import Image

warnings.filterwarnings('ignore')

d = {'全国': 'ACHN', '东北': 'ANEC', '华北': 'ANCN', '西北': 'ANWC', '西南': 'ASWC', '华中': 'ACCN', '华东': 'AECN', '华南': 'ASCN'}

timelist = pd.date_range(start='2021-07-20 08:00:00', end='2021-07-20 11:00:00', freq='6min')


def download_radar_img(time, region, savepath):
    headers = {'User-Agent': 'Mozilla/5.0 3578.98 Safari/537.36'}

    if region == '全国':
        base_url = 'http://image.data.cma.cn/vis/RAD__B0_CR/'
    else:
        base_url = 'http://image.data.cma.cn/vis/RADA_L3_MST_REF_PNG_' + d[region] + '/'

    img_url = base_url + str(time.year) + '/' + str(time.month).zfill(2) + '/' + str(time.day).zfill(
        2) + '/' + 'Z_RADA_C_BABJ_' \
              + time.strftime('%Y%m%d%H%M%S') + '_P_DOR_RDCP_R_' + d[region] + '.PNG'

    request = urllib.request.Request(img_url, headers=headers)

    try:
        response = urllib.request.urlopen(request)
        img_name = img_url.split('/')[-1]
        filename = savepath + img_name
        if (response.getcode() == 200):
            with open(filename, "wb") as f:
                f.write(response.read())  # 将内容写入图片
            return filename
    except:
        return "failed"


for time in timelist:
    download_radar_img(time, '华北', 'E:/Users/project')

imgFiles = [fn for fn in os.listdir('E:/Users/project') if fn.endswith('.PNG')]
imgFiles.sort()
print(imgFiles)

# 合成GIF图像
images = [Image.open('E:/Users' + fn) for fn in imgFiles]
im = images[0]
filename = 'test.gif'
im.save(fp=filename, format='gif', save_all=True, append_images=images[1:], duration=100)
