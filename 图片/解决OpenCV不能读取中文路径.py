# -*- codeing = utf-8 -*-
# @Time :2023/3/21 15:07
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link : https://blog.csdn.net/szx123_/article/details/128493248
# @File :  解决OpenCV不能读取中文路径.py

import cv2
import numpy as np

imgPATH = "D://abc//中文//图片.bmp"
img = cv2.imread(imgPATH)  # 报错，读取为none

img = cv2.imdecode(np.fromfile(imgPATH, dtype=np.uint8), cv2.IMREAD_COLOR)  # 可以正常读取出文件
