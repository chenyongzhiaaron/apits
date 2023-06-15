# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_hashlib.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 15:16
# -------------------------------------------------------------------------------
import hashlib

from common.utils.mylogger import MyLogger

__all__ = ['md5_encryption']

logger = MyLogger()


@logger.log_decorator()
def md5_encryption(raw_str, sha_str='', toupper=False):
    """
    执行md5加密
    Args:
        raw_str: 原始字符串
        sha_str: md5加密的盐值
        toupper: 是否将加密后的结果转大写

    Returns: 经md5加密后的字符串

    """
    md5_obj = hashlib.md5(sha_str.encode('utf-8'))
    md5_obj.update(str(raw_str).encode('utf-8'))
    encrypted_str = md5_obj.hexdigest().upper() if toupper else md5_obj.hexdigest()
    return encrypted_str
