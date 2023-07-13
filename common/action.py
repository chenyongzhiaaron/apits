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
from common.utils.load_and_execute_script import LoadScript
from common.utils.singleton import singleton
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
				error_message = f'Syntax error in dynamic code: {e}'
				self._handle_error(error_message)
			except Exception as e:
				error_message = f"Error executing dynamic code: {e}"
				self._handle_error(error_message)
			finally:
				return self.__variables
		return item
	
	def _handle_error(self, error_message):
		print(f'Error occurred: {error_message}')
	
	def set_variables(self, item):
		self.__variables = item
	
	def update_variables(self, key, value):
		self.__variables[f"{{{{{key}}}}}"] = value
	
	def get_variables(self, key=None):
		"""获取依赖表 或 依赖表中key对应的值"""
		return self.__variables if not key else self.__variables.get(key)
	
	def analysis_request(self, request_data, jp_dict, headers_crypto, headers, request_crypto):
		# 提取请求参数信息
		self.substitute_data(request_data, jp_dict=jp_dict)
		# 请求头及body加密或者加签
		headers, request_data = self.encrypt.encrypts(headers_crypto, headers, request_crypto, request_data)
		return headers, request_data
