#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: xh.py
@time: 2023/5/5 10:09
@desc:
"""
for i in range(1, 6):
    for j in range(1, 9):
        if i == 3:
            print("不⾛3层.......")
            continue  # 跳过本次循环，继续下次循环
        if i == 4 and j == 4:  # 遇到404
            print("遇到⻤屋404了,不再继续了")
            break  # 结束当前循环， 注意只会结束第2层这个⼩循环。
        print(f"{i}层-{i}0{j}室")
