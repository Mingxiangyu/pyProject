# -*- codeing = utf-8 -*-
# @Time :2023/1/10 10:27
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  桌面宠物.py
import os

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from id_validator import validator


class IDCardQuery(QWidget):
    """
    身份证信息查询工具
    """
    tool_name = '身份证信息查询工具'

    def __init__(self, parent=None, title='身份证信息查询工具', **kwargs):
        super(IDCardQuery, self).__init__(parent)
        rootdir = os.path.split(os.path.abspath(__file__))[0]
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon(os.path.join(rootdir, 'resources/icon.jpg')))
        self.setFixedSize(600, 400)
        # 定义组件
        self.birthday_label = QLabel('出生日期: ')
        self.birthday_line_edit = QLineEdit('2000-01-01')
        self.address_label = QLabel('出生地区: ')
        self.address_line_edit = QLineEdit('上海市')
        self.sex_label = QLabel('性别: ')
        self.sex_combobox = QComboBox()
        self.sex_combobox.addItem('男')
        self.sex_combobox.addItem('女')
        self.generate_button = QPushButton('随机生成')
        self.idcard_label = QLabel('身份证号: ')
        self.idcard_line_edit = QLineEdit()
        self.query_button = QPushButton('验证查询')
        self.result_label = QLabel('查询结果: ')
        self.result_text_edit = QTextEdit()
        # 排版
        self.grid = QGridLayout()
        self.grid.addWidget(self.birthday_label, 0, 0, 1, 1)
        self.grid.addWidget(self.birthday_line_edit, 0, 1, 1, 3)
        self.grid.addWidget(self.address_label, 0, 4, 1, 1)
        self.grid.addWidget(self.address_line_edit, 0, 5, 1, 3)
        self.grid.addWidget(self.sex_label, 0, 8, 1, 1)
        self.grid.addWidget(self.sex_combobox, 0, 9, 1, 2)
        self.grid.addWidget(self.generate_button, 0, 11, 1, 1)
        self.grid.addWidget(self.idcard_label, 1, 0, 1, 1)
        self.grid.addWidget(self.idcard_line_edit, 1, 1, 1, 10)
        self.grid.addWidget(self.query_button, 1, 11, 1, 1)
        self.grid.addWidget(self.result_label, 2, 0, 1, 1)
        self.grid.addWidget(self.result_text_edit, 3, 0, 1, 12)
        self.setLayout(self.grid)
        # 事件绑定
        self.generate_button.clicked.connect(self.generateID)
        self.query_button.clicked.connect(self.CheckAndParseID)

    def CheckAndParseID(self):
        """
        验证并解析身份证号信息
        """
        id_ = self.idcard_line_edit.text()
        is_valid = validator.is_valid(id_)
        if not is_valid:
            self.result_text_edit.setText('身份证号是否合法: 否\n身份证号信息: 无')
            return
        showinfo = '身份证号是否合法: 是\n'
        idinfos = validator.get_info(id_)
        key_to_showtext = {
            'address_code': '地址码',
            'abandoned': '地址码是否废弃(1是废弃, 0是仍在使用)',
            'address': '地址',
            'birthday_code': '出生日期',
            'constellation': '星座',
            'chinese_zodiac': '生肖',
            'sex': '性别',
        }
        for key, value in idinfos.items():
            if key not in key_to_showtext: continue
            showinfo += f'{key_to_showtext[key]}: {value}\n'
        self.result_text_edit.setText(showinfo)

    def generateID(self):
        """
        生成假的身份证号
        """
        birthday = self.birthday_line_edit.text().replace('-', '')
        birthday = birthday if birthday else None
        address = self.address_line_edit.text()
        address = address if address else None
        sex = self.sex_combobox.currentText()
        sex = 1 if sex == '男' else 0
        try:
            id_ = validator.fake_id(True, address, birthday, sex)
        except:
            id_ = validator.fake_id()
        self.idcard_line_edit.setText(id_)


if __name__ == '__main__':
    """
    pyqt5想要弹出窗口，需要一个主程序驱动，否则无法启动窗口，会直接结束
    """
    import sys

    print("启动服务")
    app = QApplication(sys.argv)
    window = IDCardQuery()
    window.show()
    sys.exit(app.exec_())
