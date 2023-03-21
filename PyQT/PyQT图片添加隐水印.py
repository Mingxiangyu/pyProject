# -*- codeing = utf-8 -*-
# @Time :2023/1/10 16:21
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  PyQT添加隐水印.py
import io
import os

import cv2
import numpy as np
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class WatermarkGenerator(QWidget):
    tool_name = '添加水印'

    def __init__(self, parent=None, title='添加水印', **kwargs):
        super(WatermarkGenerator, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setFixedSize(600, 500)
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        # 定义一些必要的组件
        self.grid = QGridLayout()
        # --label
        self.show_label = QLabel()
        self.show_label.setScaledContents(True)
        self.show_label.setMaximumSize(600, 400)
        # self.show_image = Image.open(os.path.join(rootdir, 'resources/background.jpg')).convert('RGB')
        self.show_image = None
        self.updateimage()
        self.show_image_ext = 'jpg'
        self.watermark_label = QLabel('输入您的水印:')
        self.source_img_label = QLabel('原图片路径:')
        # self.target_img_label = QLabel('目标图片路径:')
        # --输入框
        self.watermark_edit = QLineEdit()
        self.watermark_edit.setText('想要添加的水印文字')
        self.source_img_edit = QLineEdit()
        self.source_img_edit.setText('图片路径')
        # --button
        self.generate_button = QPushButton('添加水印')
        self.save_button = QPushButton('保存图片')
        # --下拉框
        # self.font_combobox = QComboBox()
        # for item in ['一笔艺术签', '连笔商务签', '一笔商务签', '真人手写', '暴躁字']:
        #     self.font_combobox.addItem(item)
        # self.color_combobox = QComboBox()
        # for item in ['Black', 'Blue', 'Red', 'Green', 'Yellow', 'Pink', 'DeepSkyBlue', 'Cyan', 'Orange', 'Seashell']:
        #     self.color_combobox.addItem(item)
        # 组件布局
        self.grid.addWidget(self.show_label, 0, 0, 5, 5)
        self.grid.addWidget(self.watermark_label, 5, 0, 1, 1)
        self.grid.addWidget(self.watermark_edit, 5, 1, 1, 4)
        self.grid.addWidget(self.source_img_label, 6, 0, 1, 1)
        self.grid.addWidget(self.source_img_edit, 6, 1, 1, 4)
        # self.grid.addWidget(self.target_img_label, 7, 0, 1, 1)
        # self.grid.addWidget(self.color_combobox, 7, 1, 1, 4)
        self.grid.addWidget(self.generate_button, 8, 3, 1, 1)
        self.grid.addWidget(self.save_button, 8, 4, 1, 1)
        self.setLayout(self.grid)
        # 事件绑定
        self.generate_button.clicked.connect(self.generate)
        self.save_button.clicked.connect(self.save)

    '''生成签名'''

    def generate(self):
        target_image = "resourec.png"
        txt_img = "txt.png"
        self.Text2Img(txt_img)
        source_img_path = self.source_img_edit.text()
        print(type(source_img_path))
        self.big_with_small(source_img_path, txt_img, target_image)

        self.show_image = Image.open(target_image).convert('RGB')
        self.updateimage()
        # 删除临时图片
        os.remove(txt_img)

    '''更新界面上的图片'''

    def updateimage(self):
        if self.show_image is None:
            return
        fp = io.BytesIO()
        self.show_image.save(fp, 'JPEG')
        qtimage = QtGui.QImage()
        qtimage.loadFromData(fp.getvalue(), 'JPEG')
        qtimage_pixmap = QtGui.QPixmap.fromImage(qtimage)
        self.show_label.setPixmap(qtimage_pixmap)

    '''保存签名'''

    def save(self):
        if self.show_image is None:
            return
        filename = QFileDialog.getSaveFileName(self, '保存', './sign.%s' % self.show_image_ext, '所有文件(*)')
        if filename[0]:
            self.show_image.save(filename[0])
            QDialog().show()

    # 文本生成图片
    def Text2Img(self, save_fname):
        text = self.watermark_edit.text()
        print(text)
        img_w = 1000
        img_h = 1680
        img = np.zeros((img_h, img_w, 3))
        x = 0
        y = 0
        for each_text in text:
            idx = ord(each_text)
            rgb = (0, (idx & 0xFF00) >> 8, idx & 0xFF)
            img[y, x] = rgb
            if x == img_w - 1:
                x = 0
                y += 1
            else:
                x += 1
        cv2.imwrite(save_fname, img)

    def big_with_small(self, source_img_path, txt_img_path, res_img_path):
        """
        大图里藏小图
        """
        dst_img = self.generate_img(source_img_path, txt_img_path)
        cv2.imwrite(res_img_path, dst_img)

    def generate_img(self, big_img_path, small_img_path):
        print("source_path: " + big_img_path)
        r_big_img_path = "r" + big_img_path
        big_img = cv2.imdecode(np.fromfile(big_img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # big_img = cv2.imread(r_big_img_path)
        sml_img = cv2.imread(small_img_path)

        dst_img = big_img.copy()

        big_h, big_w, _ = big_img.shape
        sml_h, sml_w, _ = sml_img.shape

        stepx = big_w / sml_w
        stepy = big_h / sml_h

        for m in range(0, sml_w):
            for n in range(0, sml_h):
                map_col = int(m * stepx + stepx * 0.5)
                map_row = int(n * stepy + stepy * 0.5)

                if map_col < big_w and map_row < big_h:
                    dst_img[map_row, map_col] = sml_img[n, m]

        return dst_img


if __name__ == '__main__':
    """
    pyqt5想要弹出窗口，需要一个主程序驱动，否则无法启动窗口，会直接结束
    """
    import sys

    print("启动服务")
    app = QApplication(sys.argv)
    window = WatermarkGenerator()
    window.show()
    sys.exit(app.exec_())
