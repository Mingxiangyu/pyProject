# -*- codeing = utf-8 -*-
# @Time :2022/11/22 13:37
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载modis数据.py
import datetime
import json
import os
import os.path
import shutil
import sys

import requests
from fake_useragent import UserAgent

SaveDir = "D:\RS_data"
DataURL = "https://ladsweb.modaps.eosdis.nasa.gov/"
Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2Njg3NTIzNDAsIm5iZiI6MTY2ODc1MjM0MCwiZXhwIjoxNjg0MzA0MzQwLCJ1aWQiOiJkZGxlYXJuaW5nIiwiZW1haWxfYWRkcmVzcyI6Im14aWFuZ195dUAxNjMuY29tIiwidG9rZW5DcmVhdG9yIjoiZGRsZWFybmluZyJ9.LFuRdRWnkpR2VGk6GzIN_bl2h6AZdtUNiJh1e6vuMn8"


def date_build(begin, end):
    dates = []
    dt = datetime.datetime.strptime(begin, '%Y-%m-%d')
    dt_end = datetime.datetime.strptime(end, '%Y-%m-%d')
    # date=begin
    while dt <= dt_end:
        t = datetime.datetime.strftime(dt, '%Y-%m-%d')
        dates.append(t)
        dt += datetime.timedelta(1)

    # url中时间字符串
    time_st = ""
    if len(dates) > 10:
        time_st += begin
        time_st += ".."
        time_st += end
    else:
        for i, date in enumerate(dates):
            time_st += date
            time_st += ".."
            time_st += date
            if i == len(dates) - 1:
                return time_st
            time_st += ","
    return time_st


class modisDownload(object):
    def __init__(self):
        # 网页版查询请求链接
        # https://ladsweb.modaps.eosdis.nasa.gov/search/order/4/MOD09--6/2013-01-02..2013-01-02,2013-01-14..2013-01-14/DB/12.5,6.7,41.6,-7
        # 下载请求链接
        # https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product=MOD09&collection=6&dateRanges=2022-09-29..2022-09-29,2022-09-30..2022-09-30&areaOfInterest=x1y4,x2y3&dayCoverage=true&dnboundCoverage=true
        """
                参数1：时间起始范围 {2013-01-02..2013-01-02}
                参数2：经纬度范围 {90.8,61.9,119.7,51.1}  W: 90.8°, N: 61.9°, E: 119.7°, S: 51.1°
                """
        self.url = "https://ladsweb.modaps.eosdis.nasa.gov/api/v1/files/product=MOD09&collection=6&dateRanges={}&areaOfInterest=x{}y{},x{}y{}&dayCoverage=true&dnboundCoverage=true"
        ua = UserAgent(verify_ssl=False)
        for i in range(1, 100):
            # 产生随机的User - Agent请求头进行访问
            self.headers = {
                'User-Agent': ua.random
            }

    # 请求网站获取url
    def get_html(self, url) -> str:
        # toDo 添加代理，更新反扒
        response = requests.get(url, headers=self.headers)
        html = response.text
        return html

    def main(self, start_time, end_time, lon_start, lon_end, lan_start, lan_end):
        time_st = date_build(start_time, end_time)
        url = self.url.format(time_st, lon_start, lon_end, lan_start, lan_end)
        print("start download html:{}".format(url))
        html = self.get_html(url)
        print(html)

        data_dict_array = json.loads(html)
        print(type(data_dict_array))

        for data_dict in data_dict_array:
            data = data_dict_array[data_dict]

            file_url_ = data["fileURL"]
            data_json = json.dumps(data)
            with open(SaveDir + "/" + data_dict + ".modisjson", "wb") as f:
                # 写文件用bytes而不是str，所以要转码
                f.write(bytes(data_json, "utf-8"))
                all_file_url_ = DataURL + file_url_
                _main(SaveDir, all_file_url_, Token)
            # print(file_url)
        # todo 获取下载链接列表，并将该列表数据存储为对应元数据文件
        # 基于下载链接，调用token进行文件下载


USERAGENT = 'tis/download.py_1.0--' + sys.version.replace('\n', '').replace('\r', '')


