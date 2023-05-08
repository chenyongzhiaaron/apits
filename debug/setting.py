#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'YinJia'

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

sys.path.append(BASE_DIR)  # 当前文件的绝对路径
# 配置文件
TEST_CONFIG = os.path.join(BASE_DIR, "database", "config.ini")  # 拼接config.ini文件绝对路径

# 测试用例模板文件
SOURCE_FILE = os.path.join(BASE_DIR, "database", "DemoAPITestCase.xlsx")  # 同上

# excel测试用例结果文件
TARGET_FILE = os.path.join(BASE_DIR, "report", "excelReport", "DemoAPITestCase.xlsx")  # 同上

# 测试用例报告
TEST_REPORT = os.path.join(BASE_DIR, "report")  # 同上

# 测试用例程序文件
TEST_CASE = os.path.join(BASE_DIR, "testcase")  # 同上


# 请求配置
host = "mp-prod.smartmidea.net"  # 测试环境 https://mp-sit.smartmidea.net ； 生产环境 https://mp-prod.smartmidea.net
secret = "prod_secret123@muc"     # 测试环境sit_secret123@muc ；生产环境 prod_secret123@muc
Iot_key = "ad0ee21d48a64bf49f4fb583ab76e799"   # 测试环境:143320d6c73144d083baf9f5b1a7acc9   生产环境:ad0ee21d48a64bf49f4fb583ab76e799