# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         loader.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2019/11/18 17:32
# -------------------------------------------------------------------------------
import types

from common.dependence import Dependence
from common.validation import comparators


def load_built_in_functions(model):
    """
    加载bif_functions包中的内建方法
    Returns:
    """
    built_in_functions = {}
    for name, item in vars(model).items():
        if isinstance(item, types.FunctionType):
            built_in_functions[name] = item
    return built_in_functions


def load_built_in_comparators() -> object:
    """
    加载包中的内建比较器
    Returns:

    """
    built_in_comparators = {}
    for name, item in vars(comparators).items():
        if isinstance(item, types.FunctionType):
            built_in_comparators[name] = item

    return built_in_comparators


# def load_model_fun(model):
#     """
#     加载指定模块中的所有函数
#     Returns:
#
#     """
#     for name, item in vars(model).items():
#         if isinstance(item, types.FunctionType):
#             Dependence.update_dep(f"{name}()", item)


def set_bif_fun(model):
    """
    将所有内置方法加载到依赖表中
    Returns:

    """
    for k, v in load_built_in_functions(model).items():
        Dependence.update_dep(f"{k}()", v)


if __name__ == '__main__':
    from common.bif_functions import random_tools
    print(load_built_in_comparators())
    set_bif_fun(random_tools)
    print(Dependence.get_dep())
