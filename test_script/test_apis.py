#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: test_g.py
@time: 2023/6/20 16:49
@desc:
"""

import sys
import time
import unittest

sys.path.append("../../")
sys.path.append("../common")
from ddt import ddt, data

from common.action import Action
from common import bif_functions
from common.config import Config
from common.database.mysql_client import MysqlClient
from common.file_handling.do_excel import DoExcel
from common.utils.mylogger import MyLogger

# from common.crypto.encrypt_data import EncryptData

test_file = Config.test_api  # 获取 excel 文件路径
excel = DoExcel(test_file)
init_data, test_case = excel.get_excel_init_and_cases()

databases = init_data.get('databases')  # 获取数据库配置信息
mysql = MysqlClient(databases)  # 初始化 mysql 链接

logger = MyLogger()
initialize_data = eval(init_data.get("initialize_data"))
host = init_data.get('host', "") + init_data.get("path", "")


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None
    action = Action()

    @classmethod
    def setUpClass(cls) -> None:
        cls.action.set_bif_fun(bif_functions)  # 加载内置方法
        cls.action.set_variable(initialize_data)

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        print("Item Type:", type(item))
        print("Item Content:", item)
        sheet, item_id, st, name, description, headers_crypto, request_crypto, method = self.extract_base_info(item)
        if self.is_run(item):
            return

        self.pause_execution(st)  # 暂存

        self.replace_and_execute_sql(item)  # 执行 sql

        prepost_script = f"prepost_script_{sheet}_{item_id}.py"
        item = self.execute_pre_script(Config.SCRIPTS_DIR, prepost_script, "setup", item)

        item = self.replace_dependent_parameters(item)
        # 检查item的内容

        url, query_str, request_data_type, request_data, headers, expected = self.__request_info(item)
        regex, keys, deps, jp_dict, extract_request_data = self.__extractor_info(item)

        self.extract_request_data(request_data, extract_request_data)

        headers, request_data = self.action.encrypt_data.encrypt_data(headers_crypto, headers, request_crypto,
                                                                      request_data)

        kwargs = {request_data_type: request_data, 'headers': headers}
        response = self.action.http_client(host, url, method, **kwargs)

        self.execute_post_script(Config.SCRIPTS_DIR, prepost_script, "teardown", response)
        response_text = response.text if response is not None else str(response)
        result = "PASS"
        result_tuple = ''
        try:
            result_tuple = self.validate_response(expected, response)
        except Exception as e:
            result = "FAIL"
            logger.error(f"测试用例执行失败：{sheet}_{item_id}_{name}_{description}:\ne")
            raise e
        else:
            self.extract_response_data(response, regex, keys, deps, jp_dict)
        finally:
            excel.write_back(sheet_name=sheet, i=item_id, response=response_text, test_result=result,
                             assert_log=result_tuple)

    def setUp(self) -> None:
        print("*********,", self.action.get_variable())

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info(f"所有用例执行完毕")

    def extract_base_info(self, item):
        sheet = item.pop("sheet")
        item_id = item.pop("Id")
        sleep_time = item.pop("Time")
        name = item.pop("Name")
        description = item.pop("Description")
        headers_crypto = item.pop("Headers Crypto")
        request_data_crypto = item.pop("Request Data Crypto")
        method = item.pop("Method")
        return sheet, item_id, sleep_time, name, description, headers_crypto, request_data_crypto, method

    def __extractor_info(self, item):
        regex = item.pop("Regex")
        keys = item.pop("Regex Params List")
        deps = item.pop("Retrieve Value")
        jp_dict = item.pop("Jsonpath")
        extract_request_data = item.pop("Extract Request Data")
        return regex, keys, deps, jp_dict, extract_request_data

    def __request_info(self, item):
        print("Item Type:", type(item))
        print("Item Content:", item)
        url = item.pop("Url")
        query_str = item.pop("Query Str")
        request_data = item.pop("Request Data")
        headers = item.pop("Headers")
        expected = item.pop("Expected")
        request_data_type = item.pop("Request Data Type")

        return url, query_str, request_data_type, request_data, headers, expected

    def is_run(self, item):
        is_run = item.pop("Run")
        if not is_run or is_run.upper() != "YES":
            return True

    def pause_execution(self, sleep_time):
        if sleep_time:
            try:
                time.sleep(int(sleep_time))
            except Exception as e:
                logger.error(f'暂停时间必须是数字')
                raise e

    def replace_and_execute_sql(self, item):
        sql = item.pop("SQL")
        sql = self.action.replace_dependent_parameter(sql)
        if sql:
            try:
                execute_sql_results = mysql.do_mysql(sql)
                sql_params_dict = item.pop("Sql Params Dict")
                if execute_sql_results and sql_params_dict:
                    self.extract_request_data(execute_sql_results, jp_dict=sql_params_dict)
                    if method == "SQL" and mysql:
                        return None
            except Exception as e:
                logger.error(f'执行 sql 失败:{sql},异常信息:{e}')
                raise e
        return sql

    def execute_pre_script(self, scripts_dir, script_name, function_name, item):
        return self.action.load_and_execute_script(scripts_dir, script_name, function_name, item)
        # return self.action.load_and_execute_script(scripts_dir, script_name, function_name, item)

    def replace_dependent_parameters(self, item):
        item = self.action.replace_dependent_parameter(item)
        return item

    def execute_post_script(self, scripts_dir, script_name, function_name, response):
        return self.action.load_and_execute_script(scripts_dir, script_name, function_name, response)

    def validate_response(self, expected, response):
        result_tuple = self.action.run_validate(expected, response.json())
        self.assertNotIn("FAIL", result_tuple, "FAIL 存在结果元组中")
        return result_tuple

    def extract_request_data(self, data, jp_dict=None):
        self.action.substitute_data(data, jp_dict=jp_dict)

    def extract_response_data(self, response, regex, keys, deps, jp_dict):
        try:
            self.action.substitute_data(response.json(), regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
        except Exception as e:
            logger.error(f"\nregex={regex}\nkeys={keys}\ndeps={deps}\njp_dict={jp_dict}")


if __name__ == '__main__':
    unittest.main()
