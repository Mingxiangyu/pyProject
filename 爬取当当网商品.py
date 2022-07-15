import csv

import requests
from fake_useragent import UserAgent
from lxml import etree


class dangdang(object):
    def __init__(self):
        self.url = 'http://search.dangdang.com/?key={}&page_index={}'
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }

    def get_html(self, url):
        response = requests.get(url, headers=self.headers)
        html = response.text
        return html

    def parse_html(self, html):
        target = etree.HTML(html)
        titles = target.xpath('//p[@class="name"]/a/@title')
        prices = target.xpath('//p[@class="price"]/span/text()')
        links = target.xpath('//p[@class="name"]/a/@href')
        with open('dangdang.csv', 'a', newline='', encoding='utf8') as f:
            csvwriter = csv.writer(f, delimiter=',')
            for title, price, link in zip(titles, prices, links):
                csvwriter.writerow([title, price, link])

    def main(self):
        product = str(input('请输入您要浏览的商品：'))
        end_page = int(input("要爬多少页："))
        for page in range(1, end_page + 1):
            url = self.url.format(product, page)
            print("第%s页。。。。" % page)
            html = self.get_html(url)
            self.parse_html(html)
            print("第%s页爬取完成" % page)


if __name__ == '__main__':
    spider = dangdang()
    spider.main()
