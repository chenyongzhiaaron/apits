# -*- coding:utf-8 -*-
"""
@author: kira
@contact: 262667641@qq.com
@file: data_extractor.py
@time: 2023/3/24 10:32
@desc:
"""
import json
import re
import sys

sys.path.append("../")
sys.path.append("./common")
from jsonpath_ng import parse
from common.utils.environments import Environments
from common.utils.exceptions import logger, InvalidParameterFormatError, ParameterExtractionError

REPLACE_DICT = {
    "null": None,
    "True": True,
    "false": False
}


class DataExtractor(Environments):

    def __init__(self):
        super().__init__()

    @logger.catch
    def substitute_data(self, response, regex=None, keys=None, deps=None, jp_dict=None):
        """
        数据提取
        Args:
            response: 被提取数据对象
            regex:  正则表达式： r'"id": (\d+), "name": "(\w+)",'
            keys:  接收正则表达式返回结果的key： ["a", "b"]
            deps: "name=data[0].name;ok=data[0].id;an=data[0].age[3].a"
            jp_dict: jsonpath 提取方式入参：{"k": "$.data", "x": "$.data[0].age[3].a"}
        Returns:
        """

        response = response
        if not isinstance(response, (dict, str, list)):
            InvalidParameterFormatError(response, "| 被提取对象非字典、非字符串、非列表，不执行jsonpath提取")
            return {}
        if regex and keys:
            self.substitute_regex(response, regex, keys)
        response = response if isinstance(response, (dict, list)) else json.loads(response)
        if deps:
            self.substitute_route(response, deps)
        if jp_dict:
            self.substitute_jsonpath(response, jp_dict)

    def substitute_regex(self, response, regex, keys):
        """
        使用正则表达式
        Args:
            response:
            regex: 正则表达式：r'"id": (\d+), "name": "(\w+)",'
            keys:结果键列表：["a", "b"],
        Returns:

        """
        response = json.dumps(response) if isinstance(response, (dict, list)) else response
        match = re.search(regex, response)
        if not match:
            return {}
        groups = match.groups()
        for i, key in enumerate(keys):
            try:
                self.update_environments(key, groups[i])
            except:
                self.update_environments(key, None)

    def substitute_route(self, response, route_str):
        """
        字典取值
        Args:
            response:
            route_str:

        Returns:

        """
        deps_list = re.sub(f"[\r\n]+", "", route_str).split(";")
        for dep_item in deps_list:
            key, value_path = dep_item.split("=")
            value_path_parts = re.findall(r'\w+', value_path)
            temp = response
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
                self.update_environments(key, temp)

    def substitute_jsonpath(self, response, json_path_dict):
        """
        jsonpath取值
        Args:
            response:
            json_path_dict: {"k": "$.data", "x": "$.data[0].age[3].a"}

        Returns: 字符串或者list

        """
        json_path_dict = json_path_dict if isinstance(json_path_dict, dict) else json.loads(json_path_dict)
        for key, expression in json_path_dict.items():
            try:
                parsed_expression = parse(expression)
                data = response
                # 使用解析器对象进行匹配和提取
                match = parsed_expression.find(data)
                result = [m.value for m in match]
                self.update_environments(key, result[0]) if len(result) == 1 else self.update_environments(key,
                                                                                                           result)
            except Exception as e:
                ParameterExtractionError(expression, e)


if __name__ == '__main__':
    # 测试subs函数
    res = '{"code": 1,"data": [{"id": 1, "name": "Alice", "age": [20, 21, 22, {"a": "b"}]}]}'
    lists = {"k": "$..code", "x": "$.data[0].age[3].a"}
    dep_str = "name=data[0].name;ok=data[0].id;an=data[0].age"
    regex_str = r'"id": (\d+), "name": "(\w+)",'
    regex_key = ["a", "b"]
    t = DataExtractor()
    t.substitute_data(res, regex=regex_str, keys=regex_key, deps=dep_str, jp_dict=lists)
    print("-------->res:", t.get_environments())
