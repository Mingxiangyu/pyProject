# -*- codeing = utf-8 -*-
# @Time :2022/12/5 18:02
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  单位转换器.py
def hum_convert(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size


if "__main__" == __name__:
    print(hum_convert(10))
    print(hum_convert(10000))
    print(hum_convert(10000000000))
    print(hum_convert(10000000000000))
