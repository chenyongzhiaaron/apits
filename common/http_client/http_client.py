# -*- coding: utf-8 -*-
import json
import re
import sys

import requests
import urllib3

sys.path.append("../")
sys.path.append("./common")

from common.http_client import logger
# from common.data_extraction.data_extractor import DataExtractor
# from common.data_extraction.dependent_parameter import DependentParameter
from common.validation.load_modules_from_folder import LoadModulesFromFolder


# @singleton
class Pyt(LoadModulesFromFolder):
	# 类属性，保存一个会话对象，防止每次都创建一个新的会话，节省资源
	session = requests.Session()
	
	def __init__(self):
		super().__init__()
		self.request = None
		self.response = None
	
	# @staticmethod
	def log_decorator(msg="请求异常"):
		def decorator(func):
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
					logger.error(f"发送请求失败: {e}")
					return
			
			return wrapper
		
		return decorator
	
	# @log_decorator()
	def http_client(self, host, url, method, **kwargs):
		"""
		发送 http 请求
		@param host: 域名
		@param __url: 接口 __url
		@param method: http 请求方法
		# @param request_data_type: 请求数据类型
		# @param headers: 请求头部信息，默认为 None
		@param kwargs: 接受 requests 原生的关键字参数
		@return: 响应对象
		"""
		# 关闭 https 警告信息
		urllib3.disable_warnings()
		
		if not url:
			raise ValueError("URL cannot be None")
		__url = f'{host}{url}' if not re.match(r"https?", url) else url
		# 获取session 中的请求方法
		# func = getattr(session, method.lower())
		
		# 增加兼容
		# 处理 headers 参数为字符串类型的情况
		if 'headers' in kwargs and isinstance(kwargs['headers'], str):
			kwargs['headers'] = json.loads(kwargs['headers'])
		
		# 处理 json 参数为字符串类型的情况
		if 'json' in kwargs and isinstance(kwargs['json'], str):
			kwargs['json'] = json.loads(kwargs['json'])
		
		# 发送请求
		# return func(__url, verify=True, timeout=30, **kwargs)
		self.request = requests.Request(method, __url, **kwargs)
		self.response = self.session.send(self.request.prepare(), timeout=30, verify=True)
		
		return self.response


if __name__ == '__main__':
	hst = 'https://ibs-test.bzlrobot.com'
	url = '/api/ibs-auth/ibs_platform/login?t=168672334'
	method = 'post'
	kwargs = {
		'json': '{"account": "luoshunwen005", "grantType": "password", "isBip": "false","password": "o+t2SnEEylblxlfIspJUvGFa0gCDNrU2dC34LjVFqIiTmxa855YDBE/6J7eRVBGaQwR7mozSKComk9n6kjSNRjSX1m574dRZdESIeYsmM/xk2Nt5n5dqB268qCMivJMXpHQMygpT4RpDiYoOiEqlOi9eG5G7v/5rixHiZ9xv98m34xVD1VdlaCbphoB9JI7T9HmVFJniSWt01ruC5t+aFUvfxLjOpRmYmfz8GwtSd5XXKaKr29ce1C39Fg+PtqOkQ3cOLVS9hXgzz6s2zud0++T4vwgVtrHx86aMrrozhCdKzrQuWPEO1cSsaEaNVdSUsT54je+4O+xKzxkJhoGMnQ=="}',
		'headers': None}
	pyt = Pyt()
	pyt.http_client(hst, url, method, **kwargs)
	# print(pyt.request.json)
	# print(pyt.request.headers)
	# print(pyt.response.text)
