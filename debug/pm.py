#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: pm.py
@time: 2023/7/13 16:38
@desc:
"""


def setup(action):
    request_data = action.get_vars()  # 获取得到请求数据
    """
    request_data 的值:  {'Url': '/login',
     'Headers': '{"Content-Type": "application/json"}',
      'Query Str': None,
       'Request Data Type': 'params',
       'Request Data': '{"account": "{{account}}", "password": "{{passwd}}"}',
       'Expected': None, 'Response': '', 'Assertion': '', 'Error Log': ''
       }
    """
    #
    email_str = action.get_variable("{{email()}}") # 加入已经自定义了邮件函数 则这里获取到
    
    action.set_variable("userEmail", email_str)
