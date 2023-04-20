#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: ddddt.py
@time: 2023/4/19 12:02
@desc:
"""
import unittest
from ddt import ddt, data


@ddt
class MyTestCase(unittest.TestCase):

    @data({"1": 1, "2": 2, "3": 3})
    def test_addition(self, item):
        print("test-->", item)
        self.item = item

        # self.assertEqual(item + 1, item)

    def setUp(self):
        # 访问 item 参数
        print("setup item:", self.item)

    def tearDown(self):
        # 访问 item 参数
        print("teardown item:", self.item)


if __name__ == '__main__':
    unittest.main()
