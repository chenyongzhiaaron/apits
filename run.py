# -*- coding: utf-8 -*-
# @Time : 2019/11/18 15:32
# @Author : kira
# @Email : 262667641@qq.com
# @File : run_main.py
# @Project : risk_api_project
import sys
import unittest

sys.path.append("./common")
sys.path.append("./")
sys.path.append('cases')

from config import Config
# from unittestreport import TestRunner
from unittestreportnew import TestRunner


def run():
    test_report = Config.test_report
    test_case = unittest.defaultTestLoader.discover(Config.script, pattern="test_*.py")
    runner = TestRunner(test_case, report_dir=test_report, title="接口自动化测试报告", templates=2, tester="kira",
                        desc="自动化测试")
    runner.run()
    # get_failed_test_cases = runner.get_failed_test_cases()
    # runner.email_notice()
    # runner.dingtalk_notice()
    runner.weixin_notice()


if __name__ == '__main__':
    run()
