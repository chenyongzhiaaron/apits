# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         extractor.py
# Description:  提取器
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2020/2/25 16:48
# -------------------------------------------------------------------------------

import json

import jsonpath

from common.validation import logger


class Extractor:
	"""
	提取器
	主要功能：
		1、格式化输出变量
		2、从响应中提取需要输出的变量信息并返回
	"""
	
	def __init__(self):
		self.output_variables_mapping = {}
	
	def uniform_output(self, output_variables):
		"""
		统一格式化测试用例的输出变量output
		Args:
			output_variables: list、dict、str 示例：["a","b",{"a":"ac"}] or {"a":"ac"} or "a"
	
		Returns: 示例：[{"alias_key":"original_key"}]
			list
		"""
		if isinstance(output_variables, list):
			for output_variable in output_variables:
				self.uniform_output(output_variable)
		elif isinstance(output_variables, dict):
			for alias_key, original_key in output_variables.items():
				if not isinstance(alias_key, str):
					alias_key = json.dumps(alias_key, ensure_ascii=False)
				if not isinstance(original_key, str):
					original_key = json.dumps(original_key, ensure_ascii=False)
				self.output_variables_mapping.update({alias_key: original_key})
		elif isinstance(output_variables, str):
			self.output_variables_mapping.update({output_variables: output_variables})
		else:
			raise Exception("参数格式错误！")
	
	def extract_output(self, resp_obj=None):
		"""
		从接口返回中提取待输出变量的值
		Args:
			resp_obj: ResponseObject对象的resp_obj属性
	
		Returns: output_variables_mapping 从resp_obj中提取后的mapping
	
		"""
		return {alias_key: self.extract_value_by_jsonpath(resp_obj=resp_obj, expr=original_key) for
		        alias_key, original_key in self.output_variables_mapping.items()}
	
	@staticmethod
	def extract_value_by_jsonpath(resp_obj=None, expr=None):
		"""
		根据jsonpath从resp_obj中提取相应的值
		Args:
			resp_obj: ResponseObject实例
			expr: 提取条件
	
		Returns:
	
		"""
		# logger.debug(f'正在执行数据提取：提取数据源内容：{resp_obj},{type(resp_obj)}')
		# logger.debug('正在执行数据提取：提取表达式：{expr}'.format(expr=expr))
		try:
			result = jsonpath.jsonpath(resp_obj if isinstance(resp_obj, (dict, list)) else json.dumps(resp_obj), expr)
		except Exception as e:
			return expr
		else:
			if result is False:
				result = []
				logger.error(f'提取失败：提取表达式：{expr}，没有提取到对应的值')
			elif isinstance(result, list):
				if len(result) == 1:
					result = result[0]
				# logger.info(f'提取成功，输出结果，提取表达式：{expr}，提取结果：{result}')
			return result


if __name__ == '__main__':
	r_obg = {"data": ["key", 1, "val", 2]}
	Extractor.extract_value_by_jsonpath(r_obg, "$.data[0]")
	Extractor.extract_value_by_jsonpath(r_obg, 200)
