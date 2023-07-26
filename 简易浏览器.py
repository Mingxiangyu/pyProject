# -*- codeing = utf-8 -*-
# @Time :2023/7/25 10:02
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  简易浏览器.py
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)

        self.nav_bar = QToolBar()
        self.addToolBar(self.nav_bar)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.add_new_tab(QUrl("https://www.baidu.com"), "首页")

        self.setCentralWidget(self.tabs)

        nav_bar = QToolBar()
        self.addToolBar(nav_bar)

        back_btn = QAction("后退", self)
        back_btn.triggered.connect(self.go_back)
        nav_bar.addAction(back_btn)

        forward_btn = QAction("前进", self)
        forward_btn.triggered.connect(self.go_forward)
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("刷新", self)
        reload_btn.triggered.connect(self.reload_page)
        nav_bar.addAction(reload_btn)

        home_btn = QAction("首页", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)
        nav_bar.addWidget(self.url_bar)

        nav_bar.addSeparator()

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # 添加书签管理
        self.bookmarks = []
        self.bookmarks_menu = self.menuBar().addMenu("书签")
        self.update_bookmarks()

        # 添加历史记录
        self.history = []

        # 添加下载管理
        self.downloads = []

        # 添加密码管理
        self.passwords = {}

        # 添加阅读模式
        self.reading_mode = False

        # 添加多语言支持
        self.language = "中文"

        # 添加设置选项
        settings_action = QAction("设置", self)
        settings_action.triggered.connect(self.show_settings)
        self.menuBar().addAction(settings_action)

        # 添加隐私模式
        self.private_mode = False

        # 添加广告拦截
        self.ad_block = False

        # 添加搜索引擎切换
        self.search_engine = "Google"

        # 添加快捷键
        new_tab_shortcut = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab_shortcut.activated.connect(self.add_new_tab)

        # 美化界面
        self.setStyleSheet("""
            QMainWindow {
                background-color: #F0F0F0;
            }
            QTabWidget::pane {
                border: 1px solid #C0C0C0;
                background: white;
            }
            QTabBar::tab {
                padding: 8px;
                background-color: #E0E0E0;
                border: 1px solid #C0C0C0;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #FFD700;
            }
            QToolBar {
                background-color: #E0E0E0;
            }
            QLineEdit {
                background-color: #FFFFFF;
            }
            QStatusBar {
                background-color: #E0E0E0;
            }
        """)

    def tab_open_doubleclick(self, i):

        if i == -1:
            self.add_new_tab()

    def update_url(self, q, browser=None):
        if browser is None:
            browser = self.tabs.currentWidget()
        if browser != self.tabs.currentWidget():
            return

        self.url_bar.setText(q.toString())

        self.url_bar.setText(q.toString())

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget())

    def add_new_tab(self, qurl=None, label="新标签页"):
        if qurl is None:
            qurl = QUrl("https://www.baidu.com")

        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def update_url(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.url_bar.setText(q.toString())

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_url(qurl, self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.baidu.com"))

    def navigate_to_url(self):
        q = QUrl(self.url_bar.text())

        if q.scheme() == "":
            q.setScheme("http")

        self.tabs.currentWidget().setUrl(q)

    def go_back(self):
        self.tabs.currentWidget().back()

    def go_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

    def update_bookmarks(self):
        for bookmark in self.bookmarks:
            self.bookmarks_menu.removeAction(bookmark)

        self.bookmarks.clear()

        for i in range(self.tabs.count()):
            qurl = self.tabs.widget(i).url()
            title = self.tabs.tabText(i)
            action = QAction(title, self)
            action.setData(qurl)
            action.triggered.connect(self.navigate_to_bookmark)
            self.bookmarks.append(action)
            self.bookmarks_menu.addAction(action)

    def navigate_to_bookmark(self):
        action = self.sender()
        if action:
            qurl = action.data()
            self.tabs.currentWidget().setUrl(qurl)

    def show_settings(self):
        settings_dialog = QDialog(self)
        settings_dialog.setWindowTitle("Settings")
        settings_dialog.setMinimumSize(300, 200)

        layout = QVBoxLayout()

        # 添加设置选项
        language_label = QLabel("Language:")
        language_combo = QComboBox()
        language_combo.addItem("English")
        language_combo.addItem("Chinese")
        language_combo.currentIndexChanged.connect(self.set_language)
        language_combo.setCurrentText(self.language)

        layout.addWidget(language_label)
        layout.addWidget(language_combo)

        settings_dialog.setLayout(layout)
        settings_dialog.exec_()

    def set_language(self, index):
        language = "English" if index == 0 else "Chinese"
        if language != self.language:
            self.language = language
            # TODO: 设置浏览器界面语言


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("强大浏览器")

    window = Browser()
    window.show()

    sys.exit(app.exec_())
