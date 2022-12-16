import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import unlzw3

unlzw = unlzw3.unlzw(Path("/Users/ming/Downloads/AFG_rrd/igsg0070.22i.Z"))
# print(unlzw)
decode = unlzw.decode('utf-8')
# print(decode)
icontent0 = decode.split('\n')
# print(icontent0)
num = 1
count = 1
timenum = 0
lat = []
lon = []
TEC0 = []
TEC = []
TEC2D = np.zeros(shape=(71, 73))
picnum = 1

print(type(icontent0))
for i in range(len(icontent0)):
    '''
    Turn list including other symbol into list only consisting of character
    '''
    icontent1 = icontent0[i].split(' ')
    for x in range(icontent1.count('')):
        icontent1.remove('')
    if len(icontent1) >= 5:
        if icontent1[-1] == 'LAT/LON1/LON2/DLON/H' and num <= 71 and count <= 13:
            Lon0 = -180.0
            Lat0 = 90
            deltla = 2.5
            deltlo = 5
            Lat0 = Lat0 - (deltla * num)
            lat.append(Lat0)

            num = num + 1
            '''
            Begin putting TEC value into TSC list
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
