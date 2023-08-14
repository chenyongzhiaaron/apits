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
from common.utils.decorators import singleton, send_request_decorator
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

    @send_request_decorator
    def send_request(self, host, method, extract_request_data):

        url, kwargs = self.prepare_request(extract_request_data, self.variables)
        self.http_client(host, url, method, **kwargs)

    def prepare_request(self, extract_request_data, item):
        item = self.replace_dependent_parameter(item)
        url, query_str, request_data, headers, request_data_type, h_crypto, r_crypto = self.request_info(item)
        headers, request_data = self.analysis_request(request_data, h_crypto, headers, r_crypto, extract_request_data)
        kwargs = {request_data_type: request_data, "headers": headers, "params": query_str}
        return url, kwargs

    def analysis_request(self, request_data, headers_crypto, headers, request_crypto, extract_request_data):
        headers, request_data = self.encrypt.encrypts(headers_crypto, headers, request_crypto, request_data)
        if extract_request_data is not None and request_data is not None:
            self.substitute_data(request_data, jp_dict=extract_request_data)
        return headers, request_data

    @staticmethod
    def base_info(item):
        """
        获取基础信息
        """
        sheet = item.pop("Sheet")
        item_id = item.pop("Id")
        condition = item.pop("Run")
        sleep_time = item.pop("Time")
        name = item.pop("Name")
        desc = item.pop("Description")
        method = item.pop("Method")
        expected = item.pop("Expected")
        return sheet, item_id, condition, sleep_time, name, desc, method, expected

    @staticmethod
    def sql_info(item):
        sql = item.pop("SQL")
        sql_params_dict = item.pop("SqlParamsDict")
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
        keys = item.pop("RegexParamsList")
        deps = item.pop("RetrieveValue")
        jp_dict = item.pop("Jsonpath")
        extract_request_data = item.pop("ExtractRequestData")
        return regex, keys, deps, jp_dict, extract_request_data

    @staticmethod
    def request_info(item):
        """
        请求数据
        """
        url = item.pop("Url")
        query_str = item.pop("QueryString")
        request_data = item.pop("RequestData")
        headers = item.pop("Headers")
        request_data_type = item.pop("RequestDataType") if item.get("RequestDataType") else 'params'
        headers_crypto = item.pop("HeadersCrypto")
        request_data_crypto = item.pop("RequestDataCrypto")

        return url, query_str, request_data, headers, request_data_type, headers_crypto, request_data_crypto

    @staticmethod
    def script(item):
        setup_script = item.pop("SetupScript")
        teardown_script = item.pop("TeardownScript")
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
        self.variables = item
        sql = self.replace_dependent_parameter(sql)
        if sql:
            client = MysqlClient(self.db_config)
            execute_sql_results = client.execute_sql(sql)
            print(f"| 执行 sql 成功--> {execute_sql_results}")
            if execute_sql_results and sql_params_dict:
                self.substitute_data(execute_sql_results, jp_dict=sql_params_dict)

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
        expected = self.replace_dependent_parameter(expected)
        try:
            self.run_validate(expected, self.response_json)
            result = "PASS"
        except Exception as e:
            result = "FAIL"
            error_info = f"| exception case:**{sheet}_{iid}_{name}_{desc},{self.assertions}"
            AssertionFailedError(error_info, e)
            raise e
        finally:
            print(f'| <span style="color:yellow">断言结果-->{self.assertions}</span>\n')
            print("-" * 50 + "我是分割线" + "-" * 50)
            response = self.response.text if self.response is not None else str(self.response)
            excel.write_back(sheet_name=sheet, i=iid, response=response, result=result, assertions=str(self.assertions))

    @property
    def variables(self, key=None):
        return self.__variables if not key else self.__variables.get(key)

    @variables.setter
    def variables(self, item):
        self.__variables = item


if __name__ == '__main__':
    print(Action())
