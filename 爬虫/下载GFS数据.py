# -*- codeing = utf-8 -*-
# @Time :2022/11/24 15:14
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载GFS数据.py
import os
import time

from selenium import webdriver

#  https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t00z.pgrb2.0p25.f000&all_lev=on&all_var=on&subregion=&leftlon=103&rightlon=110&toplat=30&bottomlat=24&dir=%2Fgfs.20200109%2F00
chromedriver = "F:/xxx/xxx/chromedriver"  # 驱动程序所在的位置
os.environ["webdriver.chrome.driver"] = chromedriver  # 将驱动程序三位路径计入到系统路径中
# 创建Chrome浏览器配置对象实例
chromeOptions = webdriver.ChromeOptions()
# 设定下载文件的保存目录
# 如果该目录不存在，将会自动创建
prefs = {"download.default_directory": "C:\\Users\ECIDI\Downloads\\1-21"}
# 将自定义设置添加到Chrome配置对象实例中
chromeOptions.add_experimental_option("prefs", prefs)
# 启动带有自定义设置的Chrome浏览器
driver = webdriver.Chrome(chromedriver,
                          chrome_options=chromeOptions)

driver.maximize_window()  # 窗口最大化（无关紧要哈）

for i in range(1, 76):  # 取值从1~75，表示从1到75个小时的预测时长上的
    # print(type(i))
    if i < 10:
        i = "00%d" % i
    elif i < 100:
        i = "0%d" % i
    else:
        i = str(i)
    for j in [0, 6, 12, 18]:  # 表示数据发布的时间分别是00,06,12,18

        if j < 10:
            j = "0%d" % j
        elif j < 100:
            j = "%d" % j
        else:
            j = str(j)
        path = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl?file=gfs.t" + j + "z.pgrb2.0p25.f" + i + "&all_lev=on&all_var=on&subregion=&leftlon=103&rightlon=110&toplat=30&bottomlat=24&dir=%2Fgfs.20200121%2F" + j
        print('path', path)
        driver.get(path)  # 打开网址
print('开始休眠等待浏览器将数据下载完成')
time.sleep(60)
driver.quit()

