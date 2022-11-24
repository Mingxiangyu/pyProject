# -*- codeing = utf-8 -*-
# @Time :2022/11/24 17:28
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @File :  下载NCAR气象数据GFS数据.py
# @link：https://blog.csdn.net/qq_38423499/article/details/122470244

#################################################################
# Python Script to retrieve 1 online Data file of 'ds084.1',
# total 548.05M. This script uses 'requests' to download data.
#
# Highlight this script by Select All, Copy and Paste it into a file;
# make the file executable and run it on command line.
#
# You need pass in your password as a parameter to execute
# this script; or you can set an environment variable RDAPSWD
# if your Operating System supports it.
#
# Contact rpconroy@ucar.edu (Riley Conroy) for further assistance.
#################################################################


import os
import sys

import requests
from pip._vendor.distlib.compat import raw_input


def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size / filesize) * 100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()


# Try to get password
if len(sys.argv) < 2 and not 'RDAPSWD' in os.environ:
    try:
        import getpass

        input = getpass.getpass
    except:
        try:
            input = raw_input
        except:
            pass
    pswd = input('Password: ')
else:
    try:
        pswd = sys.argv[1]
    except:
        pswd = os.environ['RDAPSWD']

url = 'https://rda.ucar.edu/cgi-bin/login'
values = {'email': '383590636@qq.com', 'passwd': pswd, 'action': 'login'}
# Authenticate
ret = requests.post(url, data=values)
if ret.status_code != 200:
    print('Bad Authentication')
    print(ret.text)
    exit(1)
dspath = 'https://rda.ucar.edu/data/ds084.1/'
filelist = [
    '2021/20211115/gfs.0p25.2021111518.f312.grib2']
for file in filelist:
    filename = dspath + file
    file_base = os.path.basename(file)
    print('Downloading', file_base)
    req = requests.get(filename, cookies=ret.cookies, allow_redirects=True, stream=True)
    filesize = int(req.headers['Content-length'])
    with open(file_base, 'wb') as outfile:
        chunk_size = 1048576
        for chunk in req.iter_content(chunk_size=chunk_size):
            outfile.write(chunk)
            if chunk_size < filesize:
                check_file_status(file_base, filesize)
    check_file_status(file_base, filesize)
    print()
