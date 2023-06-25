# !/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: rt.py
@time: 2023/6/19 17:15
@desc:
"""

import concurrent.futures

import requests

from common.database.redis_client import RedisClient

# 创建 Redis 客户端
redis_client = RedisClient()


def get_user_info(user_id):
	cache_key = f'user:{user_id}'
	user_info = redis_client.get_data(cache_key)
	if not user_info:
		# 调用接口获取用户信息
		response = requests.get(f'http://127.0.0.1:5000/?user_id={user_id}')
		if response.status_code == 200:
			user_info = response.text
			print(user_info)
			redis_client.set_data(cache_key, user_info, expire_time=3600)
		else:
			print(f"Failed to retrieve user info for user_id: {user_id}. Status code: {response.status_code}")
	
	return user_info


# 并发测试函数
def run_concurrent_test(user_ids):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		# 提交任务到线程池
		future_to_user_id = {executor.submit(get_user_info, user_id): user_id for user_id in user_ids}
		
		# 处理返回结果
		for future in concurrent.futures.as_completed(future_to_user_id):
			user_id = future_to_user_id[future]
			try:
				user_info = future.result()
				print(f"user_id: {user_id}; user_info: {user_info}")
			except Exception as e:
				print(f"Error occurred for user_id: {user_id}, Error: {str(e)}")


if __name__ == '__main__':
	u_ids = [i for i in range(10, 99)]
	run_concurrent_test(u_ids)
	# u_ids = [i for i in range(1000, 99999)]
	# for i in u_ids:
	#     response = requests.get(f'http://127.0.0.1:5000/?user_id={i}')
	#     print(response.text)
