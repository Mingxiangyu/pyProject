# -*- codeing = utf-8 -*-
# @Time :2022/11/25 18:48
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  日期月份转为英文和英文转为数字月份.py

import calendar

date_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# 数字转为月份简写
for i in date_list:
    print(calendar.month_abbr[i])

# 数字转月份的全写
for i in date_list:
    print(calendar.month_name[i])

month_abbr_list = ['Jan',
                   'Feb',
                   'Mar',
                   'Apr',
                   'May',
                   'Jun',
                   'Jul',
                   'Aug',
                   'Sep',
                   'Oct',
                   'Nov',
                   'Dec']

# 简写月份转数字
for i in month_abbr_list:
    print(list(calendar.month_abbr).index(i))
