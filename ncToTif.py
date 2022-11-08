import glob
import os

import netCDF4 as nc
import numpy as np
from osgeo import gdal, osr


def nc2tif(data, Output_folder):
    tmp_data = nc.Dataset(data)  # 利用.Dataset()方法读取nc数据
    print('tmp_data', tmp_data)

    Lat_data = tmp_data.variables['lat'][:]
    Lon_data = tmp_data.variables['lon'][:]
    # print(Lat_data)
    # print(Lon_data)

    tmp_arr = np.asarray(tmp_data.variables['temp'])

    # 影像的左上角&右下角坐标
    Lonmin, Latmax, Lonmax, Latmin = [Lon_data.min(), Lat_data.max(), Lon_data.max(), Lat_data.min()]
    # print(Lonmin, Latmax, Lonmax, Latmin)

    # 分辨率计算
    Num_lat = len(Lat_data)  # 5146
    Num_lon = len(Lon_data)  # 7849
    Lat_res = (Latmax - Latmin) / (float(Num_lat) - 1)
    Lon_res = (Lonmax - Lonmin) / (float(Num_lon) - 1)
    # print(Num_lat, Num_lon)
    # print(Lat_res, Lon_res)

    for i in range(len(tmp_arr[:])):
        # i=0,1,2,3,4,5,6,7,8,9,...
        # 创建tif文件
        driver = gdal.GetDriverByName('GTiff')
        out_tif_name = Output_folder + '\\' + data.split('\\')[-1].split('.')[0] + '_' + str(i + 1) + '.tif'
        out_tif = driver.Create(out_tif_name, Num_lon, Num_lat, 1, gdal.GDT_Int16)

        # 设置影像的显示范围
        # Lat_re前需要添加负号
        geotransform = (Lonmin, Lon_res, 0.0, Latmax, 0.0, -Lat_res)
        out_tif.SetGeoTransform(geotransform)

        # 定义投影
        prj = osr.SpatialReference()
        prj.ImportFromEPSG(4326)  # WGS84
        out_tif.SetProjection(prj.ExportToWkt())

        # 数据导出
        out_tif.GetRasterBand(1).WriteArray(tmp_arr[i])  # 将数据写入内存，此时没有写入到硬盘
        out_tif.FlushCache()  # 将数据写入到硬盘
        out_tif = None  # 关闭tif文件


def main():
    Input_folder = r"F:\mxy\department\国遥\数据\Modis\ladsweb"
    Output_folder = r"C:\Users\DELL\Downloads\to"

    # 读取所有数据
    os.chdir(Input_folder)
    data_list = glob.glob("*.nc")
    print(f"该文件夹下有" + str(len(data_list)))
    print(data_list)

    for i in range(len(data_list)):
        data = data_list[i]
        nc2tif(data, Output_folder)
        print(data + '转tif成功')


main()


def NC_to_tiffs(data, Output_folder):
    nc_data_obj = nc.Dataset(data)
    Lon = nc_data_obj.variables['lon'][:]
    Lat = nc_data_obj.variables['lat'][:]
    ndvi_arr = np.asarray(nc_data_obj.variables['temp'])
    ndvi_arr_float = ndvi_arr.astype(float) / 10000  # 之间
    # 影像的左上角和右下角坐标
    LonMin, LatMax, LonMax, LatMin = [Lon.min(), Lat.max(), Lon.max(), Lat.min()]
    # 分辨率计算
    N_Lat = len(Lat)
    N_Lon = len(Lon)
    Lon_Res = (LonMax - LonMin) / (float(N_Lon) - 1)
    Lat_Res = (LatMax - LatMin) / (float(N_Lat) - 1)
    for i in range(len(ndvi_arr[:])):
        driver = gdal.GetDriverByName('GTiff')
        out_tif_name = Output_folder + '\\' + data.split('\\')[-1].split('.')[0] + '_' + str(i + 1) + '.tif'
        out_tif = driver.Create(out_tif_name, N_Lon, N_Lat, 1, gdal.GDT_Float32)

        geotransform = (LonMin, Lon_Res, 0, LatMax, 0, -Lat_Res)
        out_tif.SetGeoTransform(geotransform)

        srs = osr.SpatialReference()
        srs.ImportFromEPSG(4326)
        out_tif.SetProjection(srs.ExportToWkt())
        # 数据写出
        out_tif.GetRasterBand(1).WriteArray(ndvi_arr_float[i][::-1])  # 将数据写入内存，此时没有写入硬盘 此处[::-1]用于图像的垂直镜像对称，避免图像颠倒
        out_tif.FlushCache()  # 将数据写入硬盘
        out_tif = None  # 注意必须关闭tif文件
