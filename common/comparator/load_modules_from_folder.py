#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: load_fun_from_modul.py
@time: 2023/3/17 16:15
@desc:
"""
# 以下是用Python实现的动态加载指定文件夹下模块并读取函数的示例代码，每行代码都加了注释说明：

import os
import importlib.util


def load_modules_from_folder(folder_path):
    functions = {}  # 创建一个空字典，用于存储读取到的函数

    # 遍历指定文件夹下的所有文件
    for file_name in os.listdir(folder_path):
        module_name, ext = os.path.splitext(file_name)  # 分离文件名和扩展名
        if ext == '.py':  # 如果是 Python 模块文件
            module_path = os.path.join(folder_path, file_name)  # 获取模块文件的完整路径
            spec = importlib.util.spec_from_file_location(module_name, module_path)  # 根据模块文件路径创建一个模块规范
            module = importlib.util.module_from_spec(spec)  # 根据模块规范创建一个空的模块对象
            spec.loader.exec_module(module)  # 加载模块文件并执行其中的代码，将函数定义添加到 module 对象中
            # 遍历 module 对象中的所有属性，找出函数并添加到 functions 字典中
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if callable(attr):
                    functions[attr_name] = attr

    return functions  # 返回存储函数的字典

# 上述代码主要实现了以下功能：
#
# 1. 导入了必要的模块，包括 `os` 和 `importlib.util`。
#    - `os` 模块提供了操作文件系统的功能，如列出文件夹下的所有文件。
#    - `importlib.util` 模块提供了加载指定路径的模块文件的功能。
# 2. 定义了一个名为 `load_functions` 的函数，该函数接受一个参数 `folder_path`，表示要加载模块的文件夹路径。
# 3. 在函数内部创建了一个空字典 `functions`，用于存储读取到的函数。
# 4. 使用 `os.listdir()` 函数遍历指定文件夹下的所有文件，并使用 `os.path.splitext()` 函数分离出每个文件名和扩展名。
# 5. 判断文件扩展名是否为 `.py`，如果是则说明是 Python 模块文件。
# 6. 构造模块文件的完整路径，并使用 `importlib.util.spec_from_file_location()` 函数创建一个模块规范对象 `spec`。
# 7. 使用 `importlib.util.module_from_spec()` 函数根据模块规范对象创建一个空的模块对象 `module`。
# 8. 使用 `spec.loader.exec_module()` 函数加载模块文件并执行其中的代码，这会将函数定义添加到 `module` 对象中。
# 9. 遍历 `module` 对象中的所有属性，找出其中的函数并添加到 `functions` 字典中。
# 10. 最后返回存储函数的字典 `functions`。
#
# 这个函数可以方便地动态加载指定文件夹下的模块，并读取其中的函数，存储在字典这样的数据结构中。通过访问字典的 key 可以获取到对应的函数值并调用。



import os
import importlib
import inspect


def load_modules(module_dir):
    """
    动态加载指定文件夹下的模块，并读取模块内的函数，存储在字典这样的数据结构中。

    Parameters:
        module_dir (str): 模块所在的目录路径。

    Returns:
        dict: 包含已加载模块的函数的字典。字典的key为函数名，value为对应的函数对象。
    """

    functions = {}

    # 循环遍历目录下所有Python文件
    for filename in os.listdir(module_dir):
        filepath = os.path.join(module_dir, filename)
        if not os.path.isfile(filepath) or not filename.endswith('.py'):
            continue

        # 获取Python文件名（去除扩展名）
        module_name = filename[:-3]

        try:
            # 动态加载模块
            module = importlib.import_module(module_name)

            # 遍历模块内所有对象
            for name, obj in inspect.getmembers(module):
                # 如果对象为函数，则将其添加到字典中
                if inspect.isfunction(obj):
                    functions[name] = obj

        except Exception as e:
            print(f"Failed to load module '{module_name}': {str(e)}")

    return functions



# 解释每个关键点：
# - `os.listdir(module_dir)`
# 用于获取指定目录下的所有文件名。
# - `os.path.isfile(filepath)`
# 用于判断指定路径是否为文件。
# - `not filename.endswith('.py')`
# 用于判断文件名是否以
# `.py
# `结尾。
# - `importlib.import_module(module_name)`
# 用于动态加载指定模块。
# - `inspect.getmembers(module)`
# 用于获取指定模块内的所有对象，返回一个元组列表。
# - `inspect.isfunction(obj)`
# 用于判断指定对象是否为函数。
# - 将函数以键值对
# `(name, obj)`
# 的形式添加到字典中。