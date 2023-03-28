# -*- coding: utf-8 -*-
# @Time : 2019/11/18 15:32
# @Author : kira
# @Email : 262667641@qq.com
# @File : run_main.py
# @Project : risk_api_project

import os
import sys
import unittest
import re

sys.path.append("./common")
sys.path.append("./")

from common.base_datas import BaseDates
# from common.decorator_send_info import decorator_send_info
from HTMLTestRunnerNew import HTMLTestRunner


# @decorator_send_info()
def run_test_case(case_name, url_key=None):
    # test_report = BaseDates.test_report
    test_report = r"E:\Program Project\api-test-project\scrit\apifox-reports"
    t_case = unittest.defaultTestLoader.discover(BaseDates.script, pattern=f"{case_name}.py")
    with open(BaseDates.test_report + f"/{case_name} 测试报告.html", "wb") as fb:
        runner = HTMLTestRunner(stream=fb, verbosity=2, title=f"{case_name} 接口自动化测试报告",
                                description="接口自动化测试")
        # 失败重跑
        # runner.run(test_case, 0, False)
        runner.run(t_case)
        data = [url_key, test_report]
    return data


def run():
    keys = {"test_api": "8b1647d4-dc32-447c-b524-548acf18a938"  # 企業微信key
            }
    # 获取测试用例脚本文件夹下所有文件
    test_case_names = os.listdir(BaseDates.script)
    for name in test_case_names:
        if re.match(r"test_api.+?py", name):
            test_case = re.match(r"test.+?py", name).group()
            case = test_case.split(".")[0]
            for key, value in keys.items():
                print(f"當前運行的用例：{key}; 對應的機器人key： {value}")
                if key in case:
                    run_test_case(case, value)
                else:
                    print("No script to be executed")


if __name__ == '__main__':
    run()

