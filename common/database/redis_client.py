# -*- coding: utf-8 -*-
# @Time : 2021/5/8 10:36
# @Author : kira
# @Email : 262667641@qq.com
# @File : do_redis.py
# @Project : api-test-project
import redis


class RedisClient:
    def __init__(self):
        self.redis = redis.Redis(host='10.8.203.25', port=6379, password='test2020')

    def set_data(self, key, value, expire_time=None):
        self.redis.set(key, value)
        if expire_time is not None:
            self.redis.expire(key, expire_time)

    def get_data(self, key):
        return self.redis.get(key)

    def delete_data(self, key):
        self.redis.delete(key)

    def hash_set_field(self, key, field, value):
        self.redis.hset(key, field, value)

    def hash_get_field(self, key, field):
        return self.redis.hget(key, field)

    def hash_delete_field(self, key, field):
        self.redis.hdel(key, field)


if __name__ == '__main__':

    # r = redis.Redis(host='10.8.203.25', port=6379, password='test2020')

    # print(r.select(1))  # 切数据库1
    # print(r.dbsize())  # 看 db 大小
    #
    # # 设置键为"key1"的字符串值为"Hello, Redis!"
    # r.set('key1', 'Hello, Redis!')
    #
    # # 获取键为"key1"的字符串值
    # value = r.get('key1')
    # print(value)  # 输出: b'Hello, Redis!'
    #
    # # 向名为"list1"的列表左侧插入元素
    # r.lpush('list1', 'item1')
    # r.lpush('list1', 'item2')
    # r.lpush('list1', 'item3')
    #
    # # 获取名为"list1"的列表所有元素
    # items = r.lrange('list1', 0, -1)
    # print(items)  # 输出: [b'item3', b'item2', b'item1']
    #
    # # 设置名为"hash1"的哈希表字段和值
    # r.hset('hash1', 'field1', 'value1')
    # r.hset('hash1', 'field2', 'value2')
    #
    # # 获取名为"hash1"的哈希表字段和值
    # value1 = r.hget('hash1', 'field1')
    # value2 = r.hget('hash1', 'field2')
    # values = r.hgetall('hash1')
    # print(value1, value2)  # 输出: b'value1' b'value2
    # print(values)  # 输出：{b'field1': b'value1', b'field2': b'value2'}
    #
    # # 向名为"set1"的集合添加元素
    # r.sadd('set1', 'item1')
    # r.sadd('set1', 'item2')
    # r.sadd('set1', 'item3')
    #
    # # 获取名为"set1"的集合所有元素
    # items = r.smembers('set1')
    # print(items)  # 输出: {b'item1', b'item2', b'item3'}
    redis_client = RedisClient()

    redis_client.set_data('user1', '100', 3600)


    def get_user_info(user_id):
        cache_key = f'user1:{user_id}'
        user_info = redis_client.get_data(cache_key)
        if not user_info:
            print("--")
        print(f'{user_info}')


    get_user_info(100)
