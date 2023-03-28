#!/usr/bin/env python
# encoding: utf-8
'''
@author: kira
@contact: 262667641@qq.com
@file: do_AES.py
@time: 2022/2/17 15:19
@desc:
'''

import base64
import sys

from Crypto.Cipher import AES
import binascii


def add_to_16(text):
    while len(text) % 16 != 0:
        text += '\0'
    return text


def encrypt(data, password):
    if isinstance(password, str):
        password = password.encode('utf8')

    bs = AES.block_size
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    cipher = AES.new(password, AES.MODE_ECB)
    data = cipher.encrypt(pad(data).encode('utf8'))
    encrypt_data = binascii.b2a_hex(data)  # 输出hex
    # encrypt_data = base64.b64encode(data)         # 取消注释，输出Base64格式
    return encrypt_data.decode('utf8')


def decrypt(decrData, password):
    if isinstance(password, str):
        password = password.encode('utf8')

    cipher = AES.new(password, AES.MODE_ECB)
    plain_text = cipher.decrypt(binascii.a2b_hex(decrData))
    return plain_text.decode('utf8').rstrip('\0')


if __name__ == '__main__':
    # data = sys.argv[1]  # 待加密数据
    data = '4534'  # 待加密数据
    password = '2l4LoWczlWxlMZJAAp5N0g6EygZZd9A6'  # 16,24,32位长的密码（密钥）
    password = add_to_16(password)
    encrypt_data = encrypt(data, password)
    # print('加密前数据：{}\n======================='.format(data))
    # print('加密后的数据:', encrypt_data)
    print(encrypt_data)

    # decrypt_data = decrypt(encrypt_data, password)
    # print('解密后的数据：{}'.format(decrypt_data))
