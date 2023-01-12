import pymysql

db = pymysql.connect(host="211.157.132.19", port=17062, user="root", passwd="guoyao@123", db="bigdata_zhongbao",
                     charset="utf8")
cursor = db.cursor()
cursor.execute("select * from data where station='54511099999' and date>'2021-01-01'")
result = cursor.fetchall()
# for i in result:
#     print(i[6])
# f = csv.reader(open('57799099999.csv','r'))
high_temperature_list = []
low_temperature_list = []
prcp_list = []
week_name_list_list = []
rain_month_list = {"01": 0, "02": 0, "03": 0, "04": 0, "05": 0, "06": 0, "07": 0, "08": 0, "09": 0, "10": 0, "11": 0,
                   "12": 0}
for i in result:
    if i[20] == "MAX" or i[22] == 'MIN':
        continue
    if i[20] == 9999.9 or i[22] == 9999.9:
        continue
    # 华氏温度转为摄氏温度
    high_temperature_list.append('%.2f' % ((float(i[20]) - 32) / 1.8))
    low_temperature_list.append('%.2f' % ((float(i[22]) - 32) / 1.8))
    prcp_list.append('%.2f' % ((float(i[22]))))
    week_name_list_list.append(i[1])

    # print(rain_month_list[1])
    # if i[1].split('-')[1] == "01":   
    #     rain_month_list["01"] = rain_month_list["01"] + float(i[24])
    # if i[1].split('-')[1] == "02":  
    #     rain_month_list["02"] = rain_month_list["02"] + float(i[24])
    # if i[1].split('-')[1] == "03":    
    #     rain_month_list["03"] = rain_month_list["03"] + float(i[24])
    # if i[1].split('-')[1] == "04":     
    #     rain_month_list["04"] = rain_month_list["04"] + float(i[24])
    # if i[1].split('-')[1] == "05":    
    #     rain_month_list["05"] = rain_month_list["05"] + float(i[24])
    # if i[1].split('-')[1] == "06":     
    #     rain_month_list["06"] = rain_month_list["06"] + float(i[24])
    # if i[1].split('-')[1] == "07":     
    #     rain_month_list["07"] = rain_month_list["07"] + float(i[24])
    # if i[1].split('-')[1] == "08":      
    #     rain_month_list["08"] = rain_month_list["08"] + float(i[24])
    # if i[1].split('-')[1] == "09":      
    #     rain_month_list["09"] = rain_month_list["09"] + float(i[24])
    # if i[1].split('-')[1] == "10":       
    #     rain_month_list["10"] = rain_month_list["10"] + float(i[24])
    # if i[1].split('-')[1] == "11":       
    #     rain_month_list["11"] = rain_month_list["11"] + float(i[24])
    # if i[1].split('-')[1] == "12":    
    #     rain_month_list["12"] = rain_month_list["12"] + float(i[24])
print(rain_month_list)
print(low_temperature_list)
print(prcp_list)
print(week_name_list_list)
import pyecharts.options as opts
from pyecharts.charts import Line

"""
Gallery 使用 pyecharts 1.1.0
参考地址: https://www.echartsjs.com/examples/editor.html?c=line-marker

目前无法实现的功能:

1、最低气温的最高值暂时无法和 Echarts 的示例完全复刻
"""

# week_name_list = ["一月", "二月", "三月", "四月", "五月", "六月", "七月","八月", "九月", "十月", "十一月", "十二月"]
week_name_list = week_name_list_list
high_temperature = high_temperature_list
low_temperature = low_temperature_list
prcp = prcp_list

(
    Line(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add_xaxis(xaxis_data=week_name_list)
        .add_yaxis(
        series_name="最高气温",
        y_axis=high_temperature,
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")]
        ),
    )
        .add_yaxis(
        series_name="最低气温",
        y_axis=low_temperature,
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(symbol="none", x="90%", y="max"),
                opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            ]
        ),
    )
        .add_yaxis(
        series_name="降雨量",
        y_axis=prcp,
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(value=-2, name="周最低", x=1, y=-1.5)]
        ),
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="average", name="平均值"),
                opts.MarkLineItem(symbol="none", x="90%", y="max"),
                opts.MarkLineItem(symbol="circle", type_="max", name="最高点"),
            ]
        ),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(title="北京气温变化"),
        tooltip_opts=opts.TooltipOpts(trigger="axis"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    )
        .render("temperature_change_line_chart.html")
)

# # 降雨量
# from pyecharts import options as opts
# from pyecharts.charts import Bar
#
# c = (
#     Bar()
#     .add_xaxis(
#         [
#             "1",
#             "2",
#             "3",
#             "4",
#             "5",
#             "6",
#             "7",
#             "8",
#             "9",
#             "10",
#             "11",
#             "12",
#         ]
#     )
#     .add_yaxis("降雨量",['%.2f'%(rain_month_list[n]*25.4) for n in rain_month_list])
#     .set_global_opts(
#         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
#         title_opts=opts.TitleOpts(title="降雨量"),
#     )
#     .render("bar_rotate_xaxis_label.html")
# )
