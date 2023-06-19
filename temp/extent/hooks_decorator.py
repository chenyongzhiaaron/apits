#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: hooks_decorator.py
@time: 2023/6/16 17:03
@desc:
"""
from temp.extent.hooks import Hooks

hooks = Hooks()


def before_decorator(func):
    def wrapper(*args, **kwargs):
        # hooks.execute_hooks(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper


def after_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # hooks.execute_hooks(*args, **kwargs)
        return result

    return wrapper
