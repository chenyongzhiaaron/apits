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
import re

from common.dependence import Dependence
from common.tools.logger import MyLog
from common.tools.singleton import singleton

logger = MyLog()


# @singleton
class DependentParameter:
    """
       该类用于替换接口参数。它会从字符串中寻找需要替换的参数，并将其替换为关联参数表中对应的值。
       然后，它将替换后的字符串转化为字典并返回。如果找不到需要替换的参数，则直接返回原始字符串。
    """

    def __init__(self):
        self.P = Dependence.pattern_l  # re.compile(r"{{\s*([^}\s]+)\s*}}(?:\[(\d+)\])?")
        self.pp = Dependence.PATTERN  # re.compile(r"{{(.*?)}}")
        self.p = Dependence.pattern  # re.compile(r'({)')
        self.pf = Dependence.pattern_fun  # re.compile(r"{{(\w+\(\))}}")

    def replace_dependent_parameter(self, jst):
        """
        替换字符串中的关联参数，并返回转化后的字典格式。
        Args:
            jst: 包含接口参数的字符串
        Returns:转换后的字典或原始字符串
        """
        if not jst:
            return jst
        jst = json.dumps(jst) if isinstance(jst, (dict, list)) else jst
        # 循环替换参数
        while self.P.search(jst):
            if self.pf.search(jst):
                # 函数替换
                key = self.pf.search(jst).group()
                if key in Dependence.get_dep().keys():
                    # 如果参数名称存在于关联参数表中，则调用相应的函数获取返回值，并替换字符串中的参数
                    value_ = Dependence.get_dep(key)()
                    jst = jst.replace(key, str(value_))
                    # logger.my_log(f"key:{key},替换结果为--> {str(value_)}")
                else:
                    logger.my_log(f"key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            else:
                key = self.P.search(jst)
                # 字符串替换，判断需要替换的字符串是{{key}}还是{{key}}[index]
                if "[" and "]" in key.group():
                    # 如果需要替换的是数组参数，则获取数组下标
                    index = int(key.group(2))
                    k = self.pp.search(key.group()).group()
                else:
                    index = ""
                    k = key.group()
                # 如果参数名称存在于关联参数表中，则获取相应的值，并替换字符串中的参数
                if k in Dependence.get_dep().keys():
                    if isinstance(index, int):
                        value_ = Dependence.get_dep(k)[index]
                    else:
                        value_ = Dependence.get_dep(k)
                    jst = jst.replace(key.group(), str(value_))
                    # logger.my_log(f"key:{key},替换结果为--> {str(value_)}")
                else:
                    logger.my_log(f"key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            # 将 True 和 False 转换为小写，并继续循环替换参数
            jst = jst.replace("True", "true").replace("False", "false")
        if self.p.search(jst) and not self.pf.search(jst):
            try:
                jst = json.loads(jst)
            except json.JSONDecodeError as e:
                logger.my_log(f"JSONDecodeError:{jst}:{e}")
        return jst


if __name__ == '__main__':
    dps = {
        "{{var_a}}": "foo",
        "{{var_c}}": 123,
        "{{var_d}}": None,
        "{{var_e_1}}": True,
        "{{var_e_2}}": "bar",
        "{{var_f}}": ["baz", False],
        "{{var_g}}": {'g': 'gg', 'g1': 'gg', 'g2': 'gg2'}
    }
    from common.comparator import loaders
    from common import bif_functions

    d = Dependence
    d.set_dep(dps)
    loaders.set_bif_fun(bif_functions)
    dat = {
        "a": "{{var_a}}",
        "b": {"c": "{{var_c}}", "d": "{{var_d}}", "e": ["{{var_e_1}}", "{{var_e_2}}"]},
        "f": "{{var_f}}[0]",
        "g": "{{var_g}}",
        "t": "{{get_timestamp()}}"
    }
    t = DependentParameter().replace_dependent_parameter(dat)
    print(t)
