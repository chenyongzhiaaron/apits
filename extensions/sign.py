#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: do_sign.py
@time: 2023/3/14 16:21
@desc:
"""
import hashlib
import json
import time

from natsort import natsorted

__all__ = ["md5_sign", "sha1_sign"]

from common.crypto.encryption_str import sha1_secret_str, md5


def md5_sign(data: dict):
    """
    数据加签
    Args:
        **data:需要加钱的数据

    Returns:

    """
    sorted_list = []
    for key, value in data.items():
        try:
            sorted_params = str(key) + str(value)
            sorted_list.append(sorted_params)
        except Exception:
            raise
    sort = natsorted(sorted_list)  # 列表自然排序
    argument = "加签所需要的密钥"
    keystore = argument + ("".join(sort))  # 生成加带密钥的新字符串
    sign_value = md5(keystore)
    return {**data, **{"sign": sign_value}}


def sha1_sign(post_data: dict):
    timestamp = int(round(time.time() * 1000))  # 毫秒级时间戳
    argument = {"secretKey": "", "timestamp": timestamp}  # 加密加盐参数
    res = {**post_data, **argument}
    sorted_list = []
    for key, value in res.items():
        try:
            value = json.dumps(value, ensure_ascii=False) if isinstance(value, list) or isinstance(value,
                                                                                                   dict) else str(value)
            sorted_params = str(key) + "=" + value
            sorted_list.append(sorted_params)
        except Exception as e:
            raise e
    sort = natsorted(sorted_list)  # 列表自然排序 返回[(key,value),(key,value)]
    splicing_str = "&".join(sort)  # 排序结果 key=value&key=value 拼接
    encrypted_str = sha1_secret_str(splicing_str)  # sha1加密
    sign = {"signature": encrypted_str}
    return {**res, **sign}  # request 中使用json入参，则传dict
