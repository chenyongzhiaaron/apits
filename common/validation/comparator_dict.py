# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         comparator_dict.py
# Description:  比较器名词释义
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2020/10/29 16:51
# -------------------------------------------------------------------------------

__all__ = ['comparator_dict']

# 比较器名词释义
comparator_dict = {
	'eq': 'eq:实际值与期望值相等',
	'lt': 'lt:实际值小于期望值',
	'lte': 'lte:实际值小于或等于期望值',
	'gt': 'gt:实际值大于期望值',
	'gte': 'gte:实际值大于或等于期望值',
	'neq': 'neq:实际值与期望值不相等',
	'str_eq': 'str_eq:字符串实际值与期望值相同',
	'length_eq': 'length_eq:实际值的长度等于期望长度',
	'length_gt': 'length_gt:实际值的长度大于期望长度',
	'length_gte': 'length_gte:实际值的长度大于或等于期望长度',
	'length_lt': 'length_lt:实际值的长度小于期望长度',
	'length_lte': 'length_lte:实际值的长度小于或等于期望长度',
	'contains': 'contains:期望值包含在实际值中',
	'contained_by': 'contained_by:实际值被包含在期望值中',
	'type_match': 'type_match:实际值的类型与期望值的类型相匹配',
	'regex_match': 'type_match:正则匹配(从字符串的起始位置匹配)',
	'regex_search': 'regex_search:正则匹配(从字符串的任意位置匹配)',
	'startswith': 'startswith:实际值是以期望值开始',
	'endswith': 'endswith:实际值是以期望值结束',
	'check': 'check: 实际复杂对象包含预期复杂对象'
}
