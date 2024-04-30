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
from common.utils.decorators import singleton, send_request_decorator
from common.utils.exceptions import *
from common.validation.load_and_execute_script import LoadScript


@singleton
class Action(LoadScript):
    def __init__(self, host='', initialize_data=None):
        super().__init__()
        self.__variables = {}
        if not initialize_data:
            initialize_data = {}
        self.set_environments(initialize_data)
        self.set_bif_fun(bif_functions)
        self.host = host

    def base_info(self, item):
        """
        获取基础信息
        """
        # self.variable = deepcopy(item)
        self.sheet = item.pop(self.SHEET)
        self.item_id = item.pop(self.ITEM_ID)
        self.condition = item.pop(self.RUN_CONDITION)
        self.sleep_time = item.pop(self.SLEEP_TIME)
        self.name = item.pop(self.NAME)
        self.desc = item.pop(self.DESCRIPTION)
        self.method = item.pop(self.METHOD)
        self.prepost_script = f"prepost_script_{self.sheet}_{self.item_id}.py"
        self.sql = self.replace_dependent_parameter(item.pop(self.SQL))
        self.exc_sql = item.pop(self.SQL_PARAMS_DICT)
        self.regex = item.pop(self.REGEX)
        self.keys = item.pop(self.REGEX_PARAMS_LIST)
        self.deps = item.pop(self.RETRIEVE_VALUE)
        self.jp_dict = item.pop(self.JSON_PATH_DICT)
        self.extract_request_data = item.pop(self.EXTRACT_REQUEST_DATA)
        self.url = self.replace_dependent_parameter(item.pop(self.URL))
        self.query_str = self.replace_dependent_parameter(item.pop(self.QUERY_STRING))
        self.body = self.replace_dependent_parameter(item.pop(self.REQUEST_DATA))
        self.headers = self.replace_dependent_parameter(item.pop(self.HEADERS))
        self.headers_crypto = item.pop(self.HEADERS_CRYPTO)  # 请求头加密方式
        self.body_typ = item.pop(self.REQUEST_DATA_TYPE) if item.get(self.REQUEST_DATA_TYPE) else self.PARAMS
        self.body_crypto = item.pop(self.REQUEST_DATA_CRYPTO)  # 请求数据加密方式
        self.setup_script = item.pop(self.SETUP_SCRIPT)
        self.teardown_script = item.pop(self.TEARDOWN_SCRIPT)
        self.expected = item.pop(self.EXPECTED)

    @send_request_decorator
    def send_request(self):
        """发送请求"""
        if not self.body_typ:
            raise "当前测试用例没有填写请求参数类型！"
        self.http_client()

    def analysis_request(self):
        """分析请求数据"""
        # 开始请求头、请求body加密
        headers, body = self.encrypts(self.headers_crypto, self.headers, self.body_crypto, self.body)
        if self.extract_request_data:
            for data in (self.query_str, body):
                if data:
                    self.substitute_data(data, jp_dict=self.extract_request_data)
        kwargs = {self.body_typ: body, "headers": headers, "params": self.query_str}
        self.processing_data(self.host, self.url, self.method, **kwargs)

    def analysis_response(self):
        """分析响应结果并提取响应"""
        try:
            self.substitute_data(self.response_json, regex=self.regex, keys=self.keys, deps=self.deps,
                                 jp_dict=self.jp_dict)
        except Exception as err:
            msg = f"| 分析响应失败：{self.sheet}_{self.iid}_{self.name}_{self.desc}"
            f"\nregex={self.regex};"
            f" \nkeys={self.keys};"
            f"\ndeps={self.deps};"
            f"\njp_dict={self.jp_dict}"
            f"\n{err}"
            ParameterExtractionError(msg, err)

    def execute_validation(self, excel=None):
        """执行断言校验"""
        expected = self.replace_dependent_parameter(self.expected)
        result = None
        try:
            self.run_validate(expected, self.response_json)
            # 如果不填写断言，则自动断言状态码
            if not self.expected:
                from common.validation.comparators import eq
                eq(200, self.response.status_code)
            result = "PASS"
        except Exception as e:
            result = "FAIL"
            error_info = f"| exception case:**{self.sheet}_{self.item_id}_{self.name}_{self.desc},{self.assertions}"
            AssertionFailedError(error_info, e)
            raise e
        finally:
            print(f'| <span style="color:yellow">断言结果-->{self.assertions}</span>\n')
            print("-" * 50 + "我是分割线" + "-" * 50)
            response = self.response.text if self.response is not None else str(self.response)
            if not excel:
                excel.write_back(sheet_name=self.sheet, i=self.item_id, response=response, result=result,
                                 assertions=str(self.assertions))

    def execute_dynamic_code(self, code):

        if code is not None:
            try:
                ast_obj = ast.parse(code, mode='exec')
                compiled = compile(ast_obj, '<string>', 'exec')
                exec(compiled, {"py": self})
            except Exception as e:
                ExecuteDynamiCodeError(code, e)
                raise e

    def execute_prepost_script(self, scripts_dir, prepost_script, method_name):
        self.load_and_execute_script(scripts_dir, prepost_script, self, method_name)

    def is_run(self):
        if not self.condition or self.condition.upper() != 'NO':
            return True
        return None

    def exec_sql(self, client):
        """执行sql处理"""
        if self.sql:
            execute_sql_results = client.execute_sql(self.sql)
            print(f"| 执行 sql 成功--> {execute_sql_results}")
            if execute_sql_results and self.exc_sql:
                self.substitute_data(execute_sql_results, jp_dict=self.exc_sql)

    def is_only_sql(self, client):
        if self.method.upper() == self.SQL:
            self.exec_sql(client)
            return True
        return None

    def pause_execution(self):
        if self.sleep_time:
            try:
                time.sleep(self.sleep_time)
            except Exception as e:
                raise InvalidSleepTimeError(f"{self.sleep_time}", e)
