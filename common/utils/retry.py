#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: retry.py
@time: 2023/3/15 11:15
@desc:
"""


def retry(func):
    "函数重跑"

    def run_again(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except:
            pass
    return run_again()