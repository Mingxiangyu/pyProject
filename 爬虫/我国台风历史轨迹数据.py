# -*- codeing = utf-8 -*-
# @Time :2022/11/18 14:28
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://blog.csdn.net/qazwsxpy/article/details/127427409
# 原文链接：https://www.heywhale.com/api/notebooks/62ea6d2ef145d47a93d25a5a/RenderedContent?cellcomment=1
# @File :  我国台风历史轨迹数据.py

import datetime
# 导入模块
import json
import os
import urllib.request

import xlwt

os.makedirs('./typhoon')

# 设置浏览器参数
headers = {'Connection': 'Keep-Alive',
           'Accept': 'text/html, application/xhtml+xml, */*',
           'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
           'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

for year in range(2019, 2020):
    for num in range(1, 30):
        try:
            number = str(year) + str(num).zfill(2)
            chaper_url = 'http://data.istrongcloud.com/v2/data/complex/' + number + '.json'
            req = urllib.request.Request(url=chaper_url, headers=headers)
            data = urllib.request.urlopen(req).read()
            data = json.loads(data)[0]

            f = xlwt.Workbook(encoding='utf-8')
            sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
            sheet1.write(0, 0, '台风编号')
            sheet1.write(0, 1, '中文名称')
            sheet1.write(0, 2, '英文名称')
            sheet1.write(0, 3, '时刻')
            sheet1.write(0, 4, '经度')
            sheet1.write(0, 5, '纬度')
            sheet1.write(0, 6, '强度等级')
            sheet1.write(0, 7, '气压')
            sheet1.write(0, 8, '风速')
            sheet1.write(0, 9, '风级')
            sheet1.write(0, 10, '移速')
            sheet1.write(0, 11, '移向')

            sheet1.write(0, 12, 'radius7')
            sheet1.write(0, 13, 'radius10')
            sheet1.write(0, 14, 'radius12')
            sheet1.write(0, 15, 'ne_7')
            sheet1.write(0, 16, 'se_7')
            sheet1.write(0, 17, 'sw_7')
            sheet1.write(0, 18, 'nw_7')
            sheet1.write(0, 19, 'ne_10')
            sheet1.write(0, 20, 'se_10')
            sheet1.write(0, 21, 'sw_10')
            sheet1.write(0, 22, 'nw_10')
            sheet1.write(0, 23, 'ne_12')
            sheet1.write(0, 24, 'se_12')
            sheet1.write(0, 25, 'sw_12')
            sheet1.write(0, 26, 'nw_12')

            for i in range(0, len(data['points'])):
                sheet1.write(i + 1, 0, data['tfbh'])
                sheet1.write(i + 1, 1, data['name'])
                sheet1.write(i + 1, 2, data['ename'])
                sheet1.write(i + 1, 3, str(datetime.datetime.strptime(data['points'][i]['time'], '%Y-%m-%dT%H:%M:%S')))
                sheet1.write(i + 1, 4, data['points'][i]['lat'])
                sheet1.write(i + 1, 5, data['points'][i]['lng'])
                sheet1.write(i + 1, 6, data['points'][i]['strong'])
                sheet1.write(i + 1, 7, data['points'][i]['pressure'])
                sheet1.write(i + 1, 8, data['points'][i]['speed'])
                sheet1.write(i + 1, 9, data['points'][i]['power'])
                sheet1.write(i + 1, 10, data['points'][i]['move_speed'])
                sheet1.write(i + 1, 11, data['points'][i]['move_dir'])

                sheet1.write(i + 1, 12, data['points'][i]['radius7'])
                sheet1.write(i + 1, 13, data['points'][i]['radius10'])
                sheet1.write(i + 1, 14, data['points'][i]['radius12'])
                if data['points'][i]['radius7_quad'] != 'null':
                    sheet1.write(i + 1, 15, data['points'][i]['radius7_quad']['ne'])
                    sheet1.write(i + 1, 16, data['points'][i]['radius7_quad']['se'])
                    sheet1.write(i + 1, 17, data['points'][i]['radius7_quad']['sw'])
                    sheet1.write(i + 1, 18, data['points'][i]['radius7_quad']['nw'])
                else:
                    sheet1.write(i + 1, 15, 'NaN')
                    sheet1.write(i + 1, 16, 'NaN')
                    sheet1.write(i + 1, 17, 'NaN')
                    sheet1.write(i + 1, 18, 'NaN')
                if data['points'][i]['radius10_quad'] != 'null':
                    sheet1.write(i + 1, 19, data['points'][i]['radius10_quad']['ne'])
                    sheet1.write(i + 1, 20, data['points'][i]['radius10_quad']['se'])
                    sheet1.write(i + 1, 21, data['points'][i]['radius10_quad']['sw'])
                    sheet1.write(i + 1, 22, data['points'][i]['radius10_quad']['nw'])
                else:
                    sheet1.write(i + 1, 19, 'NaN')
                    sheet1.write(i + 1, 20, 'NaN')
                    sheet1.write(i + 1, 21, 'NaN')
                    sheet1.write(i + 1, 22, 'NaN')
                if data['points'][i]['radius12_quad'] != 'null':
                    sheet1.write(i + 1, 23, data['points'][i]['radius12_quad']['ne'])
                    sheet1.write(i + 1, 24, data['points'][i]['radius12_quad']['se'])
                    sheet1.write(i + 1, 25, data['points'][i]['radius12_quad']['sw'])
                    sheet1.write(i + 1, 26, data['points'][i]['radius12_quad']['nw'])
                else:
                    sheet1.write(i + 1, 23, 'NaN')
                    sheet1.write(i + 1, 24, 'NaN')
                    sheet1.write(i + 1, 25, 'NaN')
                    sheet1.write(i + 1, 26, 'NaN')

            f.save('typhoon/' + number + '.xls')
            print(number + '.xls 已下载')
        except:
            break
