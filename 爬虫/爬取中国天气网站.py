# -*- codeing = utf-8 -*-
# @Time :2023/1/12 11:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://www.cnblogs.com/linfangnan/p/15521967.html
# @File :  爬取中国天气网站.py
import json

import requests
import xlwt

url = "http://d1.weather.com.cn/calendar_new/2023/101230201_202301.html"
headers = {
    "Referer": "http://www.weather.com.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
}
r = requests.get(url=url, headers=headers)
print("请求的状态是：" + str(r.status_code))
if r.status_code == 200:
    content = r.content.decode(encoding='utf-8')
    weathers = json.loads(content[11:])

    writebook = xlwt.Workbook()
    sheet = writebook.add_sheet('Sheet1')
    keys = ['date', 'nlyf', 'nl', 'w1', 'wd1', 'max', 'min', 'jq', 't1', 'hmax', 'hmin', 'hgl', 'alins', 'als']
    for i in range(len(keys)):
        sheet.write(0, i, keys[i])
    for i in range(len(weathers)):
        for j in range(len(keys)):
            sheet.write(i + 1, j, weathers[i][keys[j]])

    writebook.save('weathers.xls')
