#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: base_class.py
@time: 2023/4/14 16:30
@desc:
"""
import unittest

from common import bif_functions
from common.data_extraction.dependent_parameter import DependentParameter as DP
from common.data_extraction.data_extractor import DataExtractor
from common.crypto.encryption_main import do_encrypt
from common.database.do_mysql import DoMysql
from common.utils.http_client import http_client
from common.utils.logger import MyLog
from common.validation import loaders
from common.validation.validator import Validator

dep_par = DP()  # 参数提取类实例化
logger = MyLog()  # 日志


class BaseClass(unittest.TestCase):
    maxDiff = None

    def __init__(self, *args, **kwargs):
        self.host = kwargs.pop("host", "") + kwargs.pop("path", "")
        self.databases = kwargs.pop("databases")
        self.mysql = DoMysql(self.databases)
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        logger.my_log("开始加载内置方法...", "info")
        loaders.set_bif_fun(bif_functions)  # 加载内置方法
        logger.my_log("内置方法加载完成", "info")
        logger.my_log(f"所有用例执行开始...", "info")
        super().setUpClass()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()
        logger.my_log(f"所有用例执行完毕")

    def do_process(self, item):
        """执行流程"""
        self._case = item  # 绑定测试数据
        self.init_data()  # 初始化数据
        self.do_data_processing()  # 替换参数
        self.do_request()  # 发送请求
        self.check()  # 断言数据
        self.do_response()  # 提取响应

    def do_data_processing(self):
        """参数替换"""
        if self.mysql:
            self.do_sql()  # 处理 sql
        self.do_url()  # 处理 url
        self.do_headers()  # 处理 请求头
        self.do_args()  # 处理 请求参数
        self.get_args()  # 提取请求参数
        self.do_encryption()  # 处理 加密
        self.do_expected()  # 处理 预期结果

    def init_data(self):
        self.sheet = self._case.get("sheet")
        self.item_id = self._case.get("Id")
        self.name = self._case.get("name")
        self.description = self._case.get("description")
        self.url = self._case.get("Url")
        self.method = self._case.get("Method")
        self.request_data_type = self._case.get("request_data_type", "json")
        self.sql_variable = self._case.get("sql变量")
        self.sqlps = self._case.get("SQL")
        self.headers = self._case.get("Headers", {})
        self.parameters = self._case.get("Request Data")
        self.parameters_key = self._case.get("提取请求参数")
        self.encryption = self._case.get("请求参数是否加密")
        self.regex = self._case.get("正则表达式")
        self.keys = self._case.get("正则变量")
        self.deps = self._case.get("绝对路径表达式")
        self.jp_dict = self._case.get("Jsonpath")
        self.expect = self._case.get("预期结果")

    def do_url(self):
        """处理url"""
        self.url = dep_par.replace_dependent_parameter(self.url)

    def do_args(self):
        """处理请求参数"""
        self.parameters = dep_par.replace_dependent_parameter(self.parameters)

    def get_args(self):
        """提取请求参数"""
        DataExtractor(self.parameters).substitute_data(jp_dict=self.parameters_key)

    def do_encryption(self):
        self.parameters = do_encrypt(self.encryption, self.parameters)  # 数据加密：MD5 ｏｒ　ｓｈａ１

    def do_headers(self):
        """处理请求头，默认请求头与填写的请求头合并"""
        self.headers = dep_par.replace_dependent_parameter(self.headers)

    def do_expected(self):
        """替换期望结果"""
        self.expect = dep_par.replace_dependent_parameter(self.expect)

    def do_request(self):
        """发送http请求"""
        try:
            kwargs = {
                "headers": self.headers,
                self.request_data_type: self.parameters
            }
            self._response = http_client(self.host, self.url, self.method, **kwargs)
            logger.my_log(f"请求 URL --> {self._response.request.url}", "info")
            logger.my_log(f"请求 HEADERS --> {self._response.request.headers}", "info")
            logger.my_log(f"请求 BODY --> {self._response.request.body}", "info")
            logger.my_log(f"接口耗时--> 【{self._response.elapsed}】", "info")
            logger.my_log(f"接口状态--> 【{self._response.status_code}】", "info")
            logger.my_log(f"接口响应--> {self._response.text}", "info")
        except Exception as e:
            result = "失败"
            logger.my_log(f'用例id:{self.item_id}-->{self.name}_{self.description},{self._response},异常:{e}')
            raise e

    def do_response(self):
        """提取响应"""
        try:
            # 提取响应
            DataExtractor(self._response.json()).substitute_data(regex=self.regex, keys=self.keys, deps=self.deps,
                                                                 jp_dict=self.jp_dict)
        except Exception as e:
            logger.my_log(
                f"提取响应失败：{self.name}_{self.description}:提取数据表达式："
                f"\n-->regex={self.regex},"
                f"\n-->keys={self.keys},"
                f"\n-->deps={self.deps},"
                f"\n-->jp_dict={self.jp_dict}"
                f"\n-->Exception={e}")

    def check(self):
        """断言"""
        self.result_tuples = Validator().run_validate(self.expect, self._response.json())  # 执行断言 返回结果元组
        logger.my_log(f"断言结果组：{self.result_tuples}", "info")

    def do_sql(self):
        # 首先执行sql替换,将sql替换为正确的sql语句
        self.sql = dep_par.replace_dependent_parameter(self.sqlps)

    def get_sql_res(self):
        """执行sql"""
        try:
            execute_sql_results = self.mysql.do_mysql(self.sql)
            if execute_sql_results and self.sql_variable:
                # 执行sql数据提取
                DataExtractor(execute_sql_results).substitute_data(jp_dict=self.sql_variable)
                if self.method == "SQL" and self.mysql:
                    return
        except Exception as e:
            logger.my_log(f'执行 sql 失败:{self.sql},异常:{e}')
            raise e

    def do_mongoDB(self):
        """"""
        pass
