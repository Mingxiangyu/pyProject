# Python 3.6.6
# 保存下载链接
import requests

# TODO 现在下载文件需要登录！！！！
URL = 'https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/path/to/granule.nc4'  # 链接地址
# URL = 'https://oceandata.sci.gsfc.nasa.gov/MODIS-Aqua/Mapped/Daily/9km/chlor_a/2016/'  #链接地址
FILENAME = 'G:\软件备份\Project\J2\国遥\granule.nc4'  # 保存路径

# Set the URL string to point to a specific data URL. Here is an example URL:
#   https://data.gesdisc.earthdata.nasa.gov/data/MERRA2/path/to/granule.nc4

# Set the FILENAME string to the data file name, the LABEL keyword value, or any customized name.
# FILENAME = 'your_file_string_goes_here'

result = requests.get(URL)
try:
    result.raise_for_status()
    f = open(FILENAME, 'wb')
    f.write(result.content)
    f.close()
    print('contents of URL written to ' + FILENAME)
except:
    print('requests.get() returned an error code ' + str(result.status_code))
