# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         loader.py
# Description:  加载器
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2019/11/18 17:32
# -------------------------------------------------------------------------------
import types

from common.http_client.http_client import HttpClient
from common.validation import logger


class Loaders(HttpClient):
    def __init__(self):
        super().__init__()

    @logger.catch
    def load_built_in_functions(self, model) -> dict:
        """
        加载指定模块下的所有函数
        Returns:
        """
        built_in_functions = {}
        for name, item in vars(model).items():
            if isinstance(item, types.FunctionType):
                built_in_functions[name] = item
        return built_in_functions

    @logger.catch
    def set_bif_fun(self, model):
        """
        加载内置方法
        Returns:

        """
        for k, v in self.load_built_in_functions(model).items():
            self.update_environments(f"{k}()", v)


if __name__ == '__main__':
    from encryption_rules import rules

    loaders = Loaders()
    res = loaders.load_built_in_functions(rules)
    print(res)
