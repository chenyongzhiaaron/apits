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
        self.P = Dependence.PATTERN
        self.p = Dependence.pattern
        self.pf = Dependence.pattern_fun

    def replace_dependent_parameter(self, jst):
        """
        替换字符串中的关联参数，并返回转化后的字典格式。
        Args:
            jst: 包含接口参数的字符串
        Returns:转换后的字典或原始字符串
        """
        # logger.my_log(f"正在执行数据替换：提取数据源内容:{jst}", "info")
        if not jst:
            return jst
        jst = json.dumps(jst) if isinstance(jst, (dict, list)) else jst
        # 替换
        while self.P.search(jst):
            if self.pf.search(jst):
                # 函数替换
                key = self.pf.search(jst).group()
                if key in Dependence.get_dep().keys():
                    value_ = Dependence.get_dep(key)()
                    jst = jst.replace(key, str(value_))
                    logger.my_log(f"key:{key},替换结果为--> {Dependence.get_dep(key)()}")
                else:
                    logger.my_log(f"key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            else:
                key = self.P.search(jst).group()
                # 字符串替换
                if key in Dependence.get_dep().keys():
                    jst = jst.replace(key, str(Dependence.get_dep(key)))
                    logger.my_log(f"key:{key},替换结果为--> {Dependence.get_dep(key)}")
                else:
                    logger.my_log(f"key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
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
        "f": "{{var_f}}",
        "g": "{{var_g}}",
        "t": "{{get_timestamp()}}"
    }
    t = DependentParameter().replace_dependent_parameter(dat)
    print(t)
