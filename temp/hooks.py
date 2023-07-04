#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: hooks.py
@time: 2023/6/16 16:52
@desc:
"""
import requests


class Hooks:
	def __init__(self):
		self.before_request_funcs = []
		self.after_request_funcs = []
	
	def before_request(self, func):
		"""
		注册 before_request 钩子函数
		"""
		self.before_request_funcs.append(func)
		return func
	
	def after_request(self, func):
		"""
		注册 after_request 钩子函数
		"""
		self.after_request_funcs.append(func)
		return func
	
	def execute_hooks(self, url, method, **kwargs):
		"""
		执行所有的钩子函数
		"""
		for func in self.before_request_funcs:
			kwargs = func(url, method, **kwargs)
		
		response = requests.request(method, url, **kwargs)
		
		for func in self.after_request_funcs:
			response = func(response)
		
		return response


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
