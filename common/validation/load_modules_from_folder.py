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
import types

from common.data_extraction.dependent_parameter import DependentParameter
from common.validation import logger


class LoadModulesFromFolder(DependentParameter):
    def __init__(self):
        super().__init__()

    @logger.log_decorator()
    def load_modules_from_folder(self, folder_or_mnodule):
        """
        动态加载文件或模块
        """

        if isinstance(folder_or_mnodule, str):
            folder_path = folder_or_mnodule
            if not os.path.exists(folder_path):  # 检查文件夹路径是否存在
                raise ValueError("Folder path does not exist.")

            for file_name in os.listdir(folder_path):  # 遍历指定文件夹下的所有文件
                module_name, ext = os.path.splitext(file_name)
                if ext == '.py' and module_name != '__init__':
                    module_path = os.path.join(folder_path, file_name)  # 获取模块文件的完整路径
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(module)  # 加载模块文件并执行其中的代码，将函数定义添加到 module 对象中
                    except:
                        continue
                    for name, obj in vars(module).items():
                        if callable(obj):
                            self.update_environments(name, obj)
        elif isinstance(folder_or_mnodule, types.ModuleType):
            module = folder_or_mnodule
            module = importlib.reload(module)
            for n, o in vars(module).items():
                if callable(o):
                    self.update_environments(n, o)
        else:
            raise TypeError("folder_or_module should be either a folder path (str) or a module (types.ModuleType).")


if __name__ == '__main__':
    lmff = LoadModulesFromFolder()
    # lmff.load_modules_from_folder(r'..\..\extensions')
    import extensions as es

    lmff.load_modules_from_folder(es)
    print(lmff.get_environments())
