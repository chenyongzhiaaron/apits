# -*- coding:utf-8 -*-
import re
from dataclasses import dataclass


@dataclass
class Variables:
	variables = {}
	pattern_l = re.compile(r"{{\s*([^}\s]+)\s*}}(?:\[(\d+)\])?")
	PATTERN = re.compile(r"{{(.*?)}}")  # 预编译正则表达式
	pattern = re.compile(r'({)')
	pattern_fun = re.compile(r"{{(\w+\(\))}}")
	
	@classmethod
	def update_variable(cls, key, value):
		"""更新依赖表"""
		cls.variables[f"{{{{{key}}}}}"] = value
	
	@classmethod
	def get_variable(cls, key=None):
		"""获取依赖表 或 依赖表中key对应的值"""
		return cls.variables if not key else cls.variables.get(key)
	
	@classmethod
	def set_variable(cls, value):
		"""设置依赖表"""
		cls.variables = value
	
	@classmethod
	def reset(cls):
		"""重置"""
		cls.variables.clear()
		cls.request = None
		cls.response = None


if __name__ == '__main__':
	from common.file_handling.do_excel import DoExcel
	from common.config import Config
	
	test_file = Config.test_case
	do_excel = DoExcel(test_file)
	init_case = do_excel.get_excel_init()
	d = Variables
	d.set_variable(init_case)
	print("--------------------->", d.get_variable())