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

from common.crypto.encrypt_data import EncryptData
from common.database.mysql_client import MysqlClient
from common.log_utils.mylogger import MyLogger
from common.utils.decorators import singleton
from common.validation.extractor import Extractor
from common.validation.load_and_execute_script import LoadScript
from common.validation.validator import Validator


@singleton
class Action(Extractor, LoadScript, Validator, MysqlClient):
    def __init__(self, initialize_data=None, bif_functions=None, db_config=None):
        super().__init__()
        MysqlClient.__init__(self, db_config)
        self.encrypt = EncryptData()
        self.__variables = {}
        self.set_environments(initialize_data)
        self.set_bif_fun(bif_functions)
        self.logger = MyLogger()
    
    def execute_dynamic_code(self, item, code):
        self.variables = item
        if code is not None:
            try:
                ast_obj = ast.parse(code, mode='exec')
                compiled = compile(ast_obj, '<string>', 'exec')
                exec(compiled, {"pm": self})
            except SyntaxError as e:
                error_message = f'动态代码语法异常: {e}'
                self._handle_error(error_message)
            except Exception as e:
                error_message = f"动态代码执行异常: {e}"
                self._handle_error(error_message)
        return self.variables
    
    def _handle_error(self, error_message):
        print(f'发现异常: {error_message}')
    
    @property
    def variables(self, key=None):
        return self.__variables if not key else self.__variables.get(key)
    
    @variables.setter
    def variables(self, item):
        self.__variables = item
    
    # def update_variables(self, key, value):
    #     self.__variables[f"{{{{{key}}}}}"] = value
    
    def analysis_request(self, request_data, headers_crypto, headers, request_crypto, extract_request_data):
        # 请求头及body加密或者加签
        headers, request_data = self.encrypt.encrypts(headers_crypto, headers, request_crypto, request_data)
        # 提取请求参数信息
        if extract_request_data is not None and request_data is not None:
            self.substitute_data(request_data, jp_dict=extract_request_data)
        return headers, request_data
    
    def send_request(self, host, url, method, teardown_script, **kwargs):
        response = self.http_client(host, url, method, **kwargs)
        self.update_environments("responseTime", response.elapsed.total_seconds() * 1000)  # 存响应时间
        self.execute_dynamic_code(response, teardown_script)
        return response
    
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
    
    def pause_execution(self, sleep_time):
        if sleep_time:
            try:
                time.sleep(sleep_time)
            except Exception as e:
                self.logger.error("暂时时间必须是数字")
                raise e
    
    def exc_sql(self, item):
        sql, sql_params_dict = self.sql_info(item)
        sql = self.replace_dependent_parameter(sql)
        if sql:
            try:
                execute_sql_results = self.execute_sql(sql)
                if execute_sql_results and sql_params_dict:
                    self.substitute_data(execute_sql_results, jp_dict=sql_params_dict)
            except Exception as e:
                self.logger.error(f'执行 sql 失败:{sql},异常信息:{e}')
                raise e


if __name__ == '__main__':
    print(Action.__mro__)
