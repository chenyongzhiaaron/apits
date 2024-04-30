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
from common.core.action import Action
from common.utils.decorators import list_data
from config.config import Config
from common.database.mysql_client import MysqlClient

test_file = Config.TEST_CASE  # 获取 excel 文件路径
excel = DoExcel(test_file)

# 获取测试用例、数据库、初始化数据和主机
test_case, databases, initialize_data, host = excel.get_excel_init_and_cases()


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.action = Action(host, initialize_data)
        cls.action.load_modules_from_folder(extensions)
        cls.action.client = MysqlClient(databases)
        cls.action.scripts_dir = Config.SCRIPTS_DIR

    def setUp(self) -> None:
        pass

    @list_data(test_case)
    def test_api(self, item):
        self.__class__.action.base_info(item)
        if not self.__class__.action.is_run():
            self.skipTest("这个测试用例听说泡面比较好吃，所以放弃执行了！！")
        # 用例暂停
        self.__class__.action.pause_execution()

        # 单独执行 sql
        if self.__class__.action.is_only_sql(self.__class__.action.client):
            self.skipTest("这条测试用例被 SQL 吃了，所以只执行 sql 语句！！")
        # 执行 sql 语句
        self.__class__.action.exec_sql(self.__class__.action.client)
        self.__class__.action.send_request()
        # 断言响应及提取响应信息
        self.__class__.action.analysis_response()
        self.__class__.action.execute_validation(excel)

    @classmethod
    def tearDownClass(cls) -> None:
        excel.close_excel()


if __name__ == '__main__':
    unittest.main()
