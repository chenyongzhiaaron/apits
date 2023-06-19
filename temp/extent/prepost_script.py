#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: prepost_script.py
@time: 2023/6/16 16:58
@desc:
"""  # !/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: prepost_script.py
@time: 2023/6/16 16:58
@desc:
"""
from temp.extent.hooks_decorator import hooks  # 导入hooks对象


@hooks.before_request
def add_authentication_headers(url, method, **kwargs):
    """
    添加认证头信息
    """
    print("------开始执行前置操作-----")
    headers = kwargs.get('headers', {})
    headers["Authorization"] = "Bearer " + "这是token"
    kwargs['headers'] = headers
    return kwargs


@hooks.before_request
def handle_dependent_parameters(url, method, **kwargs):
    """
    处理依赖参数
    """
    print("------开始执行后置操作-----")
    payload = kwargs.get('json', {})
    payload["title"] = payload.get("title")
    kwargs['json'] = payload
    return kwargs
