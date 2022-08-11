# -*- coding: utf-8 -*-
import re
import urllib.parse
import urllib.request


def handle_request(url, page):
    # 拼接成指定页面的url
    url = url + str(page)
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }

    # 生成请求对象
    request = urllib.request.Request(url=url, headers=headers)
    return request


def parse_content(content):
    pattern = re.compile(
        r'<td>(\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b)</td>.*?<td>(\d+)</td>.*?<td>.*?</td>.*?<td>(.*?)</td>',
        re.S)
    # 通过正则处理，通过分组符号()得到一组元组的列表，元组中第一个元素是IP，第二个元素是端口，第三个元素室协议
    lt = pattern.findall(content)

    return lt


def test_agent(agent):
    # 使用百度测试代理
    url = "http://www.baidu.com/s?wd=ip"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    # 拼接ip_port字段
    ip_port = agent[0] + ':' + agent[1]
    # 创建handler对象
    handler = urllib.request.ProxyHandler({agent[2]: ip_port})
    # 创建opener对象
    print("zheli")
    opener = urllib.request.build_opener(handler)
    # 生成请求对象
    try:
        request = urllib.request.Request(url=url, headers=headers)
        # 发送请求，得到返回状态
        try:
            response = opener.open(request, timeout=10)
            if response.getcode() == 200:
                print("ip可用")
                return True
            else:
                print("ip不可用")
                return False
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)


def main():
    url = 'https://www.xicidaili.com/nn/'
    start_page = int(input("请输入起始页："))
    end_page = int(input("请输入结束页；"))
    for page in (start_page, end_page + 1):
        # 获取请求对象
        request = handle_request(url, page)

        # 获取网页文件
        content = urllib.request.urlopen(request, timeout=10).read().decode()
        # 解析文件
        lt = parse_content(content)
        for agent in lt:
            # 测试代理是否能够被调用
            if test_agent(agent) != False:
                # 第一个元素是IP
                ip = agent[0]
                # 第二个元素是端口
                port = agent[1]
                # 第三个元素是协议
                protocal = agent[2]
                # 拼接成一行的字符串
                string = '%s  %s  %s \n' % (ip, port, protocal)
                # 将字符串追加写到文件中
                with open("ip_pool.txt", "a") as fp:
                    fp.write(string)


# 入口
if __name__ == '__main__':
    main()
