#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/10/12 11:12
# @Author  : kira


# -*- coding: utf-8 -*-
# @Time : 2021/7/6 15:31
# @Author : kira
# @Email : 262667641@qq.com
# @File : test_wifi_upload_file.py
# @Project : api-test-project
import os
import random
import sys

import jsonpath

from common.file_handling.file_utils import FileUtils

sys.path.append("../../")
sys.path.append("../../common")

from common.http_client.http_client import Pyt
from common.config import Config
from common.random_tools.names import name
from common.random_tools.phone_numbers import phone
from common.random_tools.identification import idcard

pyt = Pyt()


def test_labor_register(cases):
    host = 'https://bimuse.bzlrobot.com/bsp/test/user/ugs'
    headers = {"BSP_APP_ID": "8d1f5bdc9c6648af84a98e2c017846c5",
               "BSP_TOKEN": "32c9fd9ccc0565d0281b89b5fa198008",
               "BSP_USER_ENV_ID": "f8e334ea85df45ed99a311ed022c2973",
               "BSP_USER_ID": "216684145642752200",
               "BSP_USER_TENANT": "216856950236843913",
               "bzlrobot-authorization": "bearer 32c9fd9ccc0565d0281b89b5fa198008",
               "projectId": "99000022",
               "projectName": "%E4%BD%9B%E5%B1%B1%E9%99%88%E6%9D%91%E6%97%A7%E6%94%B9%E9%A1%B9%E7%9B%AE"
               }
    sex_id = random.randint(0, 1)
    user_sex = "F" if sex_id == 0 else "M"
    user_name = name.get_girl() if sex_id == 0 else name.get_boy()
    user_id_card = idcard.get_generate_id(sex=sex_id)
    user_birthday = idcard.get_birthday(user_id_card)
    user_mobile = phone.get_mobile_number()
    # 请求工种接口，获取所有工种
    url = f"/ibs/api/ibs-lms-base/work-kind/page/list?t=1636702597000&current=1&size=1000&projectId={cases['projectId']}&key=&supplyId=&status=0&enabled=1"
    kwargs = {
        "headers": headers
    }
    res = pyt.http_client(host, url, "GET", **kwargs).json()
    codes = jsonpath.jsonpath(res, "$.data..code")
    names = jsonpath.jsonpath(res, "$.data..name")
    work_kinds = dict(zip(codes, names))
    work_code = random.choice(list(work_kinds.keys()))
    cases["name"] = user_name
    cases["idCard"]["name"] = user_name
    cases["idCard"]["cardNo"] = user_id_card
    cases["phone"] = user_mobile
    cases["idCard"]["sex"] = user_sex
    cases["idCard"]["birthday"] = user_birthday
    cases['workKindCode'] = str(work_code)
    cases['workKindName'] = work_kinds[str(work_code)]
    if "positionName" in cases:
        url = "/ibs/api/ibs-lms-member/manager/register?t=1634607524000"
    else:
        url = "/ibs/api/ibs-lms-member/labor/register?t=1633743835000"
    try:
        kwargs.update({"json": cases})
        res = pyt.http_client(host, url, "POST", **kwargs)
        assert res.status_code == 200
    except Exception as e:
        raise e


if __name__ == '__main__':
    # 测试数据路径
    test_case_path = os.path.join(Config.base_path, 'cases', 'cases', "labor.json")

    test_case = FileUtils().read_json_file(test_case_path)
    for i in range(500):
        test_labor_register(test_case)
