import csv  # 文件格式
import re  # 内置库 用于匹配正则表达式

import imageio as imageio  # 加载图片
import jieba  # 中文分词
import requests  # 发出请求
import wordcloud  # 绘制词云

# 目标网站（即我们获取到的URL）
url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=186803402'

# 设置请求头 伪装浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
}

# 发起请求 获得响应
response = requests.get(url, headers=headers)
html_doc = response.content.decode('utf-8')

# 正则表达式的匹配模式
res = re.compile('<d.*?>(.*?)</d>')
# 根据模式提取网页数据
danmu = re.findall(res, html_doc)

# 保存数据
for i in danmu:
    with open('b站弹幕.csv', 'a', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        danmu = []
        danmu.append(i)
        writer.writerow(danmu)

# 显示数据

f = open('F:/b站视频弹幕.txt', encoding='utf-8')

txt = f.read()
txt_list = jieba.lcut(txt)
# print(txt_list)
string = ' '.join((txt_list))
print(string)

# 很据得到的弹幕数据绘制词云图

mk = imageio.imread(r'F:/basketball.png')

w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',
                        font_path='C:/Windows/SIMLI.TTF',
                        mask=mk,
                        scale=15,
                        stopwords={' '},
                        contour_width=5,
                        contour_color='red'
                        )

w.generate(string)
w.to_file('gaijinwordcloud.png')