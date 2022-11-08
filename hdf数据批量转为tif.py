import glob
import os

from osgeo import gdal

#  gdal打开hdf数据集
os.chdir(r"F:\mxy\department\国遥\数据\Modis\ladsweb")
file_list = glob.glob("*.hdf")
for i in file_list:
    datasets = gdal.Open(i)
    #  获取hdf中的子数据集
    SubDatasets = datasets.GetSubDatasets()
    Metadata = datasets.GetMetadata()
    #  打印元数据
    for key, value in Metadata.items():
        print('{key}:{value}'.format(key=key, value=value))
    #  获取要转换的子数据集
    data = datasets.GetSubDatasets()[0][0]
    Raster_DATA = gdal.Open(data)
    DATA_Array = Raster_DATA.ReadAsArray()
    print("=================================================================")
    print(DATA_Array)
    #  保存为tif
    splitext = os.path.splitext(i)
    print(splitext[0])
    TifName = "F:\mxy\department\国遥\数据\Modis\ladsweb\\to\\"+splitext[0]+".tif"
    # geoData = gdal.Warp(TifName, Raster_DATA,
    #                     dstSRS='EPSG:4326', format='GTiff',
    #                     resampleAlg=gdal.GRA_Bilinear)
    # gdal.Warp(srcDSOrSrcDSTab=Raster_DATA,
    #           destNameOrDestDS=TifName,
    #           format="GTiff",
    #           dstSRS='EPSG:3795')
    gdal.Translate(srcDS=Raster_DATA,
                   destName=TifName,
                   format="GTiff")
    # del geoData
