import datetime


def get_nday_list(n):
    before_n_days = []
    for i in range(1, n + 1)[::-1]:
        before_n_days.append(str(datetime.date.today() - datetime.timedelta(days=i)))
    return before_n_days


a = get_nday_list(30)
print(a)

# 获取当天日期和7天前日期
today = datetime.date.today()
month = today.month
day = today.day

timedelta = datetime.date.today() - datetime.timedelta(7)
timedelta_month = timedelta.month
timedelta_day = timedelta.day
