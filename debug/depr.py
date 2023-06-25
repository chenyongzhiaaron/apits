#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: depr.py
@time: 2023/6/19 17:51
@desc:
"""
import requests

from common.database.redis_client import RedisClient

redis_client = RedisClient()


# 第一个接口，设置依赖数据
def first_api():
	response = requests.get('https://api.example.com/first')
	data = response.json()
	redis_client.set_data('key', data['value'])


def second_api():
	# 获取依赖数据
	dependency_data = redis_client.get_data('key')
	
	response = requests.post('https://api.example.com/second', data={'data': dependency_data})
	result = response.json()
	# 处理接口响应结果


if __name__ == '__main__':
	first_api()
	second_api()
