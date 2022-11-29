# -*- codeing = utf-8 -*-
# @Time :2022/11/28 13:21
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://blog.csdn.net/absll/article/details/127832520
# @File :  下载电离层格网文件.py

"""
url = https://cddis.nasa.gov/archive/gnss/products/ionex/2021/004/igsg0040.21i.Z
url = 'https://cddis.nasa.gov/archive/gnss/products/ionex/2021/'+doy+'/'+'igsg'+doy+str(0)+'.21i.Z'
"""

import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

s = Service("E:\edgedriver_win64\msedgedriver.exe")  # 这里写本地的msedge的所在路径
driver = webdriver.Edge(service=s)
driver.get(
    "https://urs.earthdata.nasa.gov/oauth/authorize?client_id=gDQnv1IO0j9O2xXdwS8KMQ&response_type=code&redirect_uri=https%3A%2F%2Fcddis.nasa.gov%2Fproxyauth&state=aHR0cDovL2NkZGlzLm5hc2EuZ292L2FyY2hpdmUv")  # 该处为具体网址
driver.refresh()  # 刷新页面
driver.maximize_window()  # 浏览器最大化
driver.find_element(By.ID, 'username').send_keys('xymeng')
driver.find_element(By.ID, 'password').send_keys('18844120269oooOOO')
time.sleep(0.5)
driver.find_element(By.NAME, 'commit').click()
driver.get('https://cddis.nasa.gov/archive/')
time.sleep(10)
"""
下载电离层格网文件
"""
driver.find_element(By.ID, 'gnss').click()
driver.find_element(By.ID, 'products').click()
driver.find_element(By.ID, 'ionex').click()
driver.find_element(By.ID, '2019').click()
"""
下载观测值O文件
"""
driver.find_element(By.ID, 'gnss').click()
driver.find_element(By.ID, 'data').click()
driver.find_element(By.ID, 'daily').click()
driver.find_element(By.ID, '2021').click()
"""
下载星历n文件
"""
driver.find_element(By.ID, 'gnss').click()
driver.find_element(By.ID, 'data').click()
driver.find_element(By.ID, 'daily').click()
driver.find_element(By.ID, '2020').click()
driver.find_element(By.ID, 'brdc').click()
for doy in range(93, 365):
    doy = str(doy)
    doy = doy.zfill(3)
    driver.find_element(By.ID, doy).click()
    driver.find_element(By.ID, 'igsg' + doy + str(0) + '.19i.Z').click()
    driver.back()
    time.sleep(10)
