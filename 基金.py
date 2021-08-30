from selenium import webdriver  # 浏览器驱动
from selenium.webdriver.common.keys import Keys  # 模拟浏览器点击时需要用

import time,csv
import random 

fieldnames = ['基金名称','日期', '单位净值', '累计净值', '日涨幅'] # 待获取的目标字段

# 根据用户命名来创建的 csv 文件
def createFile(file_name):
    # 写入文件的域名
    # 创建文件进行存储
    with open(file_name + '.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

# 将数据写入文件的函数
def writeFile(data, file_name):
    """ data: 传入写入的数据; file_name：可根据基金名称自定义 """
    # 对刚才创建的文件进行“追加写”
    with open(file_name + '.csv', 'a', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(data)

def parse_data(client_input, file_name):
    """
    传入完整的基金代码，返回数据，供写入文件的函数写入
    :param client_input: 用户输入的完整基金代码
           file_name: 用户自定义的生成文件的名字
    :return: 基金净值数据
    """
    # ------------------------ 基础配置 ------------------------
    # 设置不加载图片，提速
    chrome_opt = webdriver.ChromeOptions()  # 告知 webdriver：即将需要添加参数

    # 需要添加的参数们
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_opt.add_experimental_option("prefs", prefs)

    # 初始化浏览器，即运行该行代码将会打开浏览器
    driver = webdriver.Chrome(chrome_options=chrome_opt,executable_path = 'E:\迅雷下载\chromedriver.exe')

    # 找寻规律后发现的指定代码后的基金网址
    basic_url = 'https://www.howbuy.com/fund/'
    full_url = f'{basic_url + client_input}' # 全网址等于基本构造 + 人为输入的基金代码
    print(f'即将模拟浏览器打开如下基金网页：{full_url}')

    # --------------- 开始模拟浏览器打开指定基金网页并点击历史净值 ----------------
    driver.get(full_url)
    # 模拟点击历史净值
    driver.find_element_by_id('open_history_data').send_keys(Keys.ENTER)
    time.sleep(1.5) # 设置缓冲时间

    # ------------------------- 激动人心的模拟爬取 ------------------------
    ## 获取需要爬取的总页数
    page_info = driver.find_element_by_xpath('//*[@id="fHuobiData"]/div').text
    name = driver.find_element_by_xpath('//*[@class="lt"]/h1').text
    print(name)
    print(page_info)
    ## 包含最大页码的内容格式模板如下
    """

		    		第1页/共115页&nbsp;
    """
    ## 由上可知，需要替换掉空格，换行符，&nbsp 以及 第1页/共 和 页，这几样东西
    ## 当然，也可以用正则表达式来操作，这样快很多，不用写那么多 replace
    import re
    total_pages = re.findall('共(\d+)页', page_info, re.S)[0] # re.S 消除换行符的影响
    print(f'该基金共 {total_pages} 页')  # 检查一下
    if int(total_pages) >=10:
        total_pages = 10
        print(f'修改页数为50')
    print('='*55)
    print('开始爬取...')
    # 爬取历史净值信息，并模拟翻页
    try:
        for i in range(1, int(total_pages)+1):
            print(f'正在爬取第 {i} 页')
            try:
                for j in range(2, 11):  # 每一页共 10 条信息：2~11
                    # 日期
                    date_xpath = '//*[@id="fHuobiData"]/table/tbody/tr[{}]/td[1]'
                    date = driver.find_element_by_xpath(date_xpath.format(j)).text
                    # 单位净值
                    net_value_xpath = '//*[@id="fHuobiData"]/table/tbody/tr[{}]/td[2]'
                    net_value = driver.find_element_by_xpath(net_value_xpath.format(j)).text
                    # 累计净值
                    total_net_value_xpath = '//*[@id="fHuobiData"]/table/tbody/tr[{}]/td[3]'
                    total_net_value = driver.find_element_by_xpath(total_net_value_xpath.format(j)).text
                    # 日涨幅
                    daily_increase_xpath = '//*[@id="fHuobiData"]/table/tbody/tr[{}]/td[4]/span'
                    daily_increase = driver.find_element_by_xpath(daily_increase_xpath.format(j)).text

                    print(name,date, net_value, total_net_value, daily_increase)
                ## ---------------- 将爬取到的数据写入 csv 文件 ---------------------
                    data = {
                        '基金名称': name,
                        '日期': date,
                        '单位净值': net_value,
                        '累计净值': total_net_value,
                        '日涨幅': daily_increase
                    }
                    # 写入数据
                    writeFile(data, file_name=file_name)

                # 模拟点击下一页: 在大循环处模拟
                driver.find_element_by_xpath('//*[@id="fHuobiData"]/div/a[3]').send_keys(Keys.ENTER)
                time.sleep(random.random()*2)
            except Exception as e:
                print(e.args)
                continue
            print('\n')
        print(f'该基金执行完成，关闭当前窗口')
        # 获得当前所有打开的窗口的句柄执行关闭方法
        all_handles = driver.window_handles
        for handle in all_handles:
            driver.switch_to.window(handle)
            driver.close()
            time.sleep(2)

    except Exception as e:
        print(e.args)  # 为分享方便，只是设置最简单的捕获异常，日后再说


# 调度爬虫的总函数
def main():
    # client_input = input("请输入完整基金代码：")
    client_input = ['260108', '007412']
        # , '006228', '003834', '161725', '005533', '270002', '160416']
    file_name = input("请输入你希望创建的文件名(无需添加引号或后缀)，如 我的基金：")
    createFile(file_name=file_name)
    print('='*50)
    for item in client_input:
        parse_data(item, file_name=file_name)



# 主程序接口
if __name__ == '__main__':
    main()