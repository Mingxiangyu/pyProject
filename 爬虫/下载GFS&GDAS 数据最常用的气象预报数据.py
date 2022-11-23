# -*- codeing = utf-8 -*-
# @Time :2022/11/23 12:03
# @Author :xming
# @Version :1.0
# @Descriptioon :
# 原文链接：https://www.heywhale.com/api/notebooks/62ea6d2ef145d47a93d25a5a/RenderedContent?cellcomment=1&cellbookmark=1#1.4-%E5%85%A8%E7%90%83%E6%8E%A2%E7%A9%BA%E6%95%B0%E6%8D%AE-by-%E6%B4%8B%E6%B5%81
# @File :  下载GFS&GDAS 数据最常用的气象预报数据.py
"""
#!/bin/bash

GFS_DATE="20161120"
GFS_TIME="00"; # 00, 06, 12, 18
RES="1p00" # 0p25, 0p50 or 1p00
BBOX="leftlon=0&rightlon=360&toplat=90&bottomlat=-90"
LEVEL="lev_10_m_above_ground=on"
GFS_URL="http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_${RES}.pl?file=gfs.t${GFS_TIME}z.pgrb2.${RES}.f000&${LEVEL}&${BBOX}&dir=%2Fgfs.${GFS_DATE}${GFS_TIME}"

curl "${GFS_URL}&var_UGRD=on" -o utmp.grib
curl "${GFS_URL}&var_VGRD=on" -o vtmp.grib

grib_set -r -s packingType=grid_simple utmp.grib utmp.grib
grib_set -r -s packingType=grid_simple vtmp.grib vtmp.grib

printf "{\"u\":`grib_dump -j utmp.grib`,\"v\":`grib_dump -j vtmp.grib`}" > tmp.json

rm utmp.grib vtmp.grib

DIR=`dirname $0`
node ${DIR}/prepare.js ${1}/${GFS_DATE}${GFS_TIME}

rm tmp.json
"""
