# -*- codeing = utf-8 -*-
# @Time :2022/11/28 18:15
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://blog.csdn.net/LSH1628340121/article/details/126058913
# @File :  Selenium模拟登陆.py
import time

driver.get("https://user.17k.com/www/bookshelf/")
time.sleep(2)
# 获取登陆模块的iframe
el_path = driver.find_element_by_xpath('/html/body/div[4]/div/div/iframe')
# 进去该iframe
driver.switch_to.frame(el_path)
# 进入成功后，输入账号密码以及勾选同意并点击登陆
driver.find_element_by_xpath('//dd[@class="user"]/input').send_keys('你的账号')
driver.find_element_by_xpath('//dd[@class="pass"]/input').send_keys('你的密码')
# 勾选同意
driver.find_element_by_xpath('//*[@id="protocol"]').click()
# 点击登陆
driver.find_element_by_xpath('//dd[@class="button"]/input').click()
