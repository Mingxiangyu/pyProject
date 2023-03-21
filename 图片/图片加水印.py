# -*- codeing = utf-8 -*-
# @Time :2023/1/16 9:23
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :https://mp.weixin.qq.com/s/8J_M0f3ou4llLOzpgR9znw
# @File :  图片加水印.py
from watermarker.marker import add_mark

"""
file：待添加水印的照片；
mark：使用哪些字作为水印；
out：添加水印后保存的位置；
color：水印字体的颜色，默认颜色#8B8B1B；
size：水印字体的大小，默认50；
opacity：水印字体的透明度，默认0.15；
space：水印字体之间的间隔, 默认75个空格；
angle：水印字体的旋转角度，默认30度。
"""
add_mark(file=r"./test/testmarker.jpg", out=r"./output", mark="闲欢", opacity=0.5, angle=30, space=30, size=100)
