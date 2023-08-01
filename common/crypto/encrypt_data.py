#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: encrypt.py
@time: 2023/6/16 15:43
@desc:
"""
from common.crypto import logger
from common.crypto.encryption_rsa import Rsa
# from common.crypto.encryption_aes import DoAES
from encryption_rules import rules


@logger.log_decorator()
class EncryptData:
    """
    数据加密入口
    """

    def encrypts(self, headers_crypto, headers, request_data_crypto, request_data):
        encryption_methods = {
            "MD5": rules.md5_sign,
            "sha1": rules.sha1_sign,
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
