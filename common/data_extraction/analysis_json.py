# -*- coding: utf-8 -*-
# @Time : 2019/11/20 9:48
# @Author : kira
# @Email : 262667641@qq.com
# @File : analysis_json.py
"""
接口返回的数据是  列表字典
新建两个函数 A 和 B，函数 A 处理字典数据，被调用后，判断传循环嵌套  格式的，通过一个 key 值，获取到被包裹了多层的目标数据
具体思路如下：递的参数，如果参数为字典，则调用自身；
如果是列表或者元组，则调用列表处理函数 B；
函数 B 处理列表，被调用后，判断传递的参数，如果参数为列表或者元组，则调用自身；
如果是字典，则调用字典处理函数 A；
"""


class AnalysisJson:
	def get_target_value(self, key, dic, tmp_list):
		"""
		:param key: 目标 key 的值
		:param dic: json 数据
		:param tmp_list: 用于储蓄获取到的数据
		:return: 返回储蓄数据的 list
		"""
		if not isinstance(dic, dict) or not isinstance(tmp_list, list):
			msg = "argv[1] not an dict or argv[-1] not an list "
			return msg
		if key in dic.keys():
			tmp_list.append(dic[key])  # 传入数据如果存在 dict 则将字典遍历一次存入到 tmp_list 中
			for value in dic.values():  # 传入数据不符合则对其value 值进行遍历
				if isinstance(value, dict):
					self.get_target_value(key, value, tmp_list)  # 传入数据的value 是字典，则直接调用自身
				elif isinstance(value, (list, tuple)):
					self.get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用 get_value
		else:
			for value in dic.values():  # 遍历传入的字典值,value 为dic的值
				if isinstance(value, dict):  # 判断 value 是否字典
					self.get_target_value(key, value, tmp_list)  # 传入数据的值是字典，则直接调用自身
				elif isinstance(value, (list, tuple)):  # 判断 value 是否元组或者 list
					self.get_value(key, value, tmp_list)  # 传入数据的value 值是列表或者元组，则调用 get_value
		return tmp_list
	
	def get_value(self, key, val, tmp_list):
		"""
	
		:param key:目标 key 的值
		:param val:
		:param tmp_list:
		:return:
		"""
		for sub_val in val:
			if isinstance(sub_val, dict):  # 判断 sub_val 的值是否是字典
				self.get_target_value(key, sub_val, tmp_list)  # 传入数据 value 值是字典 则调用get_target_value
			elif isinstance(sub_val, (list, tuple)):
				self.get_value(key, sub_val, tmp_list)  # 传入数据的 value 值是列表或者元组，则调用自身


if __name__ == '__main__':
	test_dic = {'a': '1', 'g': '2', 'c': {
		'd': [{'e': [{'f': [{'v': [{'g': '6'}, [{'g': '7'}, [{'g': 8}]]]}, 'm']}]}, 'h', {'g': [10, 12]}]}}
	test_list = []
	test = AnalysisJson()
	resp = test.get_target_value("g", test_dic, test_list)
	print(resp)
