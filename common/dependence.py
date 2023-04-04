# -*- coding:utf-8 -*-
import re
import sys

sys.path.append("./")
sys.path.append("./common")


class Dependence:
    dependence = {}  # 定义依赖表
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
    from common.files_tools.get_excel_init import get_init

    excel_handle, init_data, test_case = get_init()
    initialize_data = eval(init_data.get("initialize_data"))
    print(initialize_data)
    Dependence.set_dep(initialize_data)  # 初始化依赖表
    print("--------------------->", Dependence.get_dep())
