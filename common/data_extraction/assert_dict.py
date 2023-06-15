# -*- coding: utf-8 -*-
# @Time : 2019/11/19 14:29
# @Author : kira
# @Email : 262667641@qq.com
# @File : assert_dict.py
# @Project : risk_api_project
import sys

sys.path.append("../")
sys.path.append("./common")
from common.data_extraction.analysis_json import AnalysisJson
from common.utils.singleton import singleton


@singleton
class AssertDict(object):

    @staticmethod
    def is_contain(expect_result, response_result):
        """
        Args:
            response_result:
            expect_result:
            expect_result:
        """
        assert expect_result.items() <= response_result.items()

    @staticmethod
    def assert_value(expect_result, response_result):
        """
        :param expect_result: 预期结果
        :param response_result: 响应结果
        :return:
        """
        contain_expect_key_dict = []  # 所有预期结果的字典key
        expect_value_list = []  # 所有预期结果的字典value
        tmp_list = []
        need_search_key = []
        res_list = {}
        for key, value in expect_result.items():
            expect_value_list.append(value)
            need_search_key.append(key)
        for expect_value in need_search_key:
            # 接收由预期key在实际响应中的所有值,返回的是一个[]
            try:
                contain_expect_key_dict = (AnalysisJson().get_target_value(
                    expect_value, response_result, tmp_list))
            except Exception as identifier:
                print("查找值异常：{}".format(contain_expect_key_dict))
                raise identifier
        for each_value in expect_value_list:
            # 判断是否每一个由预期结果组成的列表中，每一个值都存在由预期key组成的实际结果列表中
            try:
                if each_value in contain_expect_key_dict:
                    res_list["${}".format(each_value)] = True
                else:
                    res_list["${}".format(each_value)] = False
            except Exception as e:
                print("字典的key异常{}".format(each_value))
                raise e
        if False in res_list.values():
            flag = 0
        else:
            flag = 1
        return flag, res_list


if __name__ == '__main__':
    first = {
        "data": [{
            "saleRatio": "14.29",
            "weekDate": "2021-04-15"

        }, {
            "weekDate": "2021-04-16",
            "saleRatio": "14.29"
        }, {
            "weekDate": "2021-04-17",
            "saleRatio": "14.29"
        }, {
            "weekDate": "2021-04-18",
            "saleRatio": "14.29"
        }, {
            "weekDate": "2021-04-19",
            "saleRatio": "14.29"
        }, {
            "weekDate": "2021-04-20",
            "saleRatio": "14.29"
        }, {
            "weekDate": "2021-04-21",
            "saleRatio": "14.29"
        }],
        "status": 200
    }
    second = {"data": [{
        "weekDate": "2021-04-19",
        "saleRatio": "14.29"
    }], "status": 200}

    expect = {
        "status": "success",
        "code": 200,
        "message": "OK"
    }

    response = {
        "status": "success",
        "code": 200,
        "message": "OK",
        "data": {
            "id": 123,
            "name": "John"
        }
    }
    print(AssertDict().assert_value(second, first))
    print(AssertDict().assert_value(expect, response))
