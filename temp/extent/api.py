#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: api.py
@time: 2023/6/13 16:09
@desc:
"""
import os

# api.py
# 这是一个api模块的示例
# 可以定义一些api相关的类或方法

import config
import requests


class Api:

    def __init__(self):
        # 初始化一些属性或参数
        self.session = requests.Session()

    def run_script(self, script_name, pm):
        # 定义一个方法，用来执行指定的脚本代码

        # 拼接脚本文件的完整路径
        script_path = os.path.join(config.SCRIPTS_DIR, script_name)

        # 打开脚本文件，并读取内容
        with open(script_path, "r", encoding="utf-8") as f:
            script_content = f.read()

        # 使用exec函数来执行脚本代码，并传递pm对象作为局部变量
        exec(script_content, {}, {"pm": pm})


class PM:

    def __init__(self):
        # 初始化一些属性或参数
        self.url = None
        self.params = None
        self.status_code = None
        self.content = None
        self.data = None

    def print(self, message):
        # 定义一个方法，用来打印一些信息
        print(message)
