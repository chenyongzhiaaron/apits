#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: singleton.py
@time: 2023/3/21 17:41
@desc:
"""


def singleton(cls):
    """
    单例模式装饰器
    Args:
        cls:被装饰类

    Returns:

    """
    instance = {}

    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance