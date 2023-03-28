# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         loader.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2019/11/18 17:32
# -------------------------------------------------------------------------------
import types

from common import functions
from common.comparator import comparators


def load_built_in_functions():
    """
    加载builtin包中的内建方法
    Returns:
    """
    built_in_functions = {}

    for name, item in vars(functions).items():
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


def load_model_fun(model):
    """
    加载指定模块中的所有函数
    Returns:

    """
    model_fun = {}
    for name, item in vars(model).items():
        # print("-----", name, item)
        if isinstance(item, types.FunctionType):
            model_fun[name] = item

    return model_fun


# def load_ext_method_online():
#     """
#     动态加载ext_method_online.py模块中内容
#     Returns:
#         ext_method_online_module:ext_method_online模块
#         ext_methods_online:ext_method_online模块中的方法
#     """
#     ext_method_online_module = None
#     ext_methods_online = {}
#     ext_method_online = ExtMethodOnline.objects.filter(name='ext_method_online.py').first()
#     if ext_method_online:
#         filename = ext_method_online.name
#         filepath = ext_method_online.filepath.replace('/', os.sep)
#         path = os.path.join(settings.BASE_DIR, filepath, filename)
#         if os.path.exists(path) and os.path.isfile(path):
#             ext_method_online_module_name = 'apps.HttpAutoTestService.core.ext_methods.ext_method_online'
#             ext_method_online_module = importlib.import_module(ext_method_online_module_name)
#             importlib.reload(ext_method_online_module)
#             for name, item in vars(ext_method_online_module).items():
#                 if isinstance(item, types.FunctionType):
#                     ext_methods_online[name] = item
#     return ext_method_online_module, ext_methods_online


if __name__ == '__main__':
    from common.functions import random_tools

    # func = load_model_fun(random_tools)
    # print(func)
    # print(load_built_in_functions())
    print(load_built_in_comparators())
