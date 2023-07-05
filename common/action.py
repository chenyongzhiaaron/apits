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
	def __init__(self):
		super().__init__()
		self.encrypt = EncryptData()
		self.vars = {}
	
	def execute_dynamic_code(self, code):
		try:
			ast_obj = ast.parse(code, mode='exec')
			compiled = compile(ast_obj, '<string>', 'exec')
			exec(compiled, {"action": self})
			print("exec dynamic code  success")
			return self.vars
		except SyntaxError as e:
			error_message = f'Syntax error in dynamic code: {e}'
			self._handle_error(error_message)
		except Exception as e:
			error_message = f"Error executing dynamic code: {e}"
			self._handle_error(error_message)
	
	def _handle_error(self, error_message):
		print(f'Error occurred: {error_message}')
	
	def send_request(self, host, url, method, **kwargs):
		self.http_client(host, url, method, **kwargs)
