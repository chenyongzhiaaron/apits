# -*- coding: utf-8 -*-
# @Time : 2021/5/8 10:36
# @Author : kira
# @Email : 262667641@qq.com
# @File : do_redis.py
# @Project : api-test-project

from redis import Redis, ConnectionPool


class DoRedis:
    def __init__(self):
        connection = ConnectionPool(host="159.75.107.124", db=1, port=31003, decode_responses=True)
        self.r = Redis(connection_pool=connection)

    def do_redis(self):
        r = self.r
        return r
        # res = r.get("dis:szpszx")
        # return res


if __name__ == '__main__':
    test = DoRedis().do_redis()
    print(test.mget("dis:szpszx","dis:gzpszx"))
