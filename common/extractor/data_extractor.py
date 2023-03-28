# -*- coding:utf-8 -*-
"""
Time: 2020/6/1/001 15:29
Author: 陈勇志
Email:262667641@qq.com
Project:api_project
"""
import sys
import json
import re

sys.path.append("../")
sys.path.append("./common")
from common.tools.singleton import singleton
from jsonpath_ng import parse
from common.dependence import Dependence
from common.tools.logger import MyLog

REPLACE_DICT = {
    "null": None,
    "True": True,
    "false": False
}

dependence = Dependence()


@singleton
class DataExtractor:

    def __init__(self, response=None):
        self.dependence = dependence.dependence
        # self.dependence = getattr(Dependence, "dependence")
        self.response = response
        self.PATTERN = getattr(Dependence, "PATTERN")  # 预编译正则表达式

    # def update_dependence(self, key, value):
    #     # self.dependence[f"{{{{{key}}}}}"] = value
    #     dependence.update_dependence(key, value)

    def substitute_data(self, regex=None, keys=None, deps=None, jp_dict=None):
        """
        方法接收一个正则表达式 regex 和一个关联参数表 deps，用于从接口返回的数据中提取关联参数。
        它会从接口返回的数据中使用正则表达式 regex 和正则表达式返回结果的键列表 keys 提取数据，并将其更新到关联参数表中。
        然后，它会使用 subs_deps 和 subs_lists 方法提取更多的关联参数。最后，它将更新后的关联参数表设置为 Dependence 类的静态变量，并将其返回
        Args:
            regex:  正则表达式： r'"id": (\d+), "name": "(\w+)",'
            keys:  接收正则表达式返回结果的key： ["a", "b"]
            deps: "name=data[0].name;ok=data[0].id;an=data[0].age[3].a"
            jp_dict: jsonpath 提取方式入参：{"k": "$.data", "x": "$.data[0].age[3].a"}

        Returns:

        """
        if not isinstance(self.response, (dict, str, list)):
            return {}
        if regex and keys:
            self.response = json.dumps(self.response) if isinstance(self.response, (dict, list)) else self.response
            self.substitute_regex(regex, keys)
        self.response = self.response if isinstance(self.response, (dict, list)) else json.loads(self.response)
        if deps:
            self.substitute_route(deps)
        if jp_dict:
            self.substitute_jsonpath(jp_dict)
        dependence.set_dep(self.dependence)
        # setattr(Dependence, "dependence", self.dependence)
        return self.dependence

    def substitute_regex(self, regex, keys):
        """
        方法用于使用正则表达式 regex 和正则表达式返回结果的键列表 keys 从接口返回的数据中提取数据，并将其更新到关联参数表中。
        Args:
            regex: 正则表达式：r'"id": (\d+), "name": "(\w+)",'
            keys:结果键列表：["a", "b"],
        Returns:

        """
        match = re.search(regex, self.response)
        if not match:
            return {}
        groups = match.groups()
        for i, key in enumerate(keys):
            try:
                dependence.update_dep(key, groups[i])
                # self.update_dependence(key, groups[i])
            except:
                dependence.update_dep(key, None)
                # self.update_dependence(key, None)

    def substitute_route(self, route_str):
        deps_list = re.sub(f"[\r\n]+", "", route_str).split(";")
        for dep_item in deps_list:
            key, value_path = dep_item.split("=")
            value_path_parts = re.findall(r'\w+', value_path)
            temp = self.response
            for part in value_path_parts:
                if isinstance(temp, dict):
                    temp = temp.get(part)
                elif isinstance(temp, list):
                    if part.isdigit():
                        index = int(part)
                        if index < len(temp):
                            temp = temp[index]
                        else:
                            temp = None
                            break
                    else:
                        temp = None
                        break
                else:
                    temp = None
                    break
                if isinstance(temp, (dict, list)):
                    continue
                else:
                    break
            if temp is not None:
                dependence.update_dep(key, temp)
                # self.update_dependence(key, temp)

    def substitute_jsonpath(self, json_path_dict):
        """
        jsonpath 提取参数
        Args:
            json_path_dict: {"k": "$.data", "x": "$.data[0].age[3].a"}

        Returns: 字符串或者list

        """
        for key, expression in json_path_dict.items():
            try:
                parsed_expression = parse(expression)
                data = self.response
                match = parsed_expression.find(data)
                # print(match)
                result = [m.value for m in match]
                dependence.update_dep(key, result[0]) if len(result) == 1 else dependence.update_dep(key, result)
                # self.update_dependence(key, result[0]) if len(result) == 1 else self.update_dependence(key, result)
            except Exception as e:
                MyLog().my_log(f"jsonpath表达式错误'{expression}': {e}")


if __name__ == '__main__':
    # 测试subs函数
    res = {"code": 1,
           "data": [
               {"id": 1, "name": "Alice", "age": [20, 21, 22, {"a": "b"}]}
           ]
           }
    lists = {"k": "$..code", "x": "$.data[0].age[3].a"}
    dep_str = "name=data[0].name;ok=data[0].id;an=data[0].age"
    regex_str = r'"id": (\d+), "name": "(\w+)",'
    regex_key = ["a", "b"]
    t = DataExtractor(res)
    t.substitute_data(regex=regex_str, keys=regex_key, deps=dep_str, jp_dict=lists)
    print(t.dependence)
