# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         comparators.py
# Description:  内建比较器
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2020/2/25 16:48
# -------------------------------------------------------------------------------
import json
import re


def eq(actual_value, expect_value):
	"""
	实际值与期望值相等
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert actual_value == expect_value


def lt(actual_value, expect_value):
	"""
	实际值小于期望值
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert actual_value < expect_value


def lte(actual_value, expect_value):
	"""
	实际值小于或等于期望值
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert actual_value <= expect_value


def gt(actual_value, expect_value):
	"""
	实际值大于期望值
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert actual_value > expect_value


def gte(actual_value, expect_value):
	"""
	实际值大于或等于期望值
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert actual_value >= expect_value


def neq(actual_value, expect_value):
	"""
	实际值与期望值不相等
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert actual_value != expect_value


def str_eq(actual_value, expect_value):
	"""
	字符串实际值与期望值相同
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert str(actual_value) == str(expect_value)


def length_eq(actual_value, expect_value):
	"""
	实际值的长度等于期望长度
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(expect_value, (int,))
	assert len(actual_value) == expect_value


def length_gt(actual_value, expect_value):
	"""
	实际值的长度大于期望长度
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(expect_value, (int,))
	assert len(actual_value) > expect_value


def length_gte(actual_value, expect_value):
	"""
	实际值的长度大于或等于期望长度
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(expect_value, (int,))
	assert len(actual_value) >= expect_value


def length_lt(actual_value, expect_value):
	"""
	实际值的长度小于期望长度
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(expect_value, (int,))
	assert len(actual_value) < expect_value


def length_lte(actual_value, expect_value):
	"""
	实际值的长度小于或等于期望长度
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(expect_value, (int,))
	assert len(actual_value) <= expect_value


def contains(actual_value, expect_value):
	"""
	期望值包含在实际值中
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(actual_value, (list, tuple, dict, str, bytes))
	assert expect_value in actual_value


def contained_by(actual_value, expect_value):
	"""
	实际值被包含在期望值中
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert isinstance(expect_value, (list, tuple, dict, str, bytes))
	assert actual_value in expect_value


def type_match(actual_value, expect_value):
	"""
	实际值的类型与期望值的类型相匹配
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	
	def get_type(name):
		if isinstance(name, type):
			return name
		elif isinstance(name, (str, bytes)):
			try:
				return __builtins__[name]
			except KeyError:
				raise ValueError(name)
		else:
			raise ValueError(name)
	
	assert isinstance(actual_value, get_type(expect_value))


def regex_match(actual_value, expect_value):
	"""
	正则匹配(从字符串的起始位置匹配)
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	if not isinstance(actual_value, str):
		actual_value = json.dumps(actual_value, ensure_ascii=False)
	if not isinstance(expect_value, str):
		expect_value = json.dumps(expect_value, ensure_ascii=False)
	assert re.match(expect_value, actual_value)


def regex_search(actual_value, expect_value):
	"""
	正则匹配(从字符串的任意位置匹配)
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	if not isinstance(actual_value, str):
		actual_value = json.dumps(actual_value, ensure_ascii=False)
	if not isinstance(expect_value, str):
		expect_value = json.dumps(expect_value, ensure_ascii=False)
	assert re.search(expect_value, actual_value)


def startswith(actual_value, expect_value):
	"""
	实际值是以期望值开始
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert str(actual_value).startswith(str(expect_value))


def endswith(actual_value, expect_value):
	"""
	实际值是以期望值结束
	Args:
	    actual_value: 实际值
	    expect_value: 期望值
    
	Returns:
 
	"""
	assert str(actual_value).endswith(str(expect_value))
