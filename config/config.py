#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: config.py
@time: 2023/3/27 8:40
@desc: 全局配置文件
"""

import os


class Config:
    # 根目录路径
    BASE_URL = os.path.abspath(os.path.dirname(__file__))
    # 父目录路径
    PARENT_DIR = os.path.dirname(BASE_URL)

    # 测试数据所在路径
    TEMPLATES = os.path.join(PARENT_DIR, "src", "templates", "template.xlsx")  # 用例模板文件
    TEST_CASE = os.path.join(PARENT_DIR, "src", "cases", "test_openapi_cases.xlsx")
    # TEST_CASE = os.path.join(PARENT_DIR, "src", "cases", "test_cases.xlsx")
    TEST_FILES = os.path.join(PARENT_DIR, 'src', 'files')  # 用来上传文件的文件夹

    # 测试用例脚本目录
    SCRIPT = os.path.join(PARENT_DIR, "test_script")
    SCRIPTS_DIR = os.path.join(PARENT_DIR, "scripts")

    # 测试报告及 logger 所在路径
    TEST_REPORT = os.path.join(PARENT_DIR, "OutPut", "reports")
    TEST_REPORT_FILE = os.path.join(PARENT_DIR, "OutPut", "reports", "report.html")
    LOG_PATH = os.path.join(PARENT_DIR, "OutPut", "log")

    # 邮件配置信息
    MAIL_NOTICE = {
        "host": "smtp.qq.com",  # 邮件服务地址
        "user": "262667641@qq.com",  # 用户名
        "password": "xnvmmcchcxghbgfi",  # 密码（部分邮箱为授权码）# 密码
        "sender": "262667641@qq.com",  # 发送人
        "port": 465,  # smtp 端口号
        "receivers": ['262667641@qq.com']  # 接收方的邮箱
    }

    # 企业微信机器人配置信息
    WeChat_NOTICE = {
        "send_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8b1647d4-dc32-447c-b524-548acf18a938",
        "upload_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?type=file&key=8b1647d4-dc32-447c-b524-548acf18a938",
        "file_lists": [TEST_REPORT_FILE, TEST_CASE]  # 需要推送的文件的路径
    }

    # 钉钉机器人配置信息
    DINGTALK_NOTICE = {
        "url": "https://oapi.dingtalk.com/robot/send?access_token=7d1e11079e00a4ca9f11283f526349abd5ba3f792ef7bcb346909ff215af02de",
        "secret": "SEC441dbbdb8dbe150e5fc3e348bb449d3113b1be1a90be527b898ccd78c51566c1",
        "key": "",  # 安全关键字
        "atMobiles": "1827813600",  # 需要@指定人员的手机号
        "isAtAll": True,  # 是否@ 所有人
        "except_info": False  # 是否发送测试不通过的异常数据
    }


if __name__ == '__main__':
    test = Config()
    print(test.BASE_URL)
    print("测试用例", test.TEST_CASE)
    print("测试报告", test.TEST_REPORT)
    print("测试脚本", test.SCRIPTS_DIR)
