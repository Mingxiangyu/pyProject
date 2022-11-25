# -*- codeing = utf-8 -*-
# @Time :2022/11/25 10:58
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @link :https://blog.csdn.net/whatday/article/details/109257089
# @File :  搭建FTP服务器的Server端.py
# -*- coding:utf-8 -*-
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 实例化DummyAuthorizer来创建ftp用户
authorizer = DummyAuthorizer()
# 参数：用户名，密码，目录，权限
authorizer.add_user('admin', '123456', r'C:\Users\Administrator\Desktop\ftp', perm='elradfmwMT')
# 匿名登录
# authorizer.add_anonymous('/home/nobody')
handler = FTPHandler
handler.authorizer = authorizer
# 参数：IP，端口，handler
server = FTPServer(('0.0.0.0', 2121), handler)  # 设置为0.0.0.0为本机的IP地址
server.serve_forever()
