#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: decorators.py
@time: 2023/3/21 17:41
@desc:
"""
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


def request_decorator(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			print(f"发送请求的参数： {kwargs}")
			response = func(*args, **kwargs)
			print(f"请求地址 --> {response.request.url}")
			print(f"请求头 --> {response.request.headers}")
			print(f"请求 body --> {response.request.body}")
			print(f"接口状态--> {response.status_code}")
			print(f"接口耗时--> {response.elapsed}")
			print(f"接口响应--> {response.text}")
			return response
		except Exception as e:
			print(f"接口异常--> {e}")
			raise e
	
	return wrapper
