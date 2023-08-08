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
import time

from common import bif_functions
from common.crypto.encrypt_data import EncryptData
from common.database.mysql_client import MysqlClient
from common.utils.decorators import singleton
from common.utils.exceptions import *
from common.validation.extractor import Extractor
from common.validation.load_and_execute_script import LoadScript
from common.validation.validator import Validator


@singleton
class Action(Extractor, LoadScript, Validator):
    def __init__(self, initialize_data=None, db_config=None):
        super().__init__()
        self.db_config = db_config
        self.encrypt = EncryptData()
        self.__variables = {}
        self.set_environments(initialize_data)
        self.set_bif_fun(bif_functions)

    def execute_dynamic_code(self, item, code):
        self.variables = item
        if code is not None:
            try:
                ast_obj = ast.parse(code, mode='exec')
                compiled = compile(ast_obj, '<string>', 'exec')
                exec(compiled, {"pm": self})
            except SyntaxError as e:
                ExecuteDynamiCodeError(code, e)
            except TypeError as e:
                ExecuteDynamiCodeError(code, e)
            except Exception as e:
                ExecuteDynamiCodeError(code, e)

        return self.variables

    @property
    def variables(self, key=None):
        return self.__variables if not key else self.__variables.get(key)

    @variables.setter
    def variables(self, item):
        self.__variables = item

    def analysis_request(self, request_data, headers_crypto, headers, request_crypto, extract_request_data):
        headers, request_data = self.encrypt.encrypts(headers_crypto, headers, request_crypto, request_data)
        if extract_request_data is not None and request_data is not None:
            self.substitute_data(request_data, jp_dict=extract_request_data)
        return headers, request_data

    def send_request(self, host, url, method, teardown_script, **kwargs):
        self.http_client(host, url, method, **kwargs)
        self.update_environments("responseStatusCode", self.response.status_code)
        self.update_environments("responseTime", round(self.response.elapsed.total_seconds() * 1000, 2))
        self.execute_dynamic_code(self.response, teardown_script)

    def analysis_response(self, sheet, iid, name, desc, regex, keys, deps, jp_dict):
        try:
            self.substitute_data(self.response_json, regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
        except Exception as err:
            msg = f"| 分析响应失败：{sheet}_{iid}_{name}_{desc}"
            f"\nregex={regex};"
            f" \nkeys={keys};"
            f"\ndeps={deps};"
            f"\njp_dict={jp_dict}"
            f"\n{err}"
            ParameterExtractionError(msg, err)

    def execute_validation(self, excel, sheet, iid, name, desc, expected):
        try:
            self.run_validate(expected, self.response_json)
            result = "PASS"
        except Exception as e:
            result = "FAIL"
            error_info = f"| exception case:**{sheet}_{iid}_{name}_{desc},{self.assertions}"
            AssertionFailedError(error_info, e)
            raise e
        finally:
            print(f'| 断言结果-->{self.assertions}\n')
            response = self.response.text if self.response is not None else str(self.response)
            excel.write_back(sheet_name=sheet, i=iid, response=response, test_result=result,
                             assert_log=str(self.assertions))

    @staticmethod
    def base_info(item):
        """
        获取基础信息
        """
        sheet = item.pop("sheet")
        item_id = item.pop("Id")
        condition = item.pop("Run")
        sleep_time = item.pop("Time")
        name = item.pop("Name")
        desc = item.pop("Description")
        headers_crypto = item.pop("Headers Crypto")
        request_data_crypto = item.pop("Request Data Crypto")
        method = item.pop("Method")
        expected = item.pop("Expected")
        return sheet, item_id, condition, sleep_time, name, desc, headers_crypto, request_data_crypto, method, expected

    @staticmethod
    def sql_info(item):
        sql = item.pop("SQL")
        sql_params_dict = item.pop("Sql Params Dict")
        return sql, sql_params_dict

    @staticmethod
    def extractor_info(item):
        """
        获取提取参数的基本字段信息
        Args:
            item:

        Returns:

        """
        regex = item.pop("Regex")
        keys = item.pop("Regex Params List")
        deps = item.pop("Retrieve Value")
        jp_dict = item.pop("Jsonpath")
        extract_request_data = item.pop("Extract Request Data")
        return regex, keys, deps, jp_dict, extract_request_data

    @staticmethod
    def request_info(item):
        """
        请求数据
        """
        url = item.pop("Url")
        query_str = item.pop("Query Str")
        request_data = item.pop("Request Data")
        headers = item.pop("Headers")
        request_data_type = item.pop("Request Data Type") if item.get("Request Data Type") else 'params'

        return url, query_str, request_data, headers, request_data_type

    @staticmethod
    def script(item):
        setup_script = item.pop("Setup Script")
        teardown_script = item.pop("Teardown Script")
        return setup_script, teardown_script

    @staticmethod
    def is_run(condition):
        is_run = condition
        if not is_run or is_run.upper() != "YES":
            return True

    @staticmethod
    def pause_execution(sleep_time):
        if sleep_time:
            try:
                time.sleep(sleep_time)
            except Exception as e:
                raise InvalidSleepTimeError(f"{sleep_time}", e)

    def exc_sql(self, item):
        sql, sql_params_dict = self.sql_info(item)
        sql = self.replace_dependent_parameter(sql)
        if sql:
            client = MysqlClient(self.db_config)
            execute_sql_results = client.execute_sql(sql)
            print(f"| 执行 sql 成功--> {execute_sql_results}")
            if execute_sql_results and sql_params_dict:
                self.substitute_data(execute_sql_results, jp_dict=sql_params_dict)


if __name__ == '__main__':
    print(Action())
