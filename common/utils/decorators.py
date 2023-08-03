#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: decorators.py
@time: 2023/3/21 17:41
@desc:
"""
import time
from functools import wraps


def singleton(cls):
    """
    Args:
    cls:被装饰类
    Returns:
    """
    instance = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]
    
    return get_instance


def request_retry_on_exception(retries=2, delay=1.5):
    def request_decorator(func):
        e = None
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal e
            for i in range(retries):
                try:
                    print(f"| 第{i + 1}次发送请求的参数： {kwargs}")
                    response = func(*args, **kwargs)
                    print(f"| 请求地址 --> {response.request.url}")
                    print(f"| 请求头 --> {response.request.headers}")
                    print(f"| 请求 body --> {response.request.body}")
                    print(f"| 接口状态--> {response.status_code}")
                    print(f"| 接口耗时--> {response.elapsed}")
                    print(f"| 接口响应--> {response.text}")

                except Exception as error:
                    e = error
                    time.sleep(delay)
                else:
                    return response
            raise Exception(f"| 请求重试**{retries}**次失败，请检查！！{e}")
        
        return wrapper
    
    return request_decorator
