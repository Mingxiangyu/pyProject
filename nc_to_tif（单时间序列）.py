# -*- coding: utf-8 -*-
import glob
import os
import shutil

import netCDF4 as nc
import numpy as np
from osgeo import gdal, osr


def NC_to_tiffs(data, out_path):
    '''
    这个函数里面有些地方还是可能需要更改
    coord(坐标系)
    '''
    coord = 4326  # 坐标系，["EPSG","4326"]，默认为4326
    nc_data_obj = nc.Dataset(data)
    # print(nc_data_obj,type(nc_data_obj)) #了解nc数据的数据类型，<class 'netCDF4._netCDF4.Dataset'>
    # print(nc_data_obj.variables)          #了解nc数据的基本信息
    key = list(nc_data_obj.variables.keys())  # 获取时间，经度，纬度，波段的名称信息，这些可能是不一样的
    print('基础属性为', key)
    lon_size = [i for i, x in enumerate(key) if (x.find('lon'.upper()) != -1 or x.find('lon'.lower()) != -1)][
        0]  # 模糊查找属于经度的名称，还在更新.....
    lat_size = [i for i, x in enumerate(key) if (x.find('lat'.upper()) != -1 or x.find('lat'.lower()) != -1)][
        0]  # 模糊查找属于纬度的名称，还在更新.....
    key_band = key[len(key) - 1]  # 获取波段的名称     目前发现都是放在最后
    key_lon = key[lon_size]  # 获取经度的名称
    key_lat = key[lat_size]  # 获取纬度的名称
    Lon = nc_data_obj.variables[key_lon][:]  # 获取每个像元的经度,类型为数组
    Lat = nc_data_obj.variables[key_lat][:]  # 获取每个像元的纬度，类型为数组
    Band = np.asarray(nc_data_obj.variables[key_band])  # 获取对应波段的像元的值，类型为数组
    # 影像的四个角的坐标
    LonMin, LatMax, LonMax, LatMin = [Lon.min(), Lat.max(), Lon.max(), Lat.min()]

    # 分辨率计算
    N_Lat = len(Lat)
    N_Lon = len(Lon[0])
    Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)
    Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)

    # 创建.tif文件
    driver = gdal.GetDriverByName('GTiff')
    out_tif_name = out_path + os.sep + data.split('\\')[-1][:-3] + '.tif'
    out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)

    # 设置影像的显示范围
    # -Lat_Res一定要是-的
    geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
    out_tif.SetGeoTransform(geotransform)

    # 获取地理坐标系统信息，用于选取需要的地理坐标系统
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(coord)  # 定义输出的坐标系为"WGS 84"，AUTHORITY["EPSG","4326"]
    out_tif.SetProjection(srs.ExportToWkt())  # 给新建图层赋予投影信息

    # 更改异常值
    Band[Band[:, :] > 100000] = -32767

    # 数据写出
    if Band.ndim == 2:  # 如果本来就是二维数组就不变
        a = Band[:, :]
    else:  # 将三维数组转为二维
        a = Band[0, :, :]
    reversed_arr = a[::-1]  # 这里是需要倒置一下的        #这个很重要！！！！！！
    out_tif.GetRasterBand(1).WriteArray(reversed_arr)
    out_tif.GetRasterBand(1).SetNoDataValue(-32767)
    out_tif.FlushCache()  # 将数据写入硬盘
    del out_tif  # 注意必须关闭tif文件


def nc_to_tif(Input_folder):
    Output_folder = os.path.split(Input_folder)[0] + os.sep + 'out_' + os.path.split(Input_folder)[1]
    # 读取所有nc数据
    data_list = glob.glob(Input_folder + os.sep + '*.nc')
    print("输入位置为: ", Input_folder)
    print("被读取的nc文件有：", data_list)
    #     if not os.path.isdir(Output_folder):
    if os.path.exists(Output_folder):
        shutil.rmtree(Output_folder)  # 如果文件夹存在就删除
    os.makedirs(Output_folder)  # 再重建，这样就不用运行之后又要删了之后再运行了
    for i in range(len(data_list)):
        dat = data_list[i]
        NC_to_tiffs(data=dat, out_path=Output_folder)
        print(dat + '-----转tif成功')
    print(f"输入位置为: {Input_folder}")
    print("--------------------------")
    print(f'输出位置为: {Output_folder}')


'''#用户需要输入 ：nc文件所放的文件夹的路径，默认输出至同一上级目录中'''

nc_to_tif(Input_folder=r'D:\nc\real\T2')