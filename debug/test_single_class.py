#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: test_single_class.py
@time: 2023/6/21 17:03
@desc:
"""
from functools import wraps


def single(cls):
	instance = {}
	
	@wraps(cls)
	def decortator(*args, **kwargs):
		if cls not in instance:
			instance[cls] = cls(*args, **kwargs)
		return instance[cls]
	
	return decortator


class A:
	pass


@single
class B(A):
	pass


class C(B):
	pass


if __name__ == '__main__':
	C()
