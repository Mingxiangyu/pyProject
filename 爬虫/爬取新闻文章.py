# -*- codeing = utf-8 -*-
# @Time :2023/1/16 15:22
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://mp.weixin.qq.com/s/fl4oe6i_EPifBL7hlHv4-g
# @File :  爬取新闻文章.py
from newspaper import Article

url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'

# 根据url生成Article对象
article = Article(url)

# 下载文章
article.download()

# 文章的HTML
html = article.html
# '<!DOCTYPE HTML><html itemscope itemtype="http://...'

"""
Python 实用宝典
《Newspaper — 一个能下载38种语言新闻文章的 Python 模块》
"""

# 解析文章
article.parse()

# 获取文章作者
authors = article.authors
print(authors)
# ['Leigh Ann Caldwell', 'John Honway']

# 获取文章发布日期
date = article.publish_date
print(date)
# datetime.datetime(2013, 12, 30, 0, 0)

# 获取文章文本
text = article.text
print(text)
# 'Washington (CNN) -- Not everyone subscribes to a New Year's resolution...'

# 获取顶部图像
image = article.top_image
print(image)
# 'http://someCDN.com/blah/blah/blah/file.png'

# 获取文章多媒体资源
movies = article.movies
print(movies)
# ['http://youtube.com/path/to/link.com', ...]

# 使用 NLP 解析
# article.nlp() # toDo 开启后会报错，待解决

# 获取文章关键词
keywords = article.keywords
print(keywords)
# ['New Years', 'resolution', ...]

# 获取文章摘要
summary = article.summary
print(summary)
# 'The study shows that 93% of people ...'

import newspaper

sina_paper = newspaper.build('https://news.sina.com.cn/', language='zh')

for category in sina_paper.category_urls():
    print(category)
# http://health.sina.com.cn
# http://eladies.sina.com.cn
# http://english.sina.com
# ...

article = sina_paper.articles[0]
article.download()
article.parse()

print(article.text)
# 新浪武汉汽车综合 随着汽车市场的日趋成熟，
# 传统的"集全家之力抱得爱车归"的全额购车模式已然过时，
# 另一种轻松的新兴 车模式――金融购车正逐步成为时下消费者购
# 买爱车最为时尚的消费理念，他们认为，这种新颖的购车
# 模式既能在短期内
# ...

print(article.title)
# 两年双免0手续0利率 科鲁兹掀背金融轻松购_武汉车市_武汉汽
# 车网_新浪汽车_新浪网
