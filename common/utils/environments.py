#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: environments.py
@time: 2023/6/21 17:44
@desc:
"""

import re
from dataclasses import dataclass

from config.field_constants import FieldNames


class Environments(FieldNames):
    environments = {}
    PARAMETER_MATCHER = re.compile(r"{{\s*([^}\s]+)\s*}}(?:\[(\d+)\])?")  # 匹配需要替换的参数
    PARAMETER_PATTERN = re.compile(r"{{(.*?)}}")  # 匹配参数模式 {{...}}
    BRACE_MATCHER = re.compile(r'({)')  # 匹配 '{' 符号
    FUNCTION_CHAIN_MATCHER = re.compile(r"\{\{((?:\w+\([^}]*\))(?:\.\w+\([^}]*\))*)\}\}")  # 匹配函数调用链的参数模式 {{func()...}}
    FUNCTION_CALL_MATCHER = re.compile(r"\w+\([^)]*\)")  # 匹配函数调用中的方法名和参数 {{func()}} 中的 func
    METHOD_NAME_MATCHER = re.compile(r"\.(\w+)\([^)]*\)")  # 匹配函数调用中的方法名 {{.func()}} 中的 func
    ARGS_MATCHER = re.compile(r'\(([^)]*)\)')  # 匹配函数调用中的参数列表 {{func(arg1, arg2, ...)}}

    def __init__(self):
        super().__init__()

    @classmethod
    def update_environments(cls, key, value):
        """更新依赖表"""
        cls.environments[f"{{{{{key}}}}}"] = value

    @classmethod
    def get_environments(cls, key=None):
        """获取依赖表 或 依赖表中key对应的值"""
        return cls.environments if not key else cls.environments.get(key)

    @classmethod
    def set_environments(cls, value):
        """设置依赖表"""
        cls.environments = value

    @classmethod
    def reset_environments(cls):
        """重置"""
        cls.environments.clear()


if __name__ == '__main__':
    from common.file_handling.do_excel import DoExcel
    from config.config import Config

    test_file = Config.TEST_CASE
    do_excel = DoExcel(test_file)
    init_case = do_excel.get_excel_init()
    d = Environments
    d.set_environments(init_case)
    print("--------------------->", d.get_environments())
