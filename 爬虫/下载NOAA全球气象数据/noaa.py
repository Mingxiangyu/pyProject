# -*- coding: utf-8 -*-
# @Time        : 2021/12/29 15:58
# @Author      : Liuym
# @Email       : 274670459@qq.com
# @File        : noaa.py
# @Project     : noaa
# @Description : 主程序

import csv
import os
import tarfile

import pymysql
import requests
from config import *
from lxml import etree
from toolbox import BaiduMap

db = pymysql.connect(host=HOST, user=USER, passwd=PASSWORD, db=DB, charset=CHARSET)
cursor = db.cursor()

class Noaa(object):
    def __init__(self):
        self.baidu_api = BaiduMap(BD_AK)
    
    # 下载压缩文件方法
    def _download_tar_gz(self,url):
        # tar_gz_url = 'https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/'
        tar_gz_url = url
        headers = {'User-Agent': 'M'}
        resp= requests.get(tar_gz_url,headers=headers)
        tar_gz_resp_text = resp.text
        tar_gz_etree_element = etree.HTML(tar_gz_resp_text)
        tar_gz_url_xpath = tar_gz_etree_element.xpath('//*/table/tr/td/a')
        # print(tar_gz_url_xpath)
        # print(tar_gz_url[1].xpath('@href'))
        for tar_gz in tar_gz_url_xpath[1:]:
            # 打印要下载的文件名
            # print(tar_gz.xpath('@href')[0])
            requests_url = tar_gz_url + tar_gz.xpath('@href')[0]
            file_name = tar_gz.xpath('@href')[0]
            # 打印拼接以后的下载链接
            # print(requests_url)
            r = requests.get(requests_url)
            # 如果当前文件夹没有tar_gz目录则创建该目录
            if 'tar_gz' not in [x for x in os.listdir('.') if os.path.isdir(x)]:
                try:
                    os.mkdir('tar_gz')
                except:
                    print('创建文件夹失败')
            # 如果在目录tar_gz下已经有文件了则不重复下载,否则下载
            if file_name in [x for x in os.listdir('tar_gz')]:
                print('%s文件已下载'%(file_name))
            else:
            # 通过拼接的下载url下载文件
                with open(f'tar_gz/{file_name}', "wb") as code:
                    code.write(r.content)
                    print('下载文件%s成功'%(file_name))

    # 接压缩方法，传递参数为文件名以及解压的文件夹
    def untar(self,fname, dirs):
        t = tarfile.open(fname)
        t.extractall(path = dirs)
        

    # 解压下载的气象信息压缩文件,例如1929.tar.gz解压至文件夹tar_gz/1929下
    def _decomp_tar_gz(self):
        for tar_gz_file in os.listdir('tar_gz'):
            # print(tar_gz_file)
            tar_gz_dir = tar_gz_file.split('.')[0]
            if os.path.isfile(f'tar_gz/{tar_gz_file}'):
                self.untar(f'tar_gz/{tar_gz_file}',f'tar_gz/{tar_gz_dir}')
                print('文件%s解压成功'%(f'tar_gz/{tar_gz_file}'))

    # 插入数据库方法，传递csv文件路径然后解析csv文件往MySQL数据库插入数据
    def insert_data_from_csv(self,csv_file):
        f = csv.reader(open(csv_file,'r'))
        for i in f:
            if i[0] == "STATION":
                continue
            sql = 'insert into data values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        
            try:
                cursor.execute(sql,list(i[n] for n in range(28)))
                db.commit()
            except:
                print('插入数据错误')

    # 从解压后的文件夹查找csv文件然后调用插入数据库方法插入数据
    def insert_data(self):
        # 遍历文件夹
        for tar_gz_dir in os.listdir('tar_gz'):
            # 如果是文件夹则为解压缩以后的文件夹，然后再次遍历文件夹，排除压缩文件tar.gz
            if os.path.isdir(f'tar_gz/{tar_gz_dir}'):
                for tar_gz_file in os.listdir(f'tar_gz/{tar_gz_dir}'):
                    # 如果csv文件是5开头的则代表是中国的气象站则插入，否则忽略
                    if f'tar_gz/{tar_gz_dir}/{tar_gz_file}'.split('/')[2][0] == '5':
                        print('是中国的气象站网数据库插入数据%s'%(f'tar_gz/{tar_gz_dir}/{tar_gz_file}'))
                        self.insert_data_from_csv(f'tar_gz/{tar_gz_dir}/{tar_gz_file}')
                    else:
                        print('外国气象站数据不处理')

    # 插入气象站站点信息，首先从data表取出站点的id,去掉重复的station数据只保留1条
    # 然后循环取结果的第3,4条数据经纬度代入百度api取获取国家，省份，城市，县城信息，然后插入info表
    def insert_station_info(self):
        station_number = cursor.execute('select * from data group by station having count(station)>1')
        station_result = cursor.fetchall()
        for i in station_result:  
            #print(baidu_api.get_location(i[2],i[3]))
            sql = 'insert into info values(%s, %s, %s, %s, %s, %s, %s, %s)'
            values = [i[0],i[5],i[2],i[3],self.baidu_api.get_location(i[2],i[3])['country'],self.baidu_api.get_location(i[2],i[3])['province'],self.baidu_api.get_location(i[2],i[3])['city'],self.baidu_api.get_location(i[2],i[3])['district']]
            try:
                cursor.execute(sql,values)
                db.commit()
            except pymysql.err.IntegrityError:
                print('主键重复,该数据已存在')
            except:
                print('插入数据错误')
# 初始化
app = Noaa()
# 在当前文件夹下创建文件夹tar_gz下载气象信息压缩文件
app._download_tar_gz('https://www.ncei.noaa.gov/data/global-summary-of-the-day/archive/')
# 把下载的压缩文件解压成csv文件
app._decomp_tar_gz()
# 通过解压的csv文件把数据插入MySQL数据库,只插入气象站开头为5的中国气象站
app.insert_data()
# 通过百度api插入站点中文信息
app.insert_station_info()