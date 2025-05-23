# -*- codeing = utf-8 -*-
# @Time :2022/11/18 14:05
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://blog.csdn.net/qazwsxpy/article/details/127427409
# @link：https://www.heywhale.com/api/notebooks/62ea6d2ef145d47a93d25a5a/RenderedContent?cellcomment=1&cellbookmark=1#1.5-%E5%85%A8%E5%9B%BD%E7%A9%BA%E6%B0%94%E8%B4%A8%E9%87%8F%E8%A7%82%E6%B5%8B%E6%95%B0%E6%8D%AE-by-%E2%9C%98%E3%80%81%E5%93%88%E5%93%88%E3%80%81%E6%B4%8B%E6%B5%81
# @File :  下载MODIS 极轨卫星数据.py

from __future__ import (division, print_function, absolute_import, unicode_literals)

"""
官网提供python样例

python命令
python laads-data-download.py -s https://ladsweb.modaps.eosdis.nasa.gov/archive/AMS/13_920/AMSL1B/ -d E:\temp\ -t eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2Njg3NTIzNDAsIm5iZiI6MTY2ODc1MjM0MCwiZXhwIjoxNjg0MzA0MzQwLCJ1aWQiOiJkZGxlYXJuaW5nIiwiZW1haWxfYWRkcmVzcyI6Im14aWFuZ195dUAxNjMuY29tIiwidG9rZW5DcmVhdG9yIjoiZGRsZWFybmluZyJ9.LFuRdRWnkpR2VGk6GzIN_bl2h6AZdtUNiJh1e6vuMn8

nasa token
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2Njg3NTIzNDAsIm5iZiI6MTY2ODc1MjM0MCwiZXhwIjoxNjg0MzA0MzQwLCJ1aWQiOiJkZGxlYXJuaW5nIiwiZW1haWxfYWRkcmVzcyI6Im14aWFuZ195dUAxNjMuY29tIiwidG9rZW5DcmVhdG9yIjoiZGRsZWFybmluZyJ9.LFuRdRWnkpR2VGk6GzIN_bl2h6AZdtUNiJh1e6vuMn8
"""
import os
import os.path
import shutil
import sys

try:
    from StringIO import StringIO  # python2
except ImportError:
    from io import StringIO  # python3

################################################################################

USERAGENT = 'tis/download.py_1.0--' + sys.version.replace('\n', '').replace('\r', '')


def geturl(url, token=None, out=None):
    headers = {'user-agent': USERAGENT}
    if not token is None:
        headers['Authorization'] = 'Bearer ' + token
    try:
        import ssl
        CTX = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # 如果是python2走这个，否则走下面
        if sys.version_info.major == 2:
            import urllib2
            try:
                fh = urllib2.urlopen(urllib2.Request(url, headers=headers), context=CTX)
                # 保存路径，如果有存储路径则进行文件拷贝（即下载）
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
                # 保存路径，如果有存储路径则进行文件拷贝（即下载）
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


################################################################################


DESC = "如果文件不存在，此脚本将递归地从 LADS URL 下载所有文件，并将它们存储到“\\”指定路径 "


def sync(src, dest, tok):
    """将 src url 与 dest 目录同步"""
    try:
        import csv
        files = [f for f in csv.DictReader(StringIO(geturl('%s.csv' % src, tok)), skipinitialspace=True)]
    except ImportError:
        import json
        files = json.loads(geturl(src + '.json', tok))

    # 使用 os.path 因为 python 23 都支持它，而 pathlib 是 3.4+
    for f in files:
        # 目前我们使用0文件大小的文件来表示目录
        filesize = int(f['size'])
        path = os.path.join(dest, f['name'])
        url = src + '/' + f['name']
        # 这一步判断当前的是文件夹还是文件
        if filesize == 0:
            try:
                print('creating dir:', path)
                os.mkdir(path)
                sync(src + '/' + f['name'], path, tok)
            except IOError as e:
                print("mkdir `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
                sys.exit(-1)
        else:
            try:
                # 这一步判断本地是否存在该文件，如果不存在就下载，存在的话就跳过
                if not os.path.exists(path):
                    print('downloading: ', path)
                    with open(path, 'w+b') as fh:
                        geturl(url, tok, fh)
                else:
                    print('skipping: ', path)
            except IOError as e:
                print("open `%s': %s" % (e.filename, e.strerror), file=sys.stderr)
                sys.exit(-1)
    return 0


# def _main(argv):
#     parser = argparse.ArgumentParser(prog=argv[0], description=DESC)
#     parser.add_argument('-s', '--source', dest='source', metavar='URL', help='Recursively download files at URL', required=True)
#     parser.add_argument('-d', '--destination', dest='destination', metavar='DIR', help='Store directory structure in DIR', required=True)
#     parser.add_argument('-t', '--token', dest='token', metavar='TOK', help='Use app token TOK to authenticate', required=True)
#     args = parser.parse_args(argv[1:])
#     if not os.path.exists(args.destination):
#         os.makedirs(args.destination)
#     return sync(args.source, args.destination, args.token)

def _main(SaveDir, URL, Token):
    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)
    return sync(URL, SaveDir, Token)


if __name__ == '__main__':
    SaveDir = "D:\RS_data"
    DataURL = "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/6/MOD09/2022/266/MOD09.A2022266.1000.006.2022268023535.hdf"
    Token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUFMgT0F1dGgyIEF1dGhlbnRpY2F0b3IiLCJpYXQiOjE2Njg3NTIzNDAsIm5iZiI6MTY2ODc1MjM0MCwiZXhwIjoxNjg0MzA0MzQwLCJ1aWQiOiJkZGxlYXJuaW5nIiwiZW1haWxfYWRkcmVzcyI6Im14aWFuZ195dUAxNjMuY29tIiwidG9rZW5DcmVhdG9yIjoiZGRsZWFybmluZyJ9.LFuRdRWnkpR2VGk6GzIN_bl2h6AZdtUNiJh1e6vuMn8"
    # SaveDir = input("请输入数据保存地址")
    # DataURL = input("请输入数据所在链接")
    # Token = input("请输入Keys")
    try:
        sys.exit(_main(SaveDir, DataURL, Token))
    except KeyboardInterrupt:
        sys.exit(-1)
