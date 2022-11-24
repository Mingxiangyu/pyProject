# -*- codeing = utf-8 -*-
# @Time :2022/11/18 13:45
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link：https://blog.csdn.net/qazwsxpy/article/details/127427409
# @link：https://www.heywhale.com/mw/project/62dbd68d3915ed2e06bdcd50
# @File :  下载NOAA气象数据.py
import os
from ftplib import FTP

# 1. 设置您要将文件下载到的目录
destdir = 'E:/Program/MODEL/Python/DownLoad/Noaa_DownLoad'

# 2. 设置包含您要下载的数据的 FTP 目录的路径。
directory = '/archives/gdas1'

# 3.设置FTP服务器
ftpdir = 'arlftp.arlhq.noaa.gov'

# 4.连接并登录到 FTP
ftp = FTP(ftpdir)
ftp.login()

# 5. 更改为文件在 FTP 上的目录
ftp.cwd(directory)

# 6.获取 FTP 目录中的文件列表
files = ftp.nlst()

# 7.设置需求文件，年，月
# year=['12','13']
# month=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']

year = ['12']
month = ['jan']

needfiles = [s for s in files if s[-5:-3] in year and s[6:9] in month]

# 8.计算所需文件的数量和大小
number = len(needfiles)
size = 0
for i in needfiles:
    print(i)
    SIZE = round((size + ftp.size(i)) / 1024 / 1024 / 1024, 2)

print('You have selected ' + str(number) + ' pieces of data,which may about ' + str(SIZE) + 'G')

print('The currently download path is ' + destdir + '\nif you chance to countine ?')

chance = input("Y or N")
"""
通过input（）实现是否继续下载数据的命令。使用input命令时要注意，如果你使用的是spyder5.15版本的话，
该函数是不能正常使用的，这是由于该版本自身的问题。可通过Anaconda官方给出的解决办法，升级到最新的spyder5.3.2版块，正常使用。
"""
if chance.upper() == 'Y':
    # 9.Download all the needfiles
    if not os.path.exists(destdir):
        os.makedirs(destdir)
    os.chdir(destdir)

    for file in needfiles:
        print('Downloading...' + file)
        ftp.retrbinary('RETR ' + file, open(file, 'wb').write)
    print('Sucessfully Download !')

else:
    print('Please modify the path,and try again.')

# 10.over the Download and Close the FTP connection
ftp.quit()
