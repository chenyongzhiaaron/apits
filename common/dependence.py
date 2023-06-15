# -*- coding:utf-8 -*-
import re
import sys
from dataclasses import dataclass

sys.path.append("./")
sys.path.append("./common")
from common import logger


# from common.utils.mylogger import MyLogger

# logger = MyLogger()


@dataclass
class Dependence:
    dependence = {}  # 定义依赖表
    pattern_l = re.compile(r"{{\s*([^}\s]+)\s*}}(?:\[(\d+)\])?")
    PATTERN = re.compile(r"{{(.*?)}}")  # 预编译正则表达式
    pattern = re.compile(r'({)')
    pattern_fun = re.compile(r"{{(\w+\(\))}}")

    @classmethod
    def update_dep(cls, key, value):
        """更新依赖表"""
        cls.dependence[f"{{{{{key}}}}}"] = value

    @classmethod
    def get_dep(cls, key=None):
        """获取依赖表 或 依赖表中key对应的值"""
        return cls.dependence if not key else cls.dependence.get(key)

    @classmethod
    def set_dep(cls, value):
        """设置依赖表"""
        cls.dependence = value


if __name__ == '__main__':
    from common.file_handling.get_excel_init import get_init
    from common.config import Config

    test_file = Config.test_api
    excel_handle, init_data, test_case = get_init(test_file)
    initialize_data = eval(init_data.get("initialize_data"))
    print(initialize_data)
    d = Dependence
    d.set_dep(initialize_data)  # 初始化依赖表
    print("--------------------->", d.get_dep())
