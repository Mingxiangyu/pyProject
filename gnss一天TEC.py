# -*- coding: utf-8 -*-
# @Time    : 2022/1/3 14:21
# @Author  : xymeng
# @FileName: 001.py 绘制TEC等值线专用程序
# @Link    : 原文链接：https://blog.csdn.net/absll/article/details/127837253
# @Software: PyCharm

import os

import matplotlib.pyplot as plt
import numpy as np

'''
store the lat,lon,and,TEC value
'''
lat = []
lon = []
TEC0 = []
TEC = []
TEC2D = np.zeros(shape=(71, 73))
picnum = 1
timenum = 1
folder = r'C:\Users\zhouhuilin\Desktop\test'

'''
Search for each ionex file
'''

for ifile in os.listdir(folder):
    '''
    num: Record the count of the region 记录区域计数
    count: Record the count of the Map 记录Map的计数
    '''
    num = 1
    count = 1
    timenum = 0
    path = os.path.join(folder, ifile)
    print(path)
    if not path.endswith("i"):
        continue
    with open(path) as ionex:
        icontent0 = ionex.readlines()
        print(type(icontent0))
        for i in range(len(icontent0)):
            '''
            Turn list including other symbol into list only consisting of character
            将包含其他符号的列表转换为仅包含字符的列表
            '''
            icontent1 = icontent0[i].split(' ')
            for x in range(icontent1.count('')):
                icontent1.remove('')
            if len(icontent1) >= 5:
                if icontent1[-1] == 'LAT/LON1/LON2/DLON/H\n' and num <= 71 and count <= 13:
                    Lon0 = -180.0
                    Lat0 = 90
                    deltla = 2.5
                    deltlo = 5
                    Lat0 = Lat0 - (deltla * num)
                    lat.append(Lat0)

                    num = num + 1
                    '''
                    Begin putting TEC value into TSC list
                    开始将 TEC 值放入 TSC 列表
                    '''
                    ynum = 0

                    for y in range(1, 6):
                        tecvalue1 = icontent0[i + y].split(' ')
                        for z in range(tecvalue1.count('')):
                            tecvalue1.remove('')
                        for lo in range(len(tecvalue1)):
                            if num == 2:
                                lon.append(Lon0)
                            TEC2D[num - 2][ynum] = int(tecvalue1[lo])
                            ynum = ynum + 1
                            Lon0 = Lon0 + deltlo
                    if num >= 72:
                        timenum = timenum + 1
                        LON, LAT = np.meshgrid(lon, lat)
                        plt.figure()
                        plt.contourf(LON, LAT, TEC2D, 8, cmap='plasma')
                        C = plt.contour(LON, LAT, TEC2D, 8, cmap='plasma')
                        # 添加标记，标记处不显示轮廓线，颜色为黑色，保留两位小数
                        plt.clabel(C, inline=True, colors='k', fmt='%1.2f')
                        path = 'F:/contour-outcome' + '/' + str(picnum) + '/'
                        if not os.path.exists(path):  # 如果不存在路径，则创建这个路径
                            os.makedirs(path)
                        print(path)
                        plt.savefig(path + '/' + str(timenum) + '.jpg')
                        plt.close()
                        num = 1
                        count = count + 1
                        lon.clear()
                        lat.clear()
                        TEC = list(TEC)
                        TEC.clear()
                        TEC2D = np.zeros(shape=(71, 73))

    picnum = picnum + 1
    lon.clear()
    lat.clear()
    TEC.clear()
    TEC2D = np.zeros(shape=(71, 73))
