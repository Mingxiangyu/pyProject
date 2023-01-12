# -*- codeing = utf-8 -*-
# @Time :2023/1/11 15:09
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  python爬虫实现火山周报表格程序.py
import re
import requests
import xlrd
import xlwt
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("request failed")


def getLocation(addr):
    demo = getHTMLText(addr)
    a = re.findall(r"\d+.\d+&deg;\w", demo)
    latitude = re.split("&deg;", a[0])[0] + re.split("&deg;", a[0])[1]
    longitude = re.split("&deg;", a[1])[0] + re.split("&deg;", a[1])[1]
    b = re.search(r"elev. \d+[.\d+] m", demo)
    ele = re.search(r"\d+[.\d+]", b.group()).group() + "m"
    return [latitude, longitude, ele]


def getObjectData(soup):
    li = []

    New = soup.select('.WeeklyNameNew')
    print(len(New))
    for s in New:
        s = str(s)
        res = re.compile('<b>(.*?)</b>')
        volcano_name = re.findall(res, s)
        res = re.compile(r'                        | ([a-zA-Z].+)')
        country = re.findall(res, s)
        while "" in country:
            country.remove("")
        elevation = country[1].strip()
        res = re.compile('Elevation (\d+) m')
        elevation = re.findall(res, elevation)[0]
        country = country[0].strip()
        if '(' in country:
            res = re.compile('\((\w+)\)')
            country = re.findall(res, country)[0]

        res = re.compile('(\d+\.\d+°[NS])')
        latitude = re.findall(res, s)
        res = re.compile('(\d+\.\d+°[WE])')
        longitude = re.findall(res, s)
        while "" in latitude:
            latitude.remove("")
        while "" in longitude:
            longitude.remove("")
        while "" in volcano_name:
            volcano_name.remove("")
        # print(volcano_name[0], country, latitude[0], longitude[0], elevation)
        activity = 'New'

        li.append([volcano_name[0], country, latitude[0], longitude[0], elevation,
                   "", "", "", "爆炸式", activity, "无"])

    ongoing = soup.select('.WeeklyNameOngoing')
    print(len(ongoing))
    for s in ongoing:
        s = str(s)
        res = re.compile('<b>(.*?)</b>')
        volcano_name = re.findall(res, s)
        res = re.compile(r'                        | ([a-zA-Z].+)')
        country = re.findall(res, s)
        while "" in country:
            country.remove("")
        elevation = country[1].strip()
        res = re.compile('Elevation (\d+) m')
        elevation = re.findall(res, elevation)[0]
        country = country[0].strip()
        if '(' in country:
            res = re.compile('\((\w+)\)')
            country = re.findall(res, country)[0]

        res = re.compile('(\d+\.\d+°[NS])')
        latitude = re.findall(res, s)
        res = re.compile('(\d+\.\d+°[WE])')
        longitude = re.findall(res, s)
        while "" in latitude:
            latitude.remove("")
        while "" in longitude:
            longitude.remove("")
        while "" in volcano_name:
            volcano_name.remove("")
        # print(volcano_name[0], country, latitude[0], longitude[0], elevation)
        activity = 'Ongoing'

        li.append([volcano_name[0], country, latitude[0], longitude[0], elevation,
                   "", "", "", "爆炸式", activity, "无"])
    for i in li:
        print(i)

    print('-' * 50)

    return li


def printUnivList(result, num):
    result.insert(0, ["火山名", "所属国家", "纬度", "经度", "海拔", "警戒级别", "航空彩色代码", "危险区范围",
                      "喷发方式", "新增/持续", "灾害情况"])
    new_result = result
    for i in new_result:
        if i[0] == "火山名":
            continue
        if i[9] == "New":
            i[9] = "新增"
        elif i[9] == "Ongoing":
            i[9] = "持续"
        # change latitude output format
        if re.search(r"[\d]+.[\d]+S$", i[2]):
            tem = "-" + re.search(r"[\d]+.[\d]+", i[2]).group()
            i[2] = tem
        else:
            tem = re.search(r"[\d]+.[\d]+", i[2]).group()
            i[2] = tem
        # change longitude output format
        if re.search(r"[\d]+.[\d]+W$", i[3]):
            tem = "-" + re.search(r"[\d]+.[\d]+", i[3]).group()
            i[3] = tem
        else:
            tem = re.search(r"[\d]+.[\d]+", i[3]).group()
            i[3] = tem

        # change country_name format,remove"()"
        if re.search(r"\(.*\)", i[1]):
            tem = re.search(r"\(.*\)", i[1]).group()[1:-1]
            i[1] = tem

        # change English volcano_name and country_name to Chinse names
        excel1 = xlrd.open_workbook("country_name.xlsx")
        excel2 = xlrd.open_workbook("volcano_name.xlsx")

        sheet1 = excel1.sheet_by_index(0)
        sheet2 = excel2.sheet_by_index(0)
        country_cn = sheet1.col_values(0)
        country_en = sheet1.col_values(1)
        volcano_cn = sheet2.col_values(0)
        volcano_en = sheet2.col_values(1)
        count = 0
        while count < sheet1.nrows:
            if i[1] == country_en[count]:
                i[1] = country_cn[count]
            count = count + 1
        else:
            print("country not in the list")
        count = 0
        while count < sheet2.nrows:
            if i[0] == volcano_en[count]:
                i[0] = volcano_cn[count]
            count = count + 1
        else:
            print("volcano not include in the list")

    # print the list on screen
    tplt = "{0:^20}{1:^20}{2:^10}{3:^10}{4:^10}{5:^10}{6:^10}{7:^10}{8:^10}{9:^10}{10:^10}"
    for i in range(num):
        print(tplt.format(new_result[i][0], new_result[i][1], new_result[i][2], new_result[i][3],
                          new_result[i][4], new_result[i][5], new_result[i][6], new_result[i][7],
                          new_result[i][8], new_result[i][9], new_result[i][10]))
    return new_result


def len_byte(value):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    length = (utf8_length - length) / 2 + length
    return int(length)


def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
    # Automatically design column width
    col_width = []
    for i in range(len(datas)):
        for j in range(len(datas[i])):
            if i == 0:
                col_width.append(len_byte(datas[i][j]))
            else:
                if col_width[j] < len_byte(str(datas[i][j])):
                    col_width[j] = len_byte(datas[i][j])
    for i in range(len(col_width)):
        if col_width[i] > 10:
            sheet1.col(i).width = 256 * (col_width[i] + 1)  # Automatically design column width
    sheet1.col(1).width = 4000
    i = 0

    # style1 = xlwt.XFStyle()  # 设置单元格格式为文本
    #
    # style1.num_format_str = "0.000"
    for data in datas:
        for j in range(len(data)):
            # if (j!=0 and (i==2 or i==3 or i==4)):
            #     sheet1.write(i,j,data[j],style=style1)
            # else:
            sheet1.write(i, j, data[j])
        i = i + 1

    f.save(file_path)


url = "http://volcano.si.edu/reports_weekly.cfm"
demo = getHTMLText(url)
soup = BeautifulSoup(demo, "html.parser")
result = getObjectData(soup)
full_result = printUnivList(result, len(result))
file_path = 'volcano1.xls'
data_write(file_path, full_result)
