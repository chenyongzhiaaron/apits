#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: encrypt_data.py
@time: 2023/6/16 15:43
@desc:
"""
from common.crypto import logger
from common.crypto.encryption_rsa import Rsa
from extensions import sign


@logger.log_decorator()
def encrypt_data(headers_crypto, headers, request_data_crypto, request_data):
    encryption_methods = {
        "MD5": sign.md5_sign,
        "sha1": sign.sha1_sign,
        "rsa": lambda data: Rsa(data).rsa_encrypt()
    }

    if headers_crypto:
        encrypt_func = encryption_methods.get(headers_crypto)
        if encrypt_func:
            try:
                headers = encrypt_func(headers)
            except Exception as e:
                logger.error(f"{headers_crypto} 加密失败：{e}")

    if request_data_crypto:
        encrypt_func = encryption_methods.get(request_data_crypto)
        if encrypt_func:
            try:
                request_data = encrypt_func(request_data)
            except Exception as e:
                logger.error(f"{request_data_crypto} 加密失败：{e}")

    return headers, request_data
