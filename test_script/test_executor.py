#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: test_executor.py
@time: 2023/7/21 17:44
@desc:
"""
import unittest

from ddt import ddt, data

from common import bif_functions
from common.utils.action import Action
from config import Config
from common.file_handling.do_excel import DoExcel
from extensions import dynamic_scaling_methods

test_file = Config.test_case  # 获取 excel 文件路径
excel = DoExcel(test_file)

test_case, databases, initialize_data, host = excel.get_excel_init_and_cases()


@ddt
class TestProjectApi(unittest.TestCase):
	maxDiff = None
	action = Action(initialize_data, bif_functions, databases)
	
	@classmethod
	def setUpClass(cls) -> None:
		pass
	
	def setUp(self) -> None:
		self.action.set_bif_fun(dynamic_scaling_methods)
	
	@data(*test_case)
	def test_api(self, item):
		sheet, iid, condition, st, name, desc, h_crypto, r_crypto, method, expected = self.action.base_info(item)
		if self.action.is_run(condition):
			self.skipTest("这个测试用例听说泡面比较好吃，所以放弃执行了！！")
		regex, keys, deps, jp_dict, ex_request_data = self.action.extractor_info(item)
		setup_script, teardown_script = self.action.script(item)
		self.action.pause_execution(st)
		
		# 首执行 sql
		self.action.exc_sql(item)
		if method.upper() == 'SQL':
			self.skipTest("这条测试用例被 SQL 吃了，所以放弃执行了！！")
		
		# 执行动态代码
		item = self.action.execute_dynamic_code(item, setup_script)
		
		# prepost_script = f"prepost_script_{sheet}_{iid}.py"
		# item = self.action.load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "setup", item)
		
		# 修正参数
		item = self.action.replace_dependent_parameter(item)
		url, query_str, request_data, headers, request_data_type = self.action.request_info(item)
		
		# 分析请求参数信息
		headers, request_data = self.action.analysis_request(request_data, h_crypto, headers, r_crypto, ex_request_data)
		result_tp = None
		result = "PASS"
		
		# 执行请求操作
		kwargs = {request_data_type: request_data, 'headers': headers, "params": query_str}
		response = self.action.send_request(host, url, method, teardown_script, **kwargs)
		
		try:
			# 提取响应
			self.action.substitute_data(response.json(), regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
		except Exception as err:
			self.action.logger.error(f"提取响应失败：{sheet}_{iid}_{name}_{desc}"
			                         f"\nregex={regex};"
			                         f" \nkeys={keys};"
			                         f"\ndeps={deps};"
			                         f"\njp_dict={jp_dict}"
			                         f"\n{err}")
		
		# 修正断言
		expected = self.action.replace_dependent_parameter(expected)
		try:
			# print(f"期望结果--> {expected}")
			# 执行断言 返回结果元组
			self.action.run_validate(expected, response.json())
		except Exception as e:
			result = "FAIL"
			self.action.logger.error(f'异常用例: **{sheet}_{iid}_{name}_{desc}**\n{e}')
			raise e
		finally:
			print(f"断言结果-->", self.action.assertions)
			response = response.text if response is not None else str(response)
			# 响应结果及测试结果回写 excel
			excel.write_back(sheet_name=sheet, i=iid, response=response, test_result=result,
			                 assert_log=str(self.action.assertions))
	
	@classmethod
	def tearDownClass(cls) -> None:
		excel.close_excel()
		cls.action.logger.info(f"所有用例执行完毕")


if __name__ == '__main__':
	unittest.main()
