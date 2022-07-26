import os
import urllib.parse  # 转码模块
import urllib.request  # 打开网页模块

'''
原文连接：https://blog.csdn.net/qq_41882857/article/details/121955494
'''

# 这里的路径可替换为自己保存文件夹的路径
save_path = r"C:/Users\DELL\Desktop\GPS\paris_sub\\"
ak = "Lvgt7yw6mGCklShvUFzzss3i4fSqOEQu"

# 判断文件夹是否存在，若不存在则创建
if not os.path.exists(save_path):
    os.makedirs(save_path)
# data = pd.read_excel(r"D:\01bachelor\sk04paper\SamplePoints\经纬度2000.xlsx", index_col=0, usecols="A:C")
data = []


def Scrap_img():
    # 使用for循环遍历出每个location坐标
    for i in range(2000):
        # 获取采样点经纬度
        # x = str(data.iloc[i][0])
        # y = str(data.iloc[i][1])
        x = str(113.168)  # 测试经度
        y = str(34.792)  # 测试纬度
        location_number = x + ',' + y
        # 水平角度获取4个方向的照片
        for j in range(4):
            # 旋转的角度
            # [0,1,2,3] * 90 = [0,90,180,270]
            heading_number = str(90 * j)

            url = r"https://api.map.baidu.com/panorama/v2?" \
                  "&width=1024&height=512" \
                  "&location=" + location_number + \
                  "&heading=" + heading_number + \
                  "&pitch=" + str(45) + \
                  "fov=" + str(90) + \
                  "&ak=" + ak

            # 文件保存名称
            save_name = str(i) + "." + str(j + 4) + "_" + location_number + ".jpg"
            print(url)
            # 打开网页
            rep = urllib.request.urlopen(url)
            # 将图片存入本地，创建一个save_name的文件，wb为写入
            f = open(save_path + save_name, 'wb')
            # 写入图片
            f.write(rep.read())
            f.close()
            print('图片保存成功')


def Cheak_img():
    # 遍历文件夹中的图片
    for im in os.listdir(save_path):
        # 获取图片绝对路径
        file_path = os.path.abspath("im")
        # 计算图片占用内存
        im_occupy = os.path.getsize(os.path.join(save_path, im))
        if im_occupy < 150:
            os.rename(os.path.join(save_path, im), os.path.join(save_path, 'No_found' + im))


Scrap_img()
Cheak_img()
