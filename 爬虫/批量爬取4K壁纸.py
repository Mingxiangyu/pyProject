'''
运行前修改自己的账号密码


cookie获取部分
'''

from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get('https://pic.netbian.com/')

wait = WebDriverWait(driver, 10, 0.5)
wait.until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[1]/div/div[2]/a[2]')),
           message='定位超时').click()

sleep(1)

driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[1]/div[3]/ul/li[1]/a/em').click()

wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="combine_page"]/div[1]/div')),
           message='定位超时')

driver.switch_to.frame('ptlogin_iframe')

driver.find_element(By.ID, 'switcher_plogin').click()
username = driver.find_element(By.ID, 'u')
username.send_keys('账号')
sleep(1)
password = driver.find_element(By.ID, 'p')
password.send_keys('密码')
sleep(1)
driver.find_element(By.ID, 'login_button').click()


wait.until(EC.presence_of_element_located(
    (By.XPATH, '/html/body/div[1]/div/ul/li[2]/a')),
           message='定位超时')

cookies = {}
for item in driver.get_cookies():
    cookies[item['name']] = item['value']

'''
采集部分
'''

import requests
import os
from lxml import etree
import re

# 创建文件夹
isExists = os.path.exists('./4ktupian')
if not isExists:
    os.makedirs('./4ktupian')

headers = {
    'Users-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

url = 'http://pic.netbian.com/4kdongman/index_%d.html'

for page in range(1, 16):
    if (page == 1):
        new_url = 'http://pic.netbian.com/4kdongman/'
    else:
        new_url = format(url % page)
    response = requests.get(url=new_url, headers=headers, cookies=cookies)
    # 设置获取响应数据的编码格式
    response.encoding = 'gbk'
    page_text = response.text

    # 数据解析
    tree = etree.HTML(page_text)
    li_list = tree.xpath('//ul[@class="clearfix"]/li')
    img_id_list = []
    img_name_list = []
    for li in li_list:
        img_id = li.xpath('./a/@href')[0]
        img_id = re.findall('\d+', img_id)[0]
        img_id_list.append(img_id)
        img_name_list.append(li.xpath('./a/img/@alt')[0])

    # 获取完整图片url
    img_url_list = []
    for img_url in img_id_list:
        img_url_list.append(f'https://pic.netbian.com/downpic.php?id={img_url}&classid=66')

    # 提取图片数据
    for i in range(len(img_url_list)):
        img_data = requests.get(url=img_url_list[i], headers=headers, cookies=cookies).content
        filePath = './4ktupian/' + img_name_list[i] + '.jpg'
        with open(filePath, 'wb')as fp:
            fp.write(img_data)
        print('%s,下载成功' % img_name_list[i])