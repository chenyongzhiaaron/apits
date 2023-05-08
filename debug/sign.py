#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: sign.py
@time: 2023/5/8 17:03
@desc:
"""
import sys
import json
import hashlib
import random


def do_sign(data):  # 签名
    """

    Args:
        data:请求body 参数

    Returns:

    """
    key = "prod_secret123@muc" + json.dumps(data) + str(random.random())
    m = hashlib.md5()
    m.update(key.encode('utf-8'))
    sign_ = m.hexdigest()
    return sign_


if __name__ == '__main__':
    body = sys.argv[1]  # 命令行传过来的参数
    sign = do_sign(body)
    print(sign)
