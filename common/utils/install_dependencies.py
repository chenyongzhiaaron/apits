#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: install_dependencies.py
@time: 2023/8/9 15:15
@desc: 安装 Pipfile 中的依赖
"""
import subprocess
import sys


def install_dependencies():
    try:
        print("---------------- 檢測并且安装依赖文件 ----------------")
        subprocess.check_call(["pipenv", "install"])
        print("---------------- 成功安装所有依赖文件 ----------------")

    except Exception as e:
        print(f"Failed to install dependencies: {str(e)}")
        sys.exit(1)
