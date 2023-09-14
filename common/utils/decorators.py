#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: decorators.py
@time: 2023/3/21 17:41
@desc:
"""
import json
import subprocess
import sys
from functools import wraps

import yaml


def singleton(cls):
	"""
	Args:
	cls:Decorated class
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
	"""Retry on Failed Requests"""
	from common.utils.exceptions import RequestSendingError
	
	def request_decorator(func):
		e = None
		
		@wraps(func)
		def wrapper(*args, **kwargs):
			nonlocal e
			
			for i in range(retries):
				# st = time.time()
				try:
					response = func(*args, **kwargs)
					# print(f"| 代码耗时--> {time.time() - st}")
					print(f"| 请求地址 --> {response.request.url}")
					print(f"| 请求方法 --> {response.request.method}")
					print(f"| 请求头 --> {response.request.headers}")
					print(f"| 请求 body --> {response.request.body}")
					print(f"| 接口状态--> {response.status_code}")
					print(f"| 接口耗时--> {response.elapsed}")
					try:
						print(f"| 接口响应--> {response.json()}")
					except:
						print(f"| 接口响应--> {response.text}")
				except Exception as error:
					print(f"| 第{i + 1}次请求参数=【{args}__{kwargs}】")
					# print(f"| 代码耗时--> {time.time() - st}")
					e = error
					time.sleep(delay)
				else:
					return response
			raise RequestSendingError(f"{args}__{kwargs}", e)
		
		return wrapper
	
	return request_decorator


def list_data(datas):
	"""
	:param datas: Test data
	:return:
	"""
	
	def wrapper(func):
		setattr(func, "PARAMS", datas)
		return func
	
	return wrapper


def yaml_data(file_path):
	"""
	:param file_path:YAML file path
	:return:
	"""
	
	def wrapper(func):
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				datas = yaml.load(f, Loader=yaml.FullLoader)
		except:
			with open(file_path, "r", encoding="gbk") as f:
				datas = yaml.load(f, Loader=yaml.FullLoader)
		setattr(func, "PARAMS", datas)
		return func
	
	return wrapper


def json_data(file_path):
	"""
	:param file_path: YAML file path
	:return:
	"""
	
	def wrapper(func):
		try:
			with open(file_path, "r", encoding="utf-8") as f:
				datas = json.load(f)
		except:
			with open(file_path, "r", encoding="gbk") as f:
				datas = json.load(f)
		setattr(func, "PARAMS", datas)
		return func
	
	return wrapper


import time


def run_count(count, interval, func, *args, **kwargs):
	"""Run Count"""
	for i in range(count):
		try:
			func(*args, **kwargs)
		except Exception as e:
			# print("====用例执行失败===", e)
			# traceback.print_exc()
			if i + 1 == count:
				raise e
			else:
				print("==============开始第{}次重运行=============".format(i))
				time.sleep(interval)
		else:
			break


def rerun(count, interval=2):
	"""
	 Decorator for rerunning a single test case; note that if using ddt, this method should be used before ddt
	:param count: Number of retries on failure
	:param interval: Interval time between each retry, default is three seconds
	:return:
	"""
	
	def wrapper(func):
		def decorator(*args, **kwargs):
			run_count(count, interval, func, *args, **kwargs)
		
		return decorator
	
	return wrapper


def install_dependencies(func):
	"""Checking and Installing Dependencies"""
	
	@wraps(func)
	def wrapper(*args, **kwargs):
		
		try:
			print("---------------- Checking and Installing Dependencies ----------------")
			subprocess.check_call(["pipenv", "install"])
			print("---------------- Successfully Installed All Dependencies ----------------")
		
		except Exception as e:
			print(f"Failed to install dependencies: {str(e)}")
			sys.exit(1)
		else:
			return func(*args, **kwargs)
	
	return wrapper


def send_request_decorator(func):
	"""Decorator to handle the logic of sending requests."""
	
	def decorator(self, host, method, extract_request_data, scripts_dir, prepost_script):
		"""Handles setup, request execution, and teardown logic for sending requests.

			   Args:
				   self: The instance of the class.
				   host: The host for the request.
				   method: The HTTP method for the request.
				   extract_request_data: Data for extracting request details.
				   scripts_dir: The script dir.
				   prepost_script: The prepost script name.

			   Returns:
				   The response from the request.
			   """
		setup_script, teardown_script = self.script(self.variables)
		# 执行 excel 与 指定模块文件中的动态代码
		self.execute_dynamic_code(self.variables, setup_script)
		self.execute_prepost_script(scripts_dir, prepost_script, "setup")
		response = func(self, host, method, extract_request_data, scripts_dir, prepost_script)
		self.execute_dynamic_code(self.response, teardown_script)
		self.execute_prepost_script(scripts_dir, prepost_script, "teardown")
		return response
	
	return decorator
