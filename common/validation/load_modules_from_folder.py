#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: load_fun_from_modul.py
@time: 2023/3/17 16:15
@desc:
"""
import importlib.util
import os

from common.dependence import Dependence


def load_modules_from_folder(folder_path):
    """
    动态加载指定文件夹下的模块，并读取其中的函数，存储在字典这样的数据结构中。
    通过访问字典的 key 可以获取到对应的函数值并调用。

    Args:
        folder_path (str): 要加载模块的文件夹路径

    Returns:
        dict: 存储函数的字典，键为函数名，值为函数对象
    """

    if not os.path.exists(folder_path):  # 检查文件夹路径是否存在
        raise ValueError("Folder path does not exist.")

    for file_name in os.listdir(folder_path):  # 遍历指定文件夹下的所有文件
        module_name, ext = os.path.splitext(file_name)
        if ext == '.py':  # 如果是 Python 模块文件
            module_path = os.path.join(folder_path, file_name)  # 获取模块文件的完整路径
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)  # 加载模块文件并执行其中的代码，将函数定义添加到 module 对象中
            except Exception as e:
                print(f"Error loading module {module_name}: {str(e)}")
                continue

            # 遍历 module 对象中的所有属性，找出函数并添加到 functions 字典中
            for name, obj in vars(module).items():
                if callable(obj):
                    Dependence.update_dep(name, obj)


if __name__ == '__main__':
    load_modules_from_folder(r'D:\apk_api\api-test-project\extensions')
    print(Dependence.get_dep())
