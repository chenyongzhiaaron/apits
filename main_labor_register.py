#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: main_labor_register.py
@time: 2023/6/29 18:01
@desc:
"""
if __name__ == "__main__":
    number = int(input("请输入你需要实名制的用户数据总数: "))
    for i in range(number):
        pytest.main(["script/bgy/test_labor_register.py"])
