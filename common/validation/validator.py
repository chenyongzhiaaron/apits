# coding: utf-8
# -------------------------------------------------------------------------------
# Name:         validator.py
# Description:  校验器
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2023/03/24 17:32
# -------------------------------------------------------------------------------
import json

from common.validation import comparators
from common.crypto.encrypt_data import EncryptData
from common.utils.exceptions import InvalidParameterFormatError
from common.validation.extractor import Extractor


# from common.validation.loaders import Loaders


class Validator(Extractor, EncryptData):
    """
    校验器
    主要功能：
        1、格式化校验变量
        2、校验期望结果与实际结果与预期一致，并返回校验结果
    """
    validate_variables_list = []
    assertions = []

    def __init__(self):
        super().__init__()

    def uniform_validate(self, validate_variables):
        """
        统一格式化测试用例的验证变量validate
        Args:
            validate_variables: 参数格式 list、dict
                示例：
                    [{"check":"result.user.name","comparator":"eq","expect":"kira"}]
                    or {"check":"result.user.name","comparator":"eq","expect":"kira"}

        Returns: 返回数据格式 list
                示例：
                    [{"check":"result.user.name","comparator":"eq","expect":"kira"}]

        """
        if isinstance(validate_variables, str):
            validate_variables = json.loads(validate_variables)
        if isinstance(validate_variables, list):
            for item in validate_variables:
                self.uniform_validate(item)
        elif isinstance(validate_variables, dict):
            if "check" in validate_variables.keys() and "expect" in validate_variables.keys():
                # 如果验证mapping中不包含comparator时，默认为{"comparator": "eq"}
                check_item = validate_variables.get("check")
                expect_value = validate_variables.get("expect")
                comparator = validate_variables.get("comparator", "eq")
                ignore = validate_variables.get("ignore")
                self.validate_variables_list.append({
                    "check": check_item,
                    "expect": expect_value,
                    "comparator": comparator,
                    "ignore": ignore
                })
        else:
            InvalidParameterFormatError(validate_variables, "参数格式错误！")

    def validate(self, resp=None):
        """
        校验期望结果与实际结果与预期一致
        Args:
            resp: ResponseObject对象实例

        Returns:

        """

        for validate_variable in self.validate_variables_list:
            check_item = validate_variable.get('check')
            expect_value = validate_variable.get('expect')
            comparator = validate_variable.get('comparator')
            ignore = validate_variable.get("ignore")
            if not str(check_item).startswith("$"):
                actual_value = check_item
            else:
                actual_value = self.extract_value_by_jsonpath(resp_obj=resp, expr=check_item)
            e = None
            try:
                fun = self.load_built_in_functions(comparators)[comparator]
                fun(actual_value=actual_value, expect_value=expect_value, ignore=ignore)
                validate_result = "通过"
            except (AssertionError, TypeError) as err:
                validate_result = "失败"
                e = err
                raise e
            finally:
                self.assertions.append(dict(检查项=check_item,
                                            期望值=expect_value,
                                            实际值=actual_value,
                                            忽略对比字段=ignore,
                                            断言方法=comparator,
                                            断言结果=validate_result,
                                            失败信息=e))

    def run_validate(self, validate_variables, resp=None):
        """
         统一格式化测试用例的验证变量validate，然后校验期望结果与实际结果与预期一致
        Args:
            validate_variables:参数格式 list、dict
            resp:ResponseObject对象实例

        Returns:返回校验结果

        """
        if not validate_variables:
            self.assertions = ['未填写预期结果，默认断言HTTP请求状态码！！！']
            return
        self.validate_variables_list.clear()
        self.assertions.clear()
        self.uniform_validate(validate_variables)
        if not self.validate_variables_list:
            raise InvalidParameterFormatError(self.validate_variables_list,
                                              "uniform_validate 执行失败，无法进行 validate 校验")
        self.validate(resp)


if __name__ == '__main__':
    validate_variables1 = {"check": "$.result.user.name", "comparator": "eq", "expect": "chenyongzhi"}
    resp_obj = {"code": "200", "result": {"user": {"name": "chenyongzhi"}}}
    validate_variables2 = [
        {"check": resp_obj, "comparator": "check", "expect": {"result": {"user": {"name": "chenyongzhi"}}}}
    ]
    validator = Validator()
    validator.run_validate(validate_variables2, resp_obj)
    print(validator.assertions)
