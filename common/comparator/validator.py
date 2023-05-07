# coding: utf-8
# -------------------------------------------------------------------------------
# Name:         validator.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2023/03/24 17:32
# -------------------------------------------------------------------------------
import json

from common.comparator.comparator_dict import comparator_dict
from common.comparator.extractor import Extractor
from common.comparator.loaders import load_built_in_comparators
from common.tools.logger import MyLog

logger = MyLog()


class Validator(object):
    """
    校验器
    主要功能：
        1、格式化校验变量
        2、校验期望结果与实际结果与预期一致，并返回校验结果
    """

    def __init__(self):
        self.validate_variables_list = []

    def uniform_validate(self, validate_variables):
        """
        统一格式化测试用例的验证变量validate
        Args:
            validate_variables: 参数格式 list、dict
                示例：
                    [{"check":"result.user.name","comparator":"eq","expect":"chenyongzhi"}]
                    or {"check":"result.user.name","comparator":"eq","expect":"chenyongzhi"}

        Returns: 返回数据格式 list
                示例：
                    [{"check":"result.user.name","comparator":"eq","expect":"chenyongzhi"}]

        """
        if isinstance(validate_variables, list):
            for item in validate_variables:
                self.uniform_validate(item)
        elif isinstance(validate_variables, dict):
            if "check" in validate_variables.keys() and "expect" in validate_variables.keys():
                # 如果验证mapping中不包含comparator时，默认为{"comparator": "eq"}
                check_item = validate_variables.get("check")
                expect_value = validate_variables.get("expect")
                comparator = validate_variables.get("comparator", "eq")
                self.validate_variables_list.append({
                    "check": check_item,
                    "expect": expect_value,
                    "comparator": comparator
                })
        else:
            logger.my_log("参数格式错误！")

    def validate(self, resp_obj=None):
        """
        校验期望结果与实际结果与预期一致
        Args:
            resp_obj: ResponseObject对象实例

        Returns:

        """

        validate_pass = "PASS"
        built_in_comparators = load_built_in_comparators()

        # 记录校验失败的原因
        failure_reason = []
        for validate_variable in self.validate_variables_list:
            check_item = validate_variable['check']
            expect_value = validate_variable['expect']
            comparator = validate_variable['comparator']
            actual_value = Extractor.extract_value_by_jsonpath(resp_obj=resp_obj, expr=check_item)
            try:
                # 获取比较器
                fun = built_in_comparators[comparator]
                fun(actual_value=actual_value, expect_value=expect_value)
            except (AssertionError, TypeError):
                validate_pass = "FAIL"
                failure_reason.append({
                    '检查项': check_item,
                    '期望值': expect_value,
                    '实际值': actual_value,
                    '断言方法': comparator_dict.get(comparator),
                })
        return validate_pass, failure_reason

    def run_validate(self, validate_variables, resp_obj=None):
        """
         统一格式化测试用例的验证变量validate，然后校验期望结果与实际结果与预期一致
        Args:
            validate_variables:参数格式 list、dict
            resp_obj:ResponseObject对象实例

        Returns:返回校验结果

        """
        if not validate_variables:
            return ""
        self.uniform_validate(validate_variables)
        if not self.validate_variables_list:
            raise "uniform_validate 执行失败，无法进行 validate 校验"
        return self.validate(resp_obj)


if __name__ == '__main__':
    validate_variables1 = {"check": "$.result.user.name", "comparator": "eq", "expect": "chenyongzhi"}
        # {"check": "result.user", "comparator": "eq", "expect": "chen5yongzhi"}

    validate_variables2 = [
        {"check": "code", "comparator": "eq", "expect": "200"}
        # {"check": "result.user", "comparator": "eq", "expect": "chen5yongzhi"}
    ]
    resp_obj = {"code":200,"result": {"user": {"name": "chenyongzhi"}}}
    # t = Validator()
    for i in range(10):
        res = Validator().run_validate(validate_variables1, resp_obj)
        print(res)

