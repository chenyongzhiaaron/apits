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

import extensions
from common.core.dataDriver import ddt
from common.file_handling.do_excel import DoExcel
from common.utils.action import Action
from common.utils.decorators import list_data
from config import Config

test_file = Config.TEST_CASE  # 获取 excel 文件路径
excel = DoExcel(test_file)

test_case, databases, initialize_data, host = excel.get_excel_init_and_cases()


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None
    action = Action(initialize_data, databases)

    @classmethod
    def setUpClass(cls) -> None:
        cls.action.load_modules_from_folder(extensions)

    def setUp(self) -> None:
        pass

    @list_data(test_case)
    def test_api(self, item):
        sheet, iid, condition, st, name, desc, h_crypto, r_crypto, method, expected = self.action.base_info(item)
        if self.action.is_run(condition):
            self.skipTest("这个测试用例听说泡面比较好吃，所以放弃执行了！！")
        regex, keys, deps, jp_dict, ex_request_data = self.action.extractor_info(item)
        setup_script, teardown_script = self.action.script(item)
        self.action.pause_execution(st)
        self.action.exc_sql(item)
        if method.upper() == 'SQL':
            self.skipTest("这条测试用例被 SQL 吃了，所以放弃执行了！！")
        item = self.action.execute_dynamic_code(item, setup_script)

        # prepost_script = f"prepost_script_{sheet}_{iid}.py"
        # item = self.action.load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "setup", item)

        item = self.action.replace_dependent_parameter(item)
        url, query_str, request_data, headers, request_data_type = self.action.request_info(item)
        headers, request_data = self.action.analysis_request(request_data, h_crypto, headers, r_crypto, ex_request_data)
        kwargs = {request_data_type: request_data, 'headers': headers, "params": query_str}
        self.action.send_request(host, url, method, teardown_script, **kwargs)
        self.action.analysis_response(sheet, iid, name, desc, regex, keys, deps, jp_dict)
        expected = self.action.replace_dependent_parameter(expected)
        self.action.execute_validation(excel, sheet, iid, name, desc, expected)

    @classmethod
    def tearDownClass(cls) -> None:
        excel.close_excel()


if __name__ == '__main__':
    unittest.main()
