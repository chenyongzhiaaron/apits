# coding: utf-8
# -------------------------------------------------------------------------------
# Name:         validator.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2023/03/24 17:32
# -------------------------------------------------------------------------------
import json

from common.validation import logger
from common.validation.comparator_dict import comparator_dict
from common.validation.extractor import Extractor
from common.validation.loaders import Loaders


class Validator(Loaders):
	"""
	校验器
	主要功能：
		1、格式化校验变量
		2、校验期望结果与实际结果与预期一致，并返回校验结果
	"""
	validate_variables_list = []
	built_in_comparators = Loaders.load_built_in_comparators()
	
	def __init__(self):
		super().__init__()
	
	def uniform_validate(self, validate_variables):
		"""
		统一格式化测试用例的验证变量validate
		Args:
			validate_variables: 参数格式 list、dict
				示例：
					[{"check":"result.user.name","comparator":"eq","expect":"chenyongzhi"}]
					or {"check":"result.user.name","comparator":"eq","expect":"chenyongzhi"}

		Returns: 返回数据格式 list
				示例：
					[{"check":"result.user.name","comparator":"eq","expect":"chenyongzhi"}]

		"""
		if isinstance(validate_variables, str):
			validate_variables = json.loads(validate_variables)
		if isinstance(validate_variables, list):
			for item in validate_variables:
				self.uniform_validate(item)
		elif isinstance(validate_variables, dict):
			if "check" in validate_variables.keys() and "expect" in validate_variables.keys():
				# 如果验证mapping中不包含comparator时，默认为{"comparator": "eq"}
				check_item = validate_variables.get("check")
				expect_value = validate_variables.get("expect")
				comparator = validate_variables.get("comparator", "eq")
				self.validate_variables_list.append({
					"check": check_item,
					"expect": expect_value,
					"comparator": comparator,
					# "check_rt": check_rt
				})
		else:
			logger.error("参数格式错误！")
	
	def validate(self, resp_obj=None):
		"""
		校验期望结果与实际结果与预期一致
		Args:
			resp_obj: ResponseObject对象实例

		Returns:

		"""
		
		validate_pass = "PASS"
		
		# 记录校验失败的原因
		failure_reason = []
		for validate_variable in self.validate_variables_list:
			check_item = validate_variable['check']
			expect_value = validate_variable['expect']
			comparator = validate_variable['comparator']
			actual_value = Extractor.extract_value_by_jsonpath(resp_obj=resp_obj, expr=check_item)
			try:
				# 获取比较器
				fun = self.built_in_comparators[comparator]
				
				fun(actual_value=actual_value, expect_value=expect_value)
			except (AssertionError, TypeError):
				validate_pass = "FAIL"
			finally:
				failure_reason.append({
					'检查项': check_item,
					'期望值': expect_value,
					'实际值': actual_value,
					'断言方法': comparator_dict.get(comparator),
				})
		return validate_pass, failure_reason
	
	def run_validate(self, validate_variables, resp_obj=None):
		"""
		 统一格式化测试用例的验证变量validate，然后校验期望结果与实际结果与预期一致
		Args:
			validate_variables:参数格式 list、dict
			resp_obj:ResponseObject对象实例

		Returns:返回校验结果

		"""
		if not validate_variables:
			return ""
		# 清空校验变量
		self.validate_variables_list.clear()
		self.uniform_validate(validate_variables)
		if not self.validate_variables_list:
			raise "uniform_validate 执行失败，无法进行 validate 校验"
		return self.validate(resp_obj)


if __name__ == '__main__':
	validate_variables1 = {"check": "$.result.user.name", "comparator": "eq", "expect": "chenyongzhi"}
	validate_variables2 = [
		{"check": "code", "comparator": "eq", "expect": "200"},
		{"check": "result.user.name", "comparator": "eq", "expect": "chenyongzhi"}
	]
	resp_obj = {"code": "200", "result": {"user": {"name": "chenyongzhi"}}}
	validator = Validator()
	print(validator.run_validate(validate_variables1, resp_obj))
	print(validator.run_validate(validate_variables2, resp_obj))
	print(validator.run_validate(validate_variables2, resp_obj))
