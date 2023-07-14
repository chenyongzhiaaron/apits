#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: action.py
@time: 2023/6/21 17:44
@desc:
"""
import ast

from common.crypto.encrypt_data import EncryptData
from common.utils.decorators import singleton
from common.utils.load_and_execute_script import LoadScript
from common.validation.extractor import Extractor
from common.validation.validator import Validator


@singleton
class Action(Extractor, LoadScript, Validator):
	def __init__(self, initialize_data=None, bif_functions=None):
		super().__init__()
		self.encrypt = EncryptData()
		self.__variables = {}
		self.set_environments(initialize_data)
		self.set_bif_fun(bif_functions)
	
	def execute_dynamic_code(self, item, code):
		self.set_variables(item)
		if code is not None:
			try:
				ast_obj = ast.parse(code, mode='exec')
				compiled = compile(ast_obj, '<string>', 'exec')
				exec(compiled, {"pm": self})
			except SyntaxError as e:
				error_message = f'动态代码语法异常: {e}'
				self._handle_error(error_message)
			except Exception as e:
				error_message = f"动态代码执行异常: {e}"
				self._handle_error(error_message)
			finally:
				return self.__variables
		return item
	
	def _handle_error(self, error_message):
		print(f'发现异常: {error_message}')
	
	def set_variables(self, item):
		self.__variables = item
	
	def update_variables(self, key, value):
		self.__variables[f"{{{{{key}}}}}"] = value
	
	def get_variables(self, key=None):
		"""获取依赖表 或 依赖表中key对应的值"""
		return self.__variables if not key else self.__variables.get(key)
	
	def analysis_request(self, request_data, headers_crypto, headers, request_crypto, extract_request_data):
		# 请求头及body加密或者加签
		headers, request_data = self.encrypt.encrypts(headers_crypto, headers, request_crypto, request_data)
		# 提取请求参数信息
		if extract_request_data is not None and request_data is not None:
			self.substitute_data(request_data, jp_dict=extract_request_data)
		return headers, request_data
	
	def send_request(self, host, url, method, teardown_script, **kwargs):
		response = self.http_client(host, url, method, **kwargs)
		self.execute_dynamic_code(response, teardown_script)
		return response
