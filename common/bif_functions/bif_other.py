# coding: utf-8

import math
# -------------------------------------------------------------------------------
# Name:         bif_random.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 14:02
# -------------------------------------------------------------------------------
import random
import string

from common.bif_functions import logger

__all__ = ['random_choice', 'gen_random_num', 'gen_random_str', 'random_gps']


@logger.log_decorator()
def random_choice(args):
    """
    随机选择
    Args:
        args:

    Returns:

    """
    return random.choice(args)


@logger.log_decorator()
def gen_random_num(length):
    """
    随机生成指定长度的数字
    Args:
        length: 指定长度

    Returns:

    """
    return random.randint(int('1' + '0' * (length - 1)), int('9' * length))


@logger.log_decorator()
def gen_random_str(length):
    """
    生成指定长度的随机字符串
    Args:
        length: 指定长度

    Returns:

    """
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def random_gps(base_log=None, base_lat=None, radius=None):
    """

    Args:
        base_log:
        base_lat:
        radius:

    Returns:

    """
    radius_in_degrees = radius / 111300
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))
    w = radius_in_degrees * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)
    longitude = y + base_log
    latitude = x + base_lat
    # 这里是想保留6位小数点
    loga = '%.6f' % longitude
    lat = '%.6f' % latitude
    return loga, lat
