# -*- coding: utf-8 -*-
import datetime
import math
import random

from faker import Faker

__all__ = [
    'random_phone', 'random_gps',
    "random_string", "random_ssn",
    "random_email", "random_id_card",
    "random_int", "random_male_name",
    "random_female_name", "random_current_time"
]

f = Faker(locale='Zh-CN')


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


def random_string():
    """
    :return:随机生成字符串,20位
    """
    return f.pystr()


def random_ssn():
    """
    :return:随机生成省份中
    """
    return f.ssn()


def random_phone(self) -> int:
    """
    :return: 随机生成手机号码
    """
    return f.phone_number()


def random_id_card(self) -> int:
    """

    :return: 随机生成身份证号码
    """

    return f.ssn()


def random_female_name(self) -> str:
    """

    :return: 女生姓名
    """
    return f.name_male()


def random_male_name(self) -> str:
    """

    :return: 男生姓名
    """
    return f.name_female()


def random_email() -> str:
    """

    :return: 生成邮箱
    """
    return f.email()


def random_current_time() -> datetime.datetime:
    """
    计算当前时间
    :return:
    """

    return datetime.datetime.now()


def random_int():
    """随机生成 0 - 9999 的数字"""
    return f.random_int()


if __name__ == '__main__':
    print(random_current_time())
