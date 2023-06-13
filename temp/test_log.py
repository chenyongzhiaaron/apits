#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: test_log.py
@time: 2023/6/12 10:54
@desc:
"""
# 导入测试框架
import unittest

# 导入日志记录器类
from common.utils.mylogger import MyLogger


# 定义一个测试类，继承自 unittest.TestCase
class TestLogDecorator(unittest.TestCase):

    # 定义一个测试方法，以 test_ 开头
    def test_log_decorator(self):
        # 创建一个日志记录器对象
        log = MyLogger()

        # 定义一个被装饰的函数，返回两个参数的和
        @log.log_decorator(msg="Something went wrong")
        def add(a, b):
            return a + b

        # 调用被装饰的函数，传入正常的输入数据
        result = add(1, 2)
        # 断言输出结果是否符合预期
        self.assertEqual(result, 3)
        # 调用被装饰的函数，传入异常的输入数据
        with self.assertRaises(TypeError):  # 断言抛出异常
            add(1, "2")  # 传入不同类型的参数


# 如果是主模块，执行所有测试用例
if __name__ == "__main__":
    unittest.main()
