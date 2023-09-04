#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: encrypt_data.py
@time: 2023/6/16 15:43
@desc:
"""
import json

import encryption_rules
from common.utils.exceptions import EncryptionError
from common.validation.loaders import Loaders


class EncryptData(Loaders):
    """
    数据加密入口
    """

    def __init__(self):
        super().__init__()

    def encrypts(self, headers_crypto, headers, request_data_crypto, request_data):
        encryption_methods = self.load_built_in_functions(encryption_rules)
        # 请求头加密
        encrypt_func = encryption_methods.get(headers_crypto)
        # 请求头有值的时候才加密
        if encrypt_func is not None and headers:
            try:
                headers = headers if isinstance(headers, dict) else json.loads(headers)
                headers = encrypt_func(headers)
            except Exception as e:
                EncryptionError(headers_crypto, e)
        # 请求体加密
        encrypt_func = encryption_methods.get(request_data_crypto)
        # 请求参数有值的时候才加密
        if encrypt_func and request_data:
            try:
                print("request_data", request_data)
                request_data = request_data if isinstance(request_data, dict) else json.loads(request_data)
                request_data = encrypt_func(request_data)
            except Exception as e:
                EncryptionError(request_data_crypto, e)

        return headers, request_data


if __name__ == '__main__':
    enc = EncryptData()
    header = {'Content-Type': 'application/json;charset=utf-8', 'token': 'QpwL5tke4Pnpja7X4'}
    res = enc.encrypts("md5_sign", header, None, None)
    print(res)
