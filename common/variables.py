# -*- coding:utf-8 -*-
import re
from dataclasses import dataclass


@dataclass
class Variables:
    variables = {}  # 定义依赖表
    pattern_l = re.compile(r"{{\s*([^}\s]+)\s*}}(?:\[(\d+)\])?")
    PATTERN = re.compile(r"{{(.*?)}}")  # 预编译正则表达式
    pattern = re.compile(r'({)')
    pattern_fun = re.compile(r"{{(\w+\(\))}}")

    @classmethod
    def update_variable(cls, key, value):
        """更新依赖表"""
        cls.variables[f"{{{{{key}}}}}"] = value

    @classmethod
    def get_variable(cls, key=None):
        """获取依赖表 或 依赖表中key对应的值"""
        return cls.variables if not key else cls.variables.get(key)

    @classmethod
    def set_variable(cls, value):
        """设置依赖表"""
        cls.variables = value

    @classmethod
    def reset(cls):
        """重置"""
        cls.variables.clear()
        cls.request = None
        cls.response = None


if __name__ == '__main__':
    from common.file_handling.get_excel_init import get_init
    from common.config import Config

    test_file = Config.test_api
    excel_handle, init_data, test_case = get_init(test_file)
    initialize_data = eval(init_data.get("initialize_data"))
    print(initialize_data)
    d = Variables
    d.set_variable(initialize_data)  # 初始化依赖表
    print("--------------------->", d.get_variable())
