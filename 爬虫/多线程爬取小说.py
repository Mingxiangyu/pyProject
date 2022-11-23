# -*- codeing = utf-8 -*-
# @Time :2022/11/20 15:21
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  多线程爬取小说.py
import os
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from lxml import etree

# ---------------------------------------------------------------------------------
# 支持站点：
# 八一中文网（81zw.com）
# 顶点小说（23usp.com）
# 笔趣阁（bqg.org，qbiqu.com，52bqg.net等全部站点）
# 天籁小说（xs.23sk.com）
# --------------------------------------------------------------------------------
if not os.path.exists('./缓存'):  # 创建缓存文件夹来存放抓取的每一章节文件
    os.mkdir('./缓存')
else:  # 如不存在则创建文件夹，如存在则清空再创建
    shutil.rmtree('./缓存')
    os.mkdir('./缓存')
url = 'https://www.23usp.com/xs_1511/'
# url='https://www.81zw.com/book/40352/'
# url='https://www.bqg.org/2_2977/'
# url='https://www.qbiqu.com/0_1/'
# url='https://www.52bqg.net/book_99524/'
# url='https://xs.23sk.com/files/article/html/22/22295/'
reg = '(https://.*?)\/'
if '23usp' in url or '81zw' in url or '23sk' in url:
    homeUrl = re.findall(reg, url, re.S)[0]
else:
    homeUrl = url
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0'
}


def choiceCode(homeUrl):
    if '23usp' in homeUrl or '23sk' in homeUrl:  # 转码，否则有乱码
        return 'gbk'
    elif '81zw' in homeUrl:
        return 'utf-8'
    else:
        return 'GB2312'


homePage = requests.get(url=url, headers=headers)  # 抓取主页面html数据
homePage.encoding = choiceCode(homeUrl)  # 转码
tree = etree.HTML(homePage.text)
zhangJie_list = tree.xpath('//dd//a/@href')  # 获取每一章的页面相对地址
title = tree.xpath('//h1/text()')[0]  # 获取小说名字
zjNameList = []
zhangJie_list = list(set(zhangJie_list))  # 去重
for u in zhangJie_list:  # 每一章的URL地址中提取一串数字作为存储每一章的文件名
    zhangjietxtname = u.split('/')[-1].split('.')[0]
    zjNameList.append(int(zhangjietxtname))
zjNameList.sort()  # 章节排序


def downtxt(url):  # 下载每一章的函数
    zhangjie_url = homeUrl + url
    txtName = url.split('/')[-1].split('.')[0]  # 获取每一章URL地址中的一串数字作为文件名字
    if os.path.exists('./缓存/{}.txt'.format(txtName)):  # 创建缓存文件夹来存放抓取的每一章节文件
        print(zhangjie_url, "\n 已采集，执行下一个")
    else:  # 如不存在则创建文件夹，如存在则清空再创建
        try:
            zhangjie_sourse = requests.get(url=zhangjie_url, headers=headers)
            zhangjie_true = None
        except:
            for i in range(6):
                time.sleep(5)
                try:
                    zhangjie_sourse = requests.get(url=zhangjie_url, headers=headers)
                    zhangjie_true = None
                    break  # 如果没出错跳出循环，否则继续循环
                except:
                    i += 1
                    print(url + ' ' * 10 + '第%s下载失败' % i)

            if zhangjie_true != None:
                with open('./错误网址.txt', 'a', encoding='utf-8') as f:
                    f.write(url + '\n')
                print(url + ' ' * 10 + '下载失败')
                # pass
        if zhangjie_true == None:
            zhangjie_sourse.encoding = choiceCode(homeUrl)  # 章节页面内容转码
            zhangjie_sourse = zhangjie_sourse.text
            tree = etree.HTML(zhangjie_sourse)
            title = tree.xpath('//h1/text()')[0]  # 获取每一章名字
            txt = tree.xpath('//div[@id="content"]/text()')  # 获取每一章文本内容
            with open('./缓存/{}.txt'.format(txtName), 'w', encoding='UTF-8') as f:
                f.write('\n' + title + '\n')  # 保存章节名字到文本文件
                for line in txt:  # 保存章节内容到文本文件，循环保存每一行
                    f.write(line)
                print(title + ' ' * 10 + '下载成功')
        else:
            print(url + ' ' * 10 + '下载失败')


def combine_txt():  # 合并所有章节文件函数
    with open('./{}.txt'.format(title), 'a', encoding='utf-8') as f:
        for txt in zjNameList:  # 循环打开缓存中每一章的内容保存到新的文件中
            path = './缓存/{}.txt'.format(txt)  # 设置存放路径
            content = open(path, 'r', encoding='utf-8').read()  # 打开每章节文件
            f.write(content)
            os.remove(path)


def mistake_txt():
    with open('./错误网址.txt', 'w+', encoding='utf-8') as f:
        ff = f.readlines()
        ii = len(ff)
        print("共{}条数据。".format(ii))
        print("-" * 30)
        if ii > 0:
            i = 1
            for line in ff:
                print("下面采集第 {} 条数据。".format(i))
                downtxt(line)
                i += 1
            print("错误网址已经采集完毕！")
        else:
            print("你没有、没有出错网址！")
        print("-" * 30)


with ThreadPoolExecutor(15) as Pool:  # 使用线程池，设置15个线程，可修改
    Pool.map(downtxt, zhangJie_list)
print('！！！下载完毕，开始检查有没有错漏章节，请稍等。。。！！！')
mistake_txt()
print('！！！下载完毕，开始合并，请稍等。。。！！！')
combine_txt()  # 执行合并函数
os.removedirs('./缓存')
print('！！！全部完成！！！！')
