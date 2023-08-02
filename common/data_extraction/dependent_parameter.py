#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: restr.py
@time: 2023/3/24 10:32
@desc:
"""
import json

from common.data_extraction import logger
from common.data_extraction.data_extractor import DataExtractor


class DependentParameter(DataExtractor):
    """
       该类用于替换接口参数。它会从字符串中寻找需要替换的参数，并将其替换为关联参数表中对应的值。
       然后，它将替换后的字符串转化为字典并返回。如果找不到需要替换的参数，则直接返回原始字符串。
    """

    def __init__(self):
        super().__init__()

    # @logger.log_decorator()
    def replace_dependent_parameter(self, json_string):
        """
        替换字符串中的关联参数，并返回转化后的字典格式。
        Args:
            json_string: 包含接口参数的字符串
        Returns:转换后的字典或原始字符串
        """

        def execute_method_chain(obj, methods, args=None):
            """调用函数兼容调用方法链"""
            if not methods:
                if callable(obj):
                    return obj(*args)
                else:
                    return obj
            method_name, *remaining_methods = methods
            if hasattr(obj(), method_name) and callable(getattr(obj(), method_name)):
                method = getattr(obj(), method_name)
                return execute_method_chain(method(), remaining_methods)
            else:
                # 如果方法不存在或不可调用，则返回None
                return None

        def get_method_call_and_method_names(strings):
            """获取方法调用和方法名"""
            first_method_call_match = self.FUNCTION_CALL_MATCHER.search(strings)
            if first_method_call_match:
                first_method_call = "{{" + f'{first_method_call_match.group()}'.split("(")[0] + "()" + "}}"
                first_fun = first_method_call_match.group()
                args_string = self.ARGS_MATCHER.search(first_method_call_match.group())
                if args_string:
                    args_list = args_string.group(1).split(',')

                else:
                    args_list = []
            else:
                raise ValueError("函数写法错误")
            remaining_method_names = self.METHOD_NAME_MATCHER.findall(strings)
            return first_fun, first_method_call, remaining_method_names, args_list

        if not json_string:
            return json_string
        json_string = json.dumps(json_string) if isinstance(json_string, (dict, list)) else json_string
        # 循环替换参数
        while self.PARAMETER_MATCHER.search(json_string):
            if self.FUNCTION_CHAIN_MATCHER.search(json_string):
                # 函数替换
                function_pattern = self.FUNCTION_CHAIN_MATCHER.search(json_string).group()
                function_with_args, key, remaining_methods, args = get_method_call_and_method_names(function_pattern)
                if key in self.get_environments().keys():
                    # 如果参数名称存在于关联参数表中，则调用相应的函数获取返回值，并替换字符串中的参数
                    obj = self.get_environments(key)
                    obj = execute_method_chain(obj, remaining_methods, args=args)
                    json_string = json_string.replace(function_pattern, str(obj))
                else:
                    logger.error(
                        f"函数key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            else:
                key = self.PARAMETER_MATCHER.search(json_string)
                # 字符串替换，判断需要替换的字符串是{{key}}还是{{key}}[index]
                if "[" and "]" in key.group():
                    # 如果需要替换的是数组参数，则获取数组下标
                    index = int(key.group(2))
                    k = self.PARAMETER_PATTERN.search(key.group()).group()
                else:
                    index = ""
                    k = key.group()
                # 如果参数名称存在于关联参数表中，则获取相应的值，并替换字符串中的参数
                if k in self.get_environments().keys():
                    if isinstance(index, int):
                        obj = self.get_environments(k)[index]
                    else:
                        obj = self.get_environments(k)
                    json_string = json_string.replace(key.group(), str(obj))
                else:
                    logger.error(
                        f"字符串key:{key},字符串在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            # 将 True 和 False 转换为小写，并继续循环替换参数
            json_string = json_string.replace("True", "true").replace("False", "false")
        if self.BRACE_MATCHER.search(json_string) and not self.FUNCTION_CHAIN_MATCHER.search(json_string):
            try:
                json_string = json.loads(json_string)
            except json.JSONDecodeError as e:
                logger.error(f"JSONDecodeError:{json_string}:{e}")
        return json_string


if __name__ == '__main__':
    from common.utils.environments import Environments

    dps = {
        "{{var_a}}": "foo",
        "{{var_c}}": 123,
        "{{var_d}}": None,
        "{{var_e_1}}": True,
        "{{var_e_2}}": "bar",
        "{{var_f}}": ["baz", False],
        "{{var_g}}": {'g': 'gg', 'g1': 'gg', 'g2': 'gg2'}
    }

    d = Environments()
    d.set_environments(dps)
    from common.validation import loaders
    from common import bif_functions

    loaders.Loaders().set_bif_fun(bif_functions)
    dat = {
        "a": "{{var_a}}",
        "b": {"c": "{{var_c}}", "d": "{{var_d}}", "e": ["{{var_e_1}}", "{{var_e_2}}"]},
        "f": "{{var_f}}[1]",
        "g": "{{var_g}}",
        "t": "{{get_timestamp()}}",
        "fk": "{{fk().email()}}",
        "rt": "{{fk().ean(length=13)}}",
        "st": "{{ms_fmt_hms(2000)}}"
    }
    d = DependentParameter()
    print(d.replace_dependent_parameter(dat))
