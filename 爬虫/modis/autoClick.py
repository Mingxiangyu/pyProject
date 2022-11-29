# -*- codeing = utf-8 -*-
# @Time :2022/11/29 15:58
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link: https://blog.csdn.net/u013598957/article/details/118493249
# @File :  autoClick.py

import random
# from selenium.webdriver.common.keys import Keys
import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

__author__ = 'Ray'


class GetCookie:
    def __init__(self, driver_path, date_range, area_of_interest, username, password):
        self.driver_path = driver_path
        self.date_range = date_range
        self.area_of_interest = area_of_interest
        self.username = username
        self.password = password

    def autoClick(self):
        count = 1
        while True:
            # 1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口

            # 开启开发者工具（F12）
            # option = webdriver.ChromeOptions()
            # option.add_argument("--auto-open-devtools-for-tabs")
            # browser = webdriver.Chrome(chrome_options=option,
            #                           executable_path=self.driver_path)

            # 为给webdriver的options增加参数excludeSwitches
            option = webdriver.ChromeOptions()
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.add_experimental_option('useAutomationExtension', False)
            browser = webdriver.Chrome(executable_path=self.driver_path, options=option)
            # browser = webdriver.Chrome(executable_path=self.driver_path)
            # browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            #     "source": """
            #     Object.defineProperty(navigator, 'webdriver', {
            #       get: () => undefined
            #     })
            #   """
            # })

            try:
                # 2.通过浏览器向服务器发送URL请求
                url1 = 'https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD11A1--6/{}/DB/{}'.format(
                    self.date_range, self.area_of_interest)  # 后续维护问题，观察网站变化，不过该模块目的只是获取cookie
                # browser.get(
                #     'https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD11A1--6/2021-02-22..2021-03-08/DB/97,30.1,107.1,21.2')
                browser.get(url1)
                time.sleep(1)

                # 3.刷新浏览器
                # browser.refresh()

                # 4.设置浏览器的大小
                browser.set_window_size(1400, 800)

                # 5.登陆页面之前
                profile = browser.find_element_by_id("profile-menu-option")
                ActionChains(browser).move_to_element(profile).perform()
                profile.click()
                time.sleep(4.5)  # ！注意对手动使用浏览器时的精准模拟，这里会有近1秒的Loading，才会显示login按钮，前提是网络条件良好
                login = browser.find_element_by_xpath(
                    "/html/body/nav/div/div/ul/li[6]/ul/li/a")  # 后续维护问题，观察网站变化，暂时未找到更好的定位方式
                login.click()

                # 6.模拟登录
                # 输入账号
                input_account = browser.find_element_by_id('username')
                input_account.send_keys(self.username)
                # 输入密码
                input_password = browser.find_element_by_id('password')
                input_password.send_keys(self.password)
                # 取消勾选保持登陆状态的选项
                cancel_stay_in = browser.find_element_by_id('stay_in')
                cancel_stay_in.click()
                # 点击登录按钮
                time.sleep(2)
                login_button = browser.find_element_by_name('commit')

                # builder = ActionChains(browser)
                # builder.key_down(Keys.F12).perform()

                login_button.click()
                # print('=====================================')
                # print("middle page url: " + str(browser.current_url))
                # print("middle page title: " + str(browser.title))
                # print("cookie信息为：" + str(browser.get_cookies()))  # 多个Cookie
                # print(browser.get_cookies)

                # 7.回到产品页面，发现该页面下Cookie 各name-value组成的对能满足我们所需的request headers中的Cookie
                time.sleep(5)
                print('\n=====================================')
                print("current url: " + str(browser.current_url))
                print("current title: " + str(browser.title))
                cookie = browser.get_cookies()
                print('\n')
                print(type(cookie))
                print("cookie信息为：" + str(cookie))  # 多个Cookie

                time.sleep(4)
                # browser.quit()  # 关闭所有窗口
                return cookie

            except:
                browser.quit()
                print('第' + str(count) + '次模拟点击过程中遇到问题\n')
                time.sleep(random.uniform(5, 6))
                count += 1


# 用于测试的主程序，实际投入时应运行nasa_modis.py中的主程序
if __name__ == '__main__':
    path = "chromedriver.exe"
    ranges = '2021-02-22..2021-03-08'
    interest = '97,30.1,107.1,21.2'
    user = '......'  # 个人账户信息及密码！
    code = '......'
    auto_click = GetCookie(path, ranges, interest, user, code)  # 可以def __init__(self, parameters):
    cookie = auto_click.autoClick()
