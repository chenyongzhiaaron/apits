#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: exceptions.py
@time: 2023/8/1 9:12
@desc:
"""


class MyBaseException(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg


class RequestSendingError(MyBaseException):
    """请求异常"""
    ERROR_CODE = 1001
    
    def __init__(self, url, reason):
        msg = f"请求异常：URL={url}, 原因={reason}"
        super().__init__(msg)


class DatabaseExceptionError(MyBaseException):
    """数据库异常"""
    ERROR_CODE = 1002
    
    def __init__(self, operation, reason):
        msg = f"数据库异常：操作={operation}, 原因={reason}"
        super().__init__(msg)


class ParameterExtractionError(MyBaseException):
    """参数提取异常"""
    ERROR_CODE = 1003
    
    def __init__(self, parameter_path, reason):
        msg = f"参数提取异常：参数路径={parameter_path}, 原因={reason}"
        super().__init__(msg)


class ParameterReplacementError(MyBaseException):
    """参数替换异常"""
    ERROR_CODE = 1004
    
    def __init__(self, parameter_name, reason):
        msg = f"参数替换异常：参数名称={parameter_name}, 原因={reason}"
        super().__init__(msg)


class AssertionFailedError(MyBaseException):
    """断言异常"""
    ERROR_CODE = 1005
    
    def __init__(self, assertion_name, actual_value, expected_value):
        msg = f"断言失败：断言名称={assertion_name}, 实际值={actual_value}, 期望值={expected_value}"
        super().__init__(msg)


class ExecuteDynamiCodeError(MyBaseException):
    """执行动态代码异常"""
    ERROR_CODE = 1006
    
    def __init__(self, code, reason):
        msg = f"执行动态代码异常：动态代码={code}, 原因={reason}"
        super().__init__(msg)
