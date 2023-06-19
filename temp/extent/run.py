#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: run.py
@time: 2023/6/16 16:52
@desc:
"""
import requests

from temp.extent.hooks_decorator import before_decorator, after_decorator


@after_decorator
@before_decorator
def test_user_registration(url, method, **kwargs):
    requests.request(method, url, **kwargs)


if __name__ == "__main__":
    kwg = {}
    test_user_registration("http://jsonplaceholder.typicode.com/posts/2", "get", **kwg)
