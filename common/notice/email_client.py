#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: email_client.py
@time: 2023/8/8 10:58
@desc:
"""
import smtplib
from email.header import Header  # 将各类信息定义成对象，比如标题等。
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart  # 定义带有附件的邮件对象
from email.mime.text import MIMEText

from config.config import Config


class SendEmail:
    """Send mail"""

    def __init__(self):
        """
        :param host: smtp server address
        :param port: smtp server report
        :param user: Email account number
        :param password: SMTP service authorization code of mailbox
        """
        # 邮箱服务器地址
        self.host = Config.MAIL_NOTICE.get("host")
        # 用户名
        self.user = Config.MAIL_NOTICE.get("user")
        # 密码(部分邮箱为授权码)
        self.password = Config.MAIL_NOTICE.get("password")
        # 邮件发送方邮箱地址
        self.sender = Config.MAIL_NOTICE.get("sender")
        # 25 为 SMTP 端口号
        self.port = Config.MAIL_NOTICE.get("port")
        # 定义接收放的邮箱(可以是多个)
        self.receivers = Config.MAIL_NOTICE.get("receivers")

    def content(self, content=None, file_path=None):
        """内容"""
        msg = MIMEMultipart()  # 如果一份邮件含有附件，则必须定义 multipart/mixed 类型
        msg['Form'] = Header(self.sender)
        msg['Subject'] = Header('接口自动化测试报告', 'utf-8')  # 主题
        msg['To'] = ','.join(self.receivers)

        # 编辑邮件
        # ---邮件正文内容---
        message = MIMEText(content, 'html', 'utf-8')
        msg.attach(message)
        # 测试用例与测试报告一起
        if file_path:
            for ph in file_path:
                filename = ph.split('\\')[-1]
                with open(ph, 'rb') as f:
                    ctx = f.read()
                part = MIMEApplication(ctx)
                part.add_header('Content-Disposition', 'attachment', filename=filename)
                msg.attach(part)  # 附件模块添加到 MIMEMultipart

        return msg.as_string()

    def send_mail(self, content, file_path=None):
        """发送邮件"""
        try:
            s = smtplib.SMTP_SSL(self.host, self.port)
            # s.starttls()
            s.login(self.user, self.password)
            s.sendmail(self.sender, self.receivers, self.content(content, file_path))
            s.quit()
        except Exception as e:
            print("发送邮件异常", e)
