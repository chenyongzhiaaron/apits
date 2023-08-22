# -*- coding: utf-8 -*-
# @Time : 2019/11/18 15:32
# @Author : kira
# @Email : 262667641@qq.com
# @File : run.py
# @Desc : 程序执行入口文件
import sys
import unittest

sys.path.append("./common")
sys.path.append("./")
sys.path.append('cases')

from config.config import Config
from common.core.testRunner import TestRunner
from common.utils.decorators import install_dependencies


@install_dependencies
def run():
    test_report = Config.TEST_REPORT
    print(Config.BASE_URL)
    print(test_report)
    print(Config.SCRIPT)

    test_case = unittest.defaultTestLoader.discover(Config.SCRIPT, pattern="test_*.py")
    runner = TestRunner(test_case, report_dir=test_report, title="接口自动化测试报告", templates=2, tester="kira",
                        desc="自动化测试")
    runner.run()
    # # get_failed_test_cases = runner.get_failed_test_cases()
    # runner.email_notice()
    runner.dingtalk_notice()
    runner.weixin_notice()


if __name__ == '__main__':
    run()
