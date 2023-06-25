#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/29 8:46
# @Author  : kira

import re


class UnifiedSocialCreditIdentifier(object):
	'''
	统一社会信用代码 + 组织结构代码校验
	'''
	
	def __init__(self):
		'''
		Constructor
		'''
		# 统一社会信用代码中不使用I,O,S,V,Z
		# ''.join([str(i) for i in range(10)])
		# import string
		# string.ascii_uppercase  # ascii_lowercase |  ascii_letters
		# dict([i for i in zip(list(self.string), range(len(self.string)))])
		# dict(enumerate(self.string))
		# list(d.keys())[list(d.values()).index(10)]
		# chr(97)  --> 'a'
		self.string1 = '0123456789ABCDEFGHJKLMNPQRTUWXY'
		self.SOCIAL_CREDIT_CHECK_CODE_DICT = {
			'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
			'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17,
			'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24,
			'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30}
		# 第i位置上的加权因子
		self.social_credit_weighting_factor = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
		
		# GB11714-1997全国组织机构代码编制规则中代码字符集
		self.string2 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
		self.ORGANIZATION_CHECK_CODE_DICT = {
			'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
			'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
			'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26,
			'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}
		# 第i位置上的加权因子
		self.organization_weighting_factor = [3, 7, 9, 10, 5, 8, 4, 2]
	
	def check_social_credit_code(self, code):
		'''
		统一社会信用代码校验
		国家标准GB32100—2015：18位统一社会信用代码从2015年10月1日正式实行，
		标准规定统一社会信用代码用18位阿拉伯数字或大写英文字母（不使用I、O、Z、S、V）表示，
		分别是1位登记管理部门代码、1位机构类别代码、6位登记管理机关行政区划码、9位主体标识码（组织机构代码）、1位校验码
	
	
		税号 = 6位行政区划码 + 9位组织机构代码
		计算校验码公式:
		    C18 = 31-mod(sum(Ci*Wi)，31)
		其中Ci为组织机构代码的第i位字符,Wi为第i位置的加权因子,C18为校验码
		c18=30, Y; c18=31, 0
		'''
		# 主要是避免缺失值乱入
		# if type(code) != str: return False
		# 转大写
		code = code.upper()
		# 1. 长度限制
		if len(code) != 18:
			print('{} -- 统一社会信用代码长度不等18！'.format(code))
			return False
		# 2. 不含IOSVZ -- 组成限制, 非字典表给个非常大的数, 不超过15000
		'''lst = list('IOSVZ')
		for s in lst:
		    if s in code:
			print('包含非组成字符：%s' % (s))
			return False'''
		
		# 2. 组成限制
		# 登记管理部门：1=机构编制; 5=民政; 9=工商; Y=其他
		# 机构类别代码:
		'''
		机构编制=1：1=机关 | 2=事业单位 | 3=中央编办直接管理机构编制的群众团体 | 9=其他
		民政=5：1=社会团体 | 2=民办非企业单位 | 3=基金会 | 9=其他
		工商=9：1=企业 | 2=个体工商户 | 3=农民专业合作社
		其他=Y：1=其他
		'''
		reg = r'^(11|12|13|19|51|52|53|59|91|92|93|Y1)\d{6}\w{9}\w$'
		if not re.match(reg, code):
			print('{} -- 组成错误！'.format(code))
			return False
		
		# 3. 校验码验证
		# 本体代码
		ontology_code = code[:17]
		# 校验码
		check_code = code[17]
		# 计算校验码
		tmp_check_code = self.gen_check_code(self.social_credit_weighting_factor,
		                                     ontology_code,
		                                     31,
		                                     self.SOCIAL_CREDIT_CHECK_CODE_DICT)
		if tmp_check_code == -1:
			print('{} -- 包含非组成字符！'.format(code))
			return False
		
		tmp_check_code = (0 if tmp_check_code == 31 else tmp_check_code)
		if self.string1[tmp_check_code] == check_code:
			# print('{} -- 统一社会信用代码校验正确！'.format(code))
			return True
		else:
			print('{} -- 统一社会信用代码校验错误！'.format(code))
			return False
	
	def check_organization_code(self, code):
		'''
		组织机构代码校验
		该规则按照GB 11714编制：统一社会信用代码的第9~17位为主体标识码(组织机构代码)，共九位字符
		计算校验码公式:
		    C9 = 11-mod(sum(Ci*Wi)，11)
		其中Ci为组织机构代码的第i位字符,Wi为第i位置的加权因子,C9为校验码
		C9=10, X; C9=11, 0
		@param  code: 统一社会信用代码 / 组织机构代码
		'''
		# 主要是避免缺失值乱入
		# if type(code) != str: return False
		# 1. 长度限制
		if len(code) != 9:
			print('{} -- 组织机构代码长度不等9！'.format(code))
			return False
		
		# 2. 组成限制
		reg = r'^\w{9}$'
		if not re.match(reg, code):
			print('{} -- 组成错误！'.format(code))
			return False
		
		# 3. 校验码验证
		# 本体代码
		ontology_code = code[:8]
		# 校验码
		check_code = code[8]
		# 计算校验码
		tmp_check_code = self.gen_check_code(self.organization_weighting_factor,
		                                     ontology_code,
		                                     11,
		                                     self.ORGANIZATION_CHECK_CODE_DICT)
		if tmp_check_code == -1:
			print('{} -- 包含非组成字符！'.format(code))
			return False
		
		tmp_check_code = (0 if tmp_check_code == 11
		                  else (33 if tmp_check_code == 10 else tmp_check_code))
		if self.string2[tmp_check_code] == check_code:
			# print('{} -- 组织机构代码校验正确！'.format(code))
			return True
		else:
			print('{} -- 组织机构代码校验错误！'.format(code))
			return False
	
	def check_code(self, code, code_type='sc'):
		'''Series类型
		@code_type {org, sc}'''
		# try:
		if type(code) != str: return False
		if code_type == 'sc':
			return self.check_social_credit_code(code)
		elif code_type == 'org':
			return self.check_organization_code(code)
		else:
			if len(code) == 18:
				return self.check_social_credit_code(code)
			else:
				return self.check_organization_code(code) if len(code) == 9 else False
		# except Exception as err:
		#    print(err)
		#    print('code:', code)
	
	def gen_check_code(self, weighting_factor, ontology_code, modulus, check_code_dict):
		'''
		@param weighting_factor: 加权因子
		@param ontology_code:本体代码
		@param modulus:  模数(求余用)
		@param check_code_dict: 字符字典
		'''
		total = 0
		for i in range(len(ontology_code)):
			if ontology_code[i].isdigit():
				# print(ontology_code[i], weighting_factor[i])
				total += int(ontology_code[i]) * weighting_factor[i]
			else:
				num = check_code_dict.get(ontology_code[i], -1)
				if num < 0: return -1
				total += num * weighting_factor[i]
		diff = modulus - total % modulus
		# print(diff)
		return diff


if __name__ == '__main__':
	# 统一社会信用代码及组织机构代码校验
	u = UnifiedSocialCreditIdentifier()
	# print(u.check_social_credit_code(code='91330382575324831A'))
	# print(u.check_social_credit_code(code='91330382575324831A'))
	print(u.check_organization_code(code='575324831'))
	print(u.check_organization_code(code='575324831'))
