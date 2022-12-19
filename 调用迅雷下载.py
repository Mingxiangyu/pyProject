# -*- codeing = utf-8 -*-
# @Time :2022/12/19 17:47
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :https://blog.csdn.net/for_syq/article/details/105747145
# @File :  调用迅雷下载.py
import os
import time

save_path = 'D:\Download'  # 下载文件储存路径


def read():  # 读取url.txt中的下载名称，和url
    with open('url.txt', 'r')as f:
        url = [url.replace('\t', '').replace('\n', '') for url in f.readlines()]
        sum = []
        for i in url:
            num = {}
            name = str(i).rsplit('http://')[0]
            url = 'http://' + str(i).rsplit('http://')[-1]
            num['name'] = name
            num['url'] = url
            num['number'] = str(url).rsplit('/')[-1]
            sum.append(num)
        return sum


def check_start(file_name):  # 判断文件是否开始下载
    tmp = file_name + '.xltd.cfg'
    return os.path.exists(os.path.join(save_path, tmp))


def check_end(fiename):  # 检查文件是否下载成功
    return os.path.exists(os.path.join(save_path, fiename))


def download(name, url, number):  # 下载文件
    os.system(r'""D:\Program Files (x86)\Thunder Network\Thunder\Program\ThunderStart.exe"" {url}'.format(
        url=url))  # 迅雷ThunderStart.exe的路径
    time.sleep(10)
    print("正在下载 {}".format(name))
    if check_start(number):
        while True:
            time.sleep(2)
            if check_end(number):
                return True
    else:
        return False


def run():
    print("=======视频自动下载程序启动=========")
    sum = read()
    for i in sum:
        if os.path.exists(os.path.join(save_path, '\\' + str(i['name']) + '.' + str(i['number']).rsplit('.')[-1])):
            continue
        download(i['name'], i['url'], i['number'])
        # print("======下载完成======")
        try:
            if os.path.exists(os.path.join(save_path, i['number'])):
                os.rename(os.path.join(save_path, i['number']),
                          save_path + '\\' + str(i['name']) + '.' + str(i['number']).rsplit('.')[-1])
                print("======下载完成======", end='\n')
        except EnvironmentError as f:
            print(f)


run()
