# -*- coding: utf-8 -*-
# 主要参考Esir技术支持NetCDF_time_slice_to_raster脚本与MakeNetCDFRasterLayer脚本
# 速度不快，不如matlab
import arcpy  # 导入arcpy（该包为arcgis软件附带！！）
import os
from arcpy.sa import *

pre_filepath = r'D:\datasum\pre\preNc.nc'  # 读取文件夹
pre_OutputFolder = r"D:\dataset\caijiannc\pre"  # 设置tif文件的输出路径
tmp_filepath = r'D:\dataset\tmp'  # 读取文件夹
tmp_OutputFolder = r"D:\dataset\caijiannc\tmp"  # 设置tif文件的输出路径


class NC:
    def __init__(self):
        pass


def NC_toTif(firstname, filepath, OutputFolder, variable):
    file_list = os.listdir(filepath)  # 读取文件夹下所有的文件,我的文件路径之下只有NC文件
    length = len(file_list)
    for i in range(0, length):  # 建立循环
        file = filepath + '/' + file_list[i]
        print(file)
        filename = file_list[i]
        # inNetCDFFile = file
        # variable = "tmp"  # 变量类型，我这里为降水
        XDimension = "lon"  # 读取经纬度
        YDimension = "lat"
        startyear = int(filename[4:8])
        if len(filename) == len('pre_2020.nc'):
            yearnumber = 1
        else:
            yearnumber = 3
        for m in range(0, yearnumber):  # 三年m 0 1 2
            year = str(startyear + m)
            for n in range(1, 13):  # n是月份，1-12
                mouth = str(n)
                outtime = year + 'y' + mouth + 'm'  # 设置输出的文件名，以时间进行命名
                outRasterLayer = outtime
                print(outRasterLayer)
                band = str(m * 12 + n)
                bandDimension = ''
                dimensionValues = 'time' + " " + band  # 设置dimensionValue,格式为"time 1",，所以添加了空格
                print(dimensionValues)
                valueSelectionMethod = "BY_VALUE"  # 如果by index，索引是从0开始的
                # Execute MakeNetCDFRasterLayer
                arcpy.MakeNetCDFRasterLayer_md(file, variable, XDimension, YDimension, outRasterLayer, bandDimension,
                                               dimensionValues, valueSelectionMethod)
                # 导出为tif
                outExtractByMask = ExtractByMask(outRasterLayer, r"D:\datasum\DEM\1984_DEM.tif")

                outtif = OutputFolder + '/' + firstname + outtime + ".tif"
                print(outtif)
                # outExtractByMask.save(outtif)
                # arcpy.CopyRaster_management(outExtractByMask, outtif, background_value=0, pixel_type="32_BIT_FLOAT")
                # arcpy.CopyRaster_management(outRasterLayer, outtif, background_value= 0, pixel_type="32_BIT_FLOAT")
                # 导出tif,设置背景值0为nodata；不同版本arcgis参数情况不同；转为float，没必要double类型，便于接下来转换单位并裁剪研究区
                arcpy.ProjectRaster_management(in_raster=outExtractByMask, out_raster=outtif, \
                                               out_coor_system=r"D:\datasum\DEM\1984_DEM.tif",
                                               resampling_type="BILINEAR",
                                               cell_size='0.00833333333332575'
                                               )


variable = "preSum.tif"
NC_toTif('band', pre_filepath, pre_OutputFolder, variable)
variable = "tmp"
# NC_toTif('tmp',tmp_filepath,tmp_OutputFolder,variable)