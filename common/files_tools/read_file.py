#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 9:21
# @Author  : kira
import json
import os
import sys

sys.path.append("../../")
# sys.path.append("../common")


from common.base_datas import BaseDates


def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        res = json.load(f)
    return res



if __name__ == '__main__':
    # file = os.path.join(BaseDates.base_path, "data", "bgy", "json_file", "assert_data_upload.json")
    # # file = os.path.join(BaseDates.base_path, "data", "bgy", "json_file", "user.json")
    # # file = r"/data/bgy/sql_file\clear_wifi_data.sql"
    # print(read_file(file))
    # print(type(read_file(file)))

    # dir_path = os.path.join(BaseDates.base_path, "data", "bgy", "excel_file", "wifi_import_file")
    # # 断言的文件
    # assertion_path = os.path.join(BaseDates.base_path, "data", "bgy", "json_file", "wifi", "assert_data_upload.json")
    # rest = list(zip(get_folder(dir_path), read_file(assertion_path)))
    # print(rest)
    test_case_path = os.path.join(BaseDates.base_path, "data", "bgy", "json_file", "user", "labor_register.json")
    test_case = read_file(test_case_path)
    print(test_case)
