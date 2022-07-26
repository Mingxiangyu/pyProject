import html
import re
from urllib import parse

import PySimpleGUI as sg
import requests

'''
text——需要翻译的内容， 
to_language——目标语言类型， 
text_language——当前语言类型。
'''
# 构建爬虫url
# https://translate.google.com/?sl=auto&tl=en&text=测试
url = 'https://translate.google.com/?text=%s&tl=%s&sl=%s'

def translate(text, to_language="en", text_language="auto"):
    text = parse.quote(text)
    url1 = url % (text, to_language, text_language)
    response = requests.get(url1)
    data = response.text
    print(data)
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<' #TODO 有问题，暂无法解析
    result = re.findall(expr, data)
    print(result)
    if (len(result) == 0):
        return ""
    return html.unescape(result[0])


sg.theme('bluepurple')  # 设置主题
font = ("fangsong", 12)  # 字体仿宋，大小12
menu = [["Help", ["About", "Item", "Author"]]]  # 菜单栏设置
value = ['汉语', '英语', '日语', '法语', '俄语', '自动']  # 语言选择（前端显示），默认只有6种，可以自己添加
var = ['zh', 'en', 'ja', 'fr', 'ru', 'auto']  # 语言选择（后端执行时）
dic = dict(zip(value, var))  # 语言字典配置
layout = [[sg.Menu(menu, tearoff=False)],
          [sg.Text(text='Input', size=(26, 1)),
           sg.Text(text='将', size=(2, 1), justification='center'),
           sg.Combo(values=value, key='from', size=(10, 1)),
           sg.Text(text='翻译为', size=(5, 1), justification='center'),
           sg.Combo(values=value, key='to', size=(10, 1))],
          [sg.Multiline(key="-IN-", size=(60, 8), font=font)],
          [sg.Text(text='Output', size=(30, 1))],
          [sg.Multiline(key="-OUT-", size=(60, 8), font=font)],
          [sg.Text(text='', size=(36, 1)),
           sg.Button("翻译", size=(6, 1)),
           sg.Button("清除", size=(6, 1)),
           sg.Button("退出", size=(6, 1))]
          ]
window = sg.Window("自制桌面翻译器", layout, icon="CT.ico")  # 设置窗口名称，窗口布局，以及图标

"""
windows.read()可以理解为监听，分别有事件event，返回值values。

while循环，当事件为空或者为“退出”是=时，结束循环，并退出。

Popup为消息提示弹窗，可以作为警告，提示，再确认的交互界面。
"""
while True:
    event, values = window.read()
    if event in (None, "退出"):  # 点击“X”或者“退出”按钮时才退出
        break
    if event == "翻译":
        if values["to"] == '' or values["from"] == '':  # 未选择语言类型时弹窗提示
            sg.Popup("请选择语言类型后重试，谢谢！")
        else:
            tar = translate(values["-IN-"], dic[values["to"]], dic[values["from"]])
            window["-OUT-"].Update(tar)
    if event == "清除":
        window["-IN-"].Update("")
        window["-OUT-"].Update("")
    if event == "About":
        sg.Popup("使用方法：",
                 "'翻译'确认输入，并输出翻译结果",
                 "'清除'清除已有输入，清空翻译的结果",
                 "'退出'取消，并退出App", title='', font=font, auto_close=1)
    if event == "Item":
        sg.Popup("翻译类型：",
                 "'输入类型' 输入的语言类型",
                 "'输出类型' 输出的语言类型", title='', font=font, auto_close=1)
    if event == "Author":
        sg.Popup("作者简介：",
                 "姓名：XXXXXX",
                 "Wechat:XXXXXX",
                 "E-mail:XXXXXX@qq.com", title='', font=font, auto_close=1)
window.close()
