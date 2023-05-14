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

from common.files_tools.get_file import get_file

sys.path.append("./common")
sys.path.append("./")

from common.base_datas import BaseDates
from HTMLTestRunnerNew import HTMLTestRunner
from unittestreport import TestRunner


# @decorator_send_info()
def run(case_name='T', url_key=None):
    test_report = BaseDates.test_report
    print(f"当前测试报告路劲: {test_report}，测试脚本路劲: {BaseDates.script}")
    t_case = unittest.defaultTestLoader.discover(BaseDates.script, pattern="test_*.py")
    runner = TestRunner(t_case, report_dir=test_report, filename=case_name, title="接口自动化测试报告", templates=2,
                        tester="kira", desc="自动化测试")
    runner.run()
    # with open(test_report + f"/{case_name} 测试报告.html", "wb") as fb:
    #     runner = HTMLTestRunner(stream=fb, verbosity=2, title=f"{case_name} 接口自动化测试报告",
    #                             description="接口自动化测试")
    #     runner.run(t_case)
    # data = [url_key, test_report]
    # return data


def start():
    run()


if __name__ == '__main__':
    start()
