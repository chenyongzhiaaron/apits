#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: load_modules_from_folder.py
@time: 2023/3/17 16:15
@desc:动态加载文件或模块
"""
import importlib.util
import os
import types

from common.data_extraction.dependent_parameter import DependentParameter
from common.utils.exceptions import DynamicLoadingError


class LoadModulesFromFolder(DependentParameter):
    def __init__(self):
        super().__init__()

    def load_modules_from_folder(self, folder_or_mnodule):
        """
        动态加载文件或模块
        """

        if isinstance(folder_or_mnodule, str):
            folder_path = folder_or_mnodule
            if not os.path.exists(folder_path):
                raise ValueError("Folder path does not exist.")

            for file_name in os.listdir(folder_path):
                module_name, ext = os.path.splitext(file_name)
                if ext == '.py' and module_name != '__init__':
                    module_path = os.path.join(folder_path, file_name)
                    spec = importlib.util.spec_from_file_location(module_name, module_path)
                    module = importlib.util.module_from_spec(spec)
                    try:
                        spec.loader.exec_module(module)
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
            raise DynamicLoadingError(folder_or_mnodule,
                                      "older_or_module should be either a folder path (str) or a module ("
                                      "types.ModuleType).")


if __name__ == '__main__':
    lmff = LoadModulesFromFolder()
    # lmff.load_modules_from_folder(r'..\..\extensions')
    import extensions as es

    lmff.load_modules_from_folder(es)
    print(lmff.get_environments())
