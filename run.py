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

from common.config import Config
from unittestreport import TestRunner
from common.utils.WxworkSms import WxWorkSms


def run():
	test_report = Config.test_report
	test_case = unittest.defaultTestLoader.discover(Config.script, pattern="test_*.py")
	runner = TestRunner(test_case, report_dir=test_report, title="接口自动化测试报告", templates=2, tester="kira",
	                    desc="自动化测试")
	runner.run()
	WxWorkSms('8b1647d4-dc32-447c-b524-548acf18a938').send_main(test_report, 1, 2, 3, 4, 5, 6, 7, 8, 9)


if __name__ == '__main__':
	run()
