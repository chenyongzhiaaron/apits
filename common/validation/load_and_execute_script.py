# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         load_and_execute_script.py
# Description:  模块脚本动态执行器
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2020/2/25 16:48
# -------------------------------------------------------------------------------


import importlib.util
import os
import sys

from common.validation.validator import Validator

sys.path.append('..')
sys.path.append('../utils')

from common.utils.exceptions import ScriptNotFoundError, ScriptExecuteError
from common.file_handling.file_utils import FileUtils


class LoadScript(Validator):

    def __init__(self):
        super().__init__()

    def load_script(self, script_path):

        """
        加载脚本文件并返回模块对象

        Args:
            script_path (str): 脚本文件的路径

        Returns:
            module: 脚本文件对应的模块对象
        """
        try:
            spec = importlib.util.spec_from_file_location(os.path.basename(script_path), script_path)
            script_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(script_module)
            return script_module
        except Exception as e:
            ScriptNotFoundError(script_path, e)
            return

    def load_and_execute_script(self, script_directory, script_name, request, method_name=None):
        """
        加载并执行脚本文件中的指定方法
        Args:
            request: 请求获响应对象
            script_directory (str): 脚本文件所在的目录
            script_name (str): 脚本文件的名称
            method_name (str): 要执行的方法的名称
        """
        if method_name is None:
            return request
        file_list = FileUtils.get_files_in_folder(script_directory)
        # 指定文件夹下是否存在这个测试用例脚本
        if script_name in file_list:
            script_path = FileUtils.get_file_path(script_name, script_directory)
            script = self.load_script(script_path)
            if script and hasattr(script, method_name):
                try:
                    method = getattr(script, method_name)
                    return method(request)
                except Exception as e:
                    ScriptExecuteError(script_path, e)
        return request


if __name__ == '__main__':
    from config.config import Config

    SCRIPTS_DIR = Config.SCRIPTS_DIR
    load_and_exe_s = LoadScript()
    load_and_exe_s.load_and_execute_script(SCRIPTS_DIR, 'prepost_script_sheetname_id.py', 'setup', {"y": "z"})
