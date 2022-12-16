# https://blog.csdn.net/duanweidong5/article/details/116761316
def days(month, day):
    a = 0
    for i in range(1, month):
        if i in [1, 3, 5, 7, 8, 10, 12]:
            a += 31
        elif i in [4, 6, 9, 11]:
            a += 30
        else:
            a += 28
    a += day
    return a


yrea = int(input("请输入年份"))
month = int(input("请输入月份"))
day = int(input("请输入天数"))
if yrea % 400 == 0:
    a = days(month, day)
    if month > 2:
        a = days(month, day) + 1
    print("%d年%d月%d日是一年中的第%d天" % (yrea, month, day, a))
elif yrea % 4 == 0 and yrea % 100 != 0:
    a = days(month, day)
    if month > 2:
        a = days(month, day) + 1
    print("%d年%d月%d日是一年中的第%d天" % (yrea, month, day, a))
else:
    print("%d年%d月%d日是一年中的第%d天" % (yrea, month, day, days(month, day)))