def geturl(url, token=None, out=None):
    headers = {'user-agent': USERAGENT}
    if not token is None:
        headers['Authorization'] = 'Bearer ' + token
    try:
        import ssl
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if sys.version_info.major == 2:
            import urllib2
            try:
                fh = urllib2.urlopen(urllib2.Request(url, headers=headers), context=CTX)
                if out is None:
                    return fh.read()
                else:
                    shutil.copyfileobj(fh, out)
            except urllib2.HTTPError as e:
                print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
                print('HTTP GET error message: %s' % e.message, file=sys.stderr)
            except urllib2.URLError as e:
                print('Failed to make request: %s' % e.reason, file=sys.stderr)
            return None

        else:
            from urllib.request import urlopen, Request, URLError, HTTPError
            try:
                fh = urlopen(Request(url, headers=headers), context=CTX)
                if out is None:
                    return fh.read().decode('utf-8')
                else:
                    shutil.copyfileobj(fh, out)
            except HTTPError as e:
                print('HTTP GET error code: %d' % e.code(), file=sys.stderr)
                print('HTTP GET error message: %s' % e.message, file=sys.stderr)
            except URLError as e:
                print('Failed to make request: %s' % e.reason, file=sys.stderr)
            return None

    except AttributeError:
        # OS X Python 2 and 3 don't support tlsv1.1+ therefore... curl
        import subprocess
        try:
            args = ['curl', '--fail', '-sS', '-L', '--get', url]
            for (k, v) in headers.items():
                args.extend(['-H', ': '.join([k, v])])
            if out is None:
                # python3's subprocess.check_output returns stdout as a byte string
                result = subprocess.check_output(args)
                return result.decode('utf-8') if isinstance(result, bytes) else result
            else:
                subprocess.call(args, stdout=out)
        except subprocess.CalledProcessError as e:
            print('curl GET error message: %' + (e.message if hasattr(e, 'message') else e.output), file=sys.stderr)
        return None


def sync(src, dest, tok):
    try:
        split_ = src.split('/')[-1]
        path = os.path.join(dest, split_)
        # 这一步判断本地是否存在该文件，如果不存在就下载，存在的话就跳过
        if not os.path.exists(path):
            print('downloading: ', path)
            with open(path, 'w+b') as fh:
                geturl(src, tok, fh)
        else:
            print('skipping: ', path)
    except IOError as e:
        print("open `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
        sys.exit(-1)
    # """synchronize src url with dest directory"""
    # try:
    #     import csv
    #     files = [f for f in csv.DictReader(StringIO(geturl('%s.csv' % src, tok)), skipinitialspace=True)]
    # except ImportError:
    #     import json
    #     files = json.loads(geturl(src + '.json', tok))
    #
    # # 使用 os.path 因为 python 23 都支持它，而 pathlib 是 3.4+
    # for f in files:
    #     # 目前我们使用0文件大小的文件来表示目录
    #     filesize = int(f['size'])
    #     path = os.path.join(dest, f['name'])
    #     url = src + '/' + f['name']
    #     # 这一步判断当前的是文件夹还是文件
    #     if filesize == 0:
    #         try:
    #             print('creating dir:', path)
    #             os.mkdir(path)
    #             sync(src + '/' + f['name'], path, tok)
    #         except IOError as e:
    #             print("mkdir `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
    #             sys.exit(-1)
    #     else:
    #         try:
    #             # 这一步判断本地是否存在该文件，如果不存在就下载，存在的话就跳过
    #             if not os.path.exists(path):
    #                 print('downloading: ', path)
    #                 with open(path, 'w+b') as fh:
    #                     geturl(url, tok, fh)
    #             else:
    #                 print('skipping: ', path)
    #         except IOError as e:
    #             print("open `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
    #             sys.exit(-1)
    # return 0


def _main(SaveDir, URL, Token):
    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)
    return sync(URL, SaveDir, Token)


if __name__ == '__main__':
    spider = modisDownload()
    start_time = '2022-9-23'
    end_time = '2022-09-30'
    lon_start = '1'
    lon_end = '2'
    lan_start = '3'
    lan_end = '4'
    spider.main(start_time, end_time, lon_start, lon_end, lan_start, lan_end)
