# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_random.py
# Description:
# Author:       chenyongzhi
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 14:02
# -------------------------------------------------------------------------------
import random
import string

from common.bif_functions import logger

__all__ = ['random_choice', 'gen_random_num', 'gen_random_str']


@logger.log_decorator()
def random_choice(args):
	"""
	随机选择
	Args:
	    args:
    
	Returns:
 
	"""
	return random.choice(args)


@logger.log_decorator()
def gen_random_num(length):
	"""
	随机生成指定长度的数字
	Args:
	    length: 指定长度
    
	Returns:
 
	"""
	return random.randint(int('1' + '0' * (length - 1)), int('9' * length))


@logger.log_decorator()
def gen_random_str(length):
	"""
	生成指定长度的随机字符串
	Args:
	    length: 指定长度
    
	Returns:
 
	"""
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
