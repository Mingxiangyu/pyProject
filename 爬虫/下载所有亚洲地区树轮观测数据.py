# -*- codeing = utf-8 -*-
# @Time :2022/11/22 16:51
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://blog.csdn.net/weixin_42590927/article/details/123312335
# @File :  下载所有亚洲地区树轮观测数据.py


import re
import urllib.request

from bs4 import BeautifulSoup

TR_url = 'https://www1.ncdc.noaa.gov/pub/data/paleo/treering/measurements/asia/'
my_url = urllib.request.urlopen(TR_url).read().decode('ascii')

soup = BeautifulSoup(my_url, 'lxml')

url_list = soup.find_all(href=re.compile(".rwl"))
print('step1 has fininshed!')

urls = []
for i in url_list[1:]:
    urls.append('https://www1.ncdc.noaa.gov/pub/data/paleo/treering/measurements/asia/' + i.get('href'))
print('step2 has finished!')

for i, url in enumerate(urls):
    file_name = "D:\my_data\climate_factor_data\ASM_domain/tree_ring\Asia_all_NOAA/" + url.split('/')[-1]
    urllib.request.urlretrieve(url, file_name)

print('congratulations! you got them all!')
