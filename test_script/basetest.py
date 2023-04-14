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


class BaseTest(unittest.TestCase):
    maxDiff = None
    test_excel = None
    logger = MyLog()  # 日志
    dep_par = DependentParameter()  # 参数提取类实例化
    dep = Dependence
    # @classmethod
    # def setUpClass(cls) -> None:
    #     loaders.set_bif_fun(bif_functions)  # 加载内置方法

    # def do_init(self):
    #     """初始化excel数据、初始化mysql链接、初始化依赖表"""
        # self.excel_handle, self.init_data, self._case = get_init(self.test_excel)
        # self.database = self.init_data.pop("database")
        # self.mysql = DoMysql(self.database)
        # self.dep = Dependence
        # self.dep.set_dep(eval(self.init_data.pop("initialize_data")))  # 初始化依赖表

    def do_process(self, item):
        """执行流程"""
        self._case = item  # 绑定测试数据

    def check(self):
        """断言"""
        pass

    def do_request(self):
        """发送http请求"""
        # self._response = req(host + path, url, method, headers=headers, data=parameters)

    def do_replace(self):
        """"""
        pass

    def do_mysql(self):
        """"""
        pass

    def do_get(self):
        """"""
        pass

    def do_mongoDB(self):
        """"""
        pass

    def do_excel(self):
        """"""
        pass

    def do_url(self):
        """"""
        pass

    def do_args(self):
        """"""
        pass

    def do_headers(self):
        pass

    def do_expected(self):
        """替换期望结果"""
        pass

    def get_request_args(self):
        """提取请求参数"""
        pass
