#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: common_setup_teardown.py
@time: 2023/6/20 10:10
@desc:
"""


def common_setup_teardown(func):
    def wrapper(item):
        sheet = item.pop("sheet")
        item_id = item.pop("Id")
        name = item.pop("Name")
        description = item.pop("Description")
