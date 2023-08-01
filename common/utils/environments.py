# -*- coding:utf-8 -*-
import re
from dataclasses import dataclass


@dataclass
class Environments:
	environments = {}
	pattern_l = re.compile(r"{{\s*([^}\s]+)\s*}}(?:\[(\d+)\])?")
	PATTERN = re.compile(r"{{(.*?)}}")  # 预编译正则表达式
	pattern = re.compile(r'({)')
	pattern_fun = re.compile(r"{{(\w+\(\))}}")
	
	@classmethod
	def update_environments(cls, key, value):
		"""更新依赖表"""
		cls.environments[f"{{{{{key}}}}}"] = value
	
	@classmethod
	def get_environments(cls, key=None):
		"""获取依赖表 或 依赖表中key对应的值"""
		return cls.environments if not key else cls.environments.get(key)
	
	@classmethod
	def set_environments(cls, value):
		"""设置依赖表"""
		cls.environments = value
	
	@classmethod
	def reset_environments(cls):
		"""重置"""
		cls.environments.clear()


if __name__ == '__main__':
	from common.file_handling.do_excel import DoExcel
	from config import Config
	
	test_file = Config.test_case
	do_excel = DoExcel(test_file)
	init_case = do_excel.get_excel_init()
	d = Environments
	d.set_environments(init_case)
	print("--------------------->", d.get_environments())
