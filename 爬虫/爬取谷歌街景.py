# _*_ coding: utf-8 _*_

import urllib.request

''' 相关信息
原文连接：http://t.zoukankan.com/lhgis-p-9072154.html

下面是读取的坐标信息txt文档内容
'paris_sub/48.651717_2.493865_270_-004.JPG'
'paris_sub/48.756312_2.069988_90_-004.JPG'
'paris_sub/48.759815_2.502092_90_-004.JPG'
'paris_sub/48.911445_1.850626_270_-004.JPG'
'paris_sub/48.893319_2.262638_90_-004.JPG'
'paris_sub/48.815737_2.412183_270_-004.JPG'
'paris_sub/48.905476_2.527302_90_-004.JPG'
'paris_sub/48.912099_2.285934_270_-004.JPG'
'paris_sub/48.772068_2.033889_90_-004.JPG'
'paris_sub/48.648679_2.306182_90_-004.JPG'
'paris_sub/48.618283_2.925704_90_-004.JPG'
'paris_sub/48.926558_1.941170_270_-004.JPG'
'paris_sub/48.881077_2.705896_90_-004.JPG'
'paris_sub/48.966915_2.477976_90_-004.JPG'
'paris_sub/49.105046_2.245066_270_-004.JPG'
'paris_sub/48.703037_2.216347_270_-004.JPG'
'paris_sub/48.791862_2.420343_90_-004.JPG'
'paris_sub/48.681379_2.660818_90_-004.JPG'
'paris_sub/48.712748_2.377744_90_-004.JPG'
'paris_sub/48.806908_2.604621_270_-004.JPG'
'paris_sub/48.652523_1.862794_90_-004.JPG'
'paris_sub/48.488890_2.270909_90_-004.JPG'
'paris_sub/48.525296_1.950706_270_-004.JPG'
'''


def download(url, name):
    # url = "http://pic2.sc.chinaz.com/files/pic/pic9/201309/apic520.jpg"
    # 保存文件时候注意类型要匹配，如要保存的图片为jpg，则打开的文件的名称必须是jpg格式，否则会产生无效图片
    conn = urllib.request.urlopen(url)

    f = open(name, 'wb')  # wb以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
    f.write(conn.read())
    f.close()
    print('Pic Saved!')


txt_path = r"C:/Users\DELL\Desktop\GPS\paris.txt"
save_path = r"C:/Users\DELL\Desktop\GPS\paris_sub\\"

fp = open(txt_path, "r")  # 以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
for line in fp.readlines():
    line = (lambda x: x[11:33])(line)  # 选取从第十一个到第十三个字符 也可以写成line =  (lambda x: x[11:-11])(line)
    print(line)
    zu = line.split('_')
    jin = zu[0]
    wei = zu[1]
    heading = zu[2]
    name = save_path + jin + "_" + wei + "_" + heading + "_-004.JPG"
    url = "https://maps.googleapis.com/maps/api/streetview?size=936x537&location=" + jin + "," + wei + "&heading=" + heading + "&pitch=-004&key=" + "key"
    print(name)
    print(url)
    download(url, name)
fp.close()
