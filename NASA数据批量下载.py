# Python 3.6.6
#保存下载链接
import os
import re
import requests

URL = 'https://oceandata.sci.gsfc.nasa.gov/MODIS-Aqua/Mapped/Daily/9km/chlor_a/2016/'  #链接地址
DIR = 'D:\data\chla'  #保存路径
FILENAME = 'chla_2016.txt' #保存文件
def WriteURL(url,filename):
	resp = requests.get(url)
	pattern = r'<td><a href=\'(.*?)\'>'
	down_url_list = re.findall(pattern,resp.text)
	with open(filename,'w') as file:
		for down_url in down_url_list:
			text = down_url + '\n'
			print(text)
			file.write(text)
			file.flush()
if __name__=='__main__':
	os.chdir(DIR) #
	WriteURL(URL,FILENAME)
