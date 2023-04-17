#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: base_class.py
@time: 2023/4/14 16:30
@desc:
"""
import sys
import time
import warnings
import unittest

from common import bif_functions
from common.extractor.dependent_parameter import DependentParameter
from common.extractor.data_extractor import DataExtractor
from common.encryption.encryption_main import do_encrypt
from common.do_sql.do_mysql import DoMysql
from common.tools.req import req
from common.tools.logger import MyLog
from common.comparator import loaders
from common.comparator.validator import Validator
from common.dependence import Dependence
from common.files_tools.get_excel_init import get_init

dep_par = DependentParameter()  # 参数提取类实例化
logger = MyLog()  # 日志


class BaseTest(unittest.TestCase):
    maxDiff = None
    test_excel = None


    @classmethod
    def setUpClass(cls) -> None:
        loaders.set_bif_fun(bif_functions)  # 加载内置方法
        cls.host = ""
        cls.path = ""
        cls.header = {}  # 默认请求头

    def do_init(self):
        pass

    def do_process(self, item):
        """执行流程"""
        self._case = item  # 绑定测试数据
        if self._case.get("Run").upper() != "YES":
            return
        # 前置处理
        self.do_data_processing()  # 替换参数
        # 执行加密
        # 发送请求
        self.do_request()

        # 后置处理
        # 断言数据
        # 结果回写
        # 提取响应

    def do_data_processing(self):
        """参数替换"""
        self.do_url()
        self.do_args()
        self.do_encryption()
        self.do_headers()
        self.do_expected()

    def init_data(self):
        self.sheet = self._case.get("sheet")
        self.item_id = self._case.get("Id")
        self.name = self._case.get("name")
        self.description = self._case.get("description")
        self.host = self.host
        self.path = self.path
        self.url = self._case.get("Url")
        self.headers = self.headers
        self.run = self._case.get("Run")
        self.method = self._case.get("Method")
        self.sql_variable = self._case.get("sql变量")
        self.sqlps = self._case.get("SQL")
        self.item_headers = self._case.get("Headers") if self._case.get("Headers") else {}
        self.parameters = self._case.get("请求参数")
        self.parameters_key = self._case.get("提取请求参数")
        self.encryption = self._case.get("参数加密方式")
        self.regex = self._case.get("正则表达式")
        self.keys = self._case.get("正则变量")
        self.deps = self._case.get("绝对路径表达式")
        self.jp_dict = self._case.get("Jsonpath")
        self.sql_key = self._case.get("sql变量")
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
        item_headers = dep_par.replace_dependent_parameter(self.item_headers if self.item_headers else {})
        self.headers = {**self.header, **item_headers}

    def do_expected(self):
        """替换期望结果"""
        self.expected = dep_par.replace_dependent_parameter(self.expect)

    def do_request(self):
        """发送http请求"""
        self._response = req(f'{self._case.get("host")}{self._case.get("path")}',
                             self._case.get("url"),
                             self._case.get("method"),
                             headers=self.headers, data=self.parameters)

    def do_response(self):
        """提取响应"""
        DataExtractor(self._response.json()).substitute_data(regex=self.regex, keys=self.keys, deps=self.deps,
                                                             jp_dict=self.jp_dict)

    def check(self):
        """断言"""
        result_tuple = Validator().run_validate(self.expected, self._response.json())  # 执行断言 返回结果元组

    def do_mysql(self):
        """"""
        mysql = DoMysql(databases)
        mysql.do_mysql(sql)

    def do_mongoDB(self):
        """"""
        pass

    def do_excel(self):
        """"""
        pass
