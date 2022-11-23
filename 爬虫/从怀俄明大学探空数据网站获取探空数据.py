def get_sounding_from_uwyo(dates, station, file=None, region='naconf'):
    """
    从怀俄明大学探空数据网站获取探空数据

    参数：
        dates   : datetime.datetime。探空时间
        station ： 站点信息
        file    : 探空输出文件名。默认为None，即不输出到文件中。
                字符串类型
        region  ：探空数据的区域，可以不指定。默认为北美地区。

    输出：
        sounding : 探空数据。如果输出到文件的话，为None。
    """

    import requests
    from bs4 import BeautifulSoup

    url = ('http://weather.uwyo.edu/cgi-bin/sounding?region={region}&TYPE=TEXT%3ALIST'
           '&YEAR={time:%Y}&MONTH={time:%m}&FROM={time:%d%H}&TO={time:%d%H}'
           '&STNM={stid}').format(region=region, time=dates, stid=station)

    data = BeautifulSoup(requests.request('get', url).text, 'lxml')

    sounding_head = data.find_all('h2')
    sounding = data.find_all('pre')
    sisi_head = data.find_all('h3')

    if file is None:
        return sounding[0].get_text()

    else:
        with open(file, 'w') as f:
            f.write(sounding_head[0].get_text())
            f.write(sounding[0].get_text())
            f.close()


if __name__ == '__main__':
    from datetime import datetime

    dates = datetime(2017, 6, 21, 0)
    station = 58238

    sounding = get_sounding_from_uwyo(dates, station, file='sounding.txt')

    print(sounding)
