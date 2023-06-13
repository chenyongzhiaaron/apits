#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 9:21
# @Author  : kira
import json
import os
import sys

sys.path.append("../../")


# sys.path.append("../common")


def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        res = json.load(f)
    return res


if __name__ == '__main__':
    from common.config import BaseDates

    test_case_path = os.path.join(BaseDates.base_path, "data", "bgy", "json_file", "user", "labor_register.json")
    test_case = read_file(test_case_path)
    print(test_case)
