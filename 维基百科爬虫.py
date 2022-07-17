# -*- coding:utf-8 -*-
import time
import urllib

import bs4
import requests

start_url = "https://en.wikipedia.org/wiki/Special:Random"
target_url = "https://en.wikipedia.org/wiki/Philosophy"


def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")

    # 这个div标签包含了网页的主体部分，因为我们要找的链接都出自文章正文部分，直接在正文中开始查找
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # 在存储项目中找到的第一个链接，若项目不包含链接，就将此值保持为空
    article_link = None

    # 查找div标签的所有的直接子段落
    for element in content_div.find_all("p", recursive=False):
        # 查找链接，并判断是不是我们需要的有效链接，若不是，则查找下一个链接并判断
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # 从查找出的链接中生成完整的url,并赋给first_link，由它带回并输出
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link


def continue_crawl(search_history, target_url, max_steps=25):
    if search_history[-1] == target_url:
        print("We've found the target article!")
        return False
    elif len(search_history) > max_steps:
        print("The search has gone on suspiciously long, aborting search!")
        return False
    elif search_history[-1] in search_history[:-1]:
        print("We've arrived at an article we've already seen, aborting search!")
        return False
    else:
        return True


article_chain = [start_url]

while continue_crawl(article_chain, target_url):
    print(article_chain[-1])
    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("We've arrived at an article with no links, aborting search!")
        break

    article_chain.append(first_link)

    time.sleep(2)  # 放慢速度，以免破坏维基百科的服务器
