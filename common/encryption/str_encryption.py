#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: str_encryption.py
@time: 2023/3/14 16:28
@desc:
"""

import hashlib
import base64
import binascii
import rsa

from pyDes import des, CBC, PAD_PKCS5
# from Crypto.Cipher import AES


def bs64_data_encode(st):
    """
    base64 加密
    Args:
        st:

    Returns:

    """
    return base64.b64encode(st.encode("utf-8"))


def bs64_data_decode(st):
    """
    base64 解密
    Args:
        st:

    Returns:

    """
    return base64.b64decode(st).decode()


def md5(st: str) -> str:
    """

    Args:
        st:待加密字符串

    Returns: 返回MD5 加密后的字符串

    """
    md = hashlib.md5()  # 创建MD5对象
    md.update(st.encode(encoding="utf-8"))
    return md.hexdigest()


def sha1_secret_str(st):
    """
    使用sha1加密算法，返回str加密后的字符串
    Args:
        st:

    Returns:

    """
    sha = hashlib.sha1(st.encode("utf-8"))
    return sha.hexdigest()


def sha256_single(st):
    """
    sha256加密
    Args:
        st: 加密字符串

    Returns:加密结果转换为16进制字符串，并大写

    """
    sha_obj = hashlib.sha256()
    sha_obj.update(st.encode("utf-8"))
    return sha_obj.hexdigest().upper()


class Des:
    def __init__(self, text, key):
        self.text = text  # 原始字符串
        self.KEY = key  # 这个key是固定问开发，

    def des_encrypt(self):
        """DES 加密
        Returns:加密后字符串，16进制

        """
        secret_key = self.KEY  # 密码
        iv = secret_key  # 偏移
        # secret_key:加密密钥，CBC:加密模式，iv:偏移, padmode:填充
        des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        # 返回为字节
        secret_bytes = des_obj.encrypt(self.text.encode("utf-8"), padmode=PAD_PKCS5)
        # 返回为16进制
        return binascii.b2a_hex(secret_bytes)

    def des_decrypt(self):
        """
        DES 解密
        Returns:解密后的字符串

        """
        secret_key = self.KEY
        iv = secret_key
        des_obj = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
        decrypt_str = des_obj.decrypt(binascii.a2b_hex(self.text), padmode=PAD_PKCS5)
        return bytes.decode(decrypt_str)  # bytes.decode() 将bit转为str


def add_to_16(text: str):
    """
    使用空格补足16位数
    Args:
        text:源字符串

    Returns:补位后字符串

    """
    b_text = text.encode("utf-8")
    add = 0
    # 计算需要补的位数
    if len(b_text) % 16:
        add = 16 - len(b_text) % 16
    return b_text + b'\0' * add


# class AesEcb:
#
#     def __init__(self, text: str, key: str):
#         self.text = text
#         self.KEY = key
#
#     def encrypt_by_aes(self):
#         """
#         加密函数
#         Returns:加密后字符串，base64 编码输出
#
#         """
#         key = self.KEY.encode("utf-8")
#         text = add_to_16(self.text)  # 补位：16位
#         cryptos = AES.new(key, AES.MODE_ECB)  # 加密模式 ECB
#         cipher_text = cryptos.encrypt(text)  # 加密
#         return base64.standard_b64encode(cipher_text).decode("utf-8")  # 加密结果 base64 编码输出
#
#     def decrypt_by_aes(self):
#         """
#         解密函数
#         Returns:
#
#         """
#         key = self.KEY.encode("utf-8")
#         text = self.text.encode("utf-8")
#         text = base64.b64decode(text)  # 先用base64 解密
#         cryptos = AES.new(key, AES.MODE_ECB)
#         cipher_text = cryptos.decrypt(text)  # 解密
#         return cipher_text.decode("utf-8").strip("\0")  # 解密，去掉补位的0


# class AesCbc:
#
#     def __init__(self, key: str, iv: str):
#         self.key = key.encode("utf-8")  # 初始化密钥
#         self.iv = iv.encode("utf-8")  # 初始化偏移量
#         self.length = 16  # 初始化数据快大小
#         self.aes = AES.new(self.key, AES.MODE_CBC, self.iv)  # 初始化AES,ECB 模式的实例
#         self.unpad = lambda s: s[0:-s[-1]]  # 截断函数，去除填充的字符
#
#     def pad(self, text):
#         """
#         填充函数，使被加密数据的字节码长度是block_size的整数倍
#         """
#         count = len(text.encode('utf-8'))
#         add = self.length - (count % self.length)
#         entext = text + (chr(add) * add)
#         return entext
#
#     def encrypt(self, encr_data):  # 加密函数
#         a = self.pad(encr_data)
#         res = self.aes.encrypt(a.encode("utf-8"))
#         msg = str(base64.b64encode(res), encoding="utf8")
#         return msg
#
#     def decrypt(self, decr_data):  # 解密函数
#         res = base64.decodebytes(decr_data.encode("utf-8"))
#         msg_text = self.aes.decrypt(res)
#         decrypt_text = self.unpad(msg_text).decode('utf8')
#         return decrypt_text


class Rsa:
    def __init__(self, st: str):
        self.st = st

    # rsa加密
    def rsa_encrypt(self):
        # 生成公钥、私钥
        (pubkey, privkey) = rsa.newkeys(1024)
        print("公钥: ", pubkey)
        print("私钥: ", privkey)
        # 明文编码格式
        content = self.st.encode('utf-8')
        # 公钥加密
        crypto = rsa.encrypt(content, pubkey)
        # # 一般加密的密文会以base64编码的方式输出
        b_res = base64.b64encode(crypto).decode()
        return b_res, privkey

    # rsa解密
    def rsa_decrypt(self, pk):
        # 私钥解密
        st = base64.b64decode(self.st.encode())
        content = rsa.decrypt(st, pk)
        con = content.decode('utf-8')

        return con
