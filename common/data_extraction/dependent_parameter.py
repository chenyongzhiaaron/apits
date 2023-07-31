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
    
    @logger.log_decorator()
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
        while self.pattern_l.search(jst):
            if self.pattern_fun.search(jst):
                # 函数替换
                key = self.pattern_fun.search(jst).group()
                if key in self.get_environments().keys():
                    # 如果参数名称存在于关联参数表中，则调用相应的函数获取返回值，并替换字符串中的参数
                    value_ = self.get_environments(key)()
                    jst = jst.replace(key, str(value_))
                else:
                    logger.error(
                        f"key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            else:
                key = self.pattern_l.search(jst)
                # 字符串替换，判断需要替换的字符串是{{key}}还是{{key}}[index]
                if "[" and "]" in key.group():
                    # 如果需要替换的是数组参数，则获取数组下标
                    index = int(key.group(2))
                    k = self.PATTERN.search(key.group()).group()
                else:
                    index = ""
                    k = key.group()
                # 如果参数名称存在于关联参数表中，则获取相应的值，并替换字符串中的参数
                if k in self.get_environments().keys():
                    if isinstance(index, int):
                        value_ = self.get_environments(k)[index]
                    else:
                        value_ = self.get_environments(k)
                    jst = jst.replace(key.group(), str(value_))
                else:
                    logger.error(
                        f"key:{key},在关联参数表中查询不到,请检查关联参数字段提取及填写是否正常\n")
                    break
            # 将 True 和 False 转换为小写，并继续循环替换参数
            jst = jst.replace("True", "true").replace("False", "false")
        if self.pattern.search(jst) and not self.pattern_fun.search(jst):
            try:
                jst = json.loads(jst)
            except json.JSONDecodeError as e:
                logger.error(f"JSONDecodeError:{jst}:{e}")
        return jst


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
        "t": "{{get_timestamp()}}"
    }
    d = DependentParameter()
    print("=====》res: ", d.replace_dependent_parameter(dat))
