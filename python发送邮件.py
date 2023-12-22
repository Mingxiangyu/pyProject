# -*- codeing = utf-8 -*-
# @Time :2023/12/22 10:34
# @Author :xming
# @Version :1.0
# @Descriptioon :
# @Link :
# @File :  python发送邮件.py
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE

# 邮件服务器配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'your_email@gmail.com'
SMTP_PASSWORD = 'your_password'

# 收件人和邮件内容配置
TO = ['recipient1@example.com', 'recipient2@example.com']
SUBJECT = 'Test Email from Python'
BODY = 'This is a test email sent from Python.'

# 创建邮件对象
msg = MIMEMultipart()
msg['From'] = SMTP_USER
msg['To'] = COMMASPACE.join(TO)
msg['Subject'] = Header(SUBJECT, 'utf-8')

# 添加邮件正文
msg.attach(MIMEText(BODY, 'plain', 'utf-8'))

# 添加附件
filename = 'example.txt'
with open(filename, 'rb') as f:
    part = MIMEApplication(f.read(), Name=filename)
    part['Content-Disposition'] = 'attachment; filename="%s"' % filename
    msg.attach(part)

# 发送邮件
try:
    smtp = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtp.starttls()
    smtp.login(SMTP_USER, SMTP_PASSWORD)
    smtp.sendmail(SMTP_USER, TO, msg.as_string())
    smtp.quit()
    print('邮件发送成功.')
except Exception as e:
    print('邮件发送失败:', e)