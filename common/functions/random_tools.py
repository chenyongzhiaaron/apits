# -*- coding: utf-8 -*-
import datetime
import math
import random
import time
from faker import Faker

__all__ = ['random_phone', 'random_gps', "random_string", "random_ssn"]

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


def next_time():
    """

    Returns:

    """
    c_time = time.time()  # 获取当前时间，秒值输出
    yesterday_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c_time - 86400))
    # 获取当前日期 带时分秒
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(c_time))
    # 獲取當前日期时间 0时0分开始
    c_date_start = time.strftime("%Y-%m-%d", time.localtime(c_time)) + ' 00:00:00'
    c_date_end = time.strftime("%Y-%m-%d", time.localtime(c_time)) + ' 23:59:59'
    # 获取昨天日期
    y_date = time.strftime("%Y-%m-%d", time.localtime(c_time - 86400))
    # 获取当前日期
    c_date = time.strftime("%Y-%m-%d", time.localtime(c_time))
    # 获取明天日期
    n_date = time.strftime("%Y-%m-%d", time.localtime(c_time + 86400))
    # 获取明日日期
    n_date_start = time.strftime("%Y-%m-%d", time.localtime(c_time + 86400)) + ' 00:00:00'
    n_date_end = time.strftime("%Y-%m-%d", time.localtime(c_time + 86400)) + ' 23:59:59'
    # 獲取過去日期
    p_time_start = time.strftime("%Y-%m-%d", time.localtime(c_time - 86400)) + ' 00:00:00'
    p_time_end = time.strftime("%Y-%m-%d", time.localtime(c_time - 86400)) + ' 23:59:59'
    # 獲取将来60天内的任意日期，不包含今天
    random_data = time.strftime(
        "%Y-%m-%d", time.localtime(c_time + random.randint(86400, 5184000)))
    # 获取当前时间戳
    timestamp = int(round(time.time() * 1000))
    res = {
        "{{random_data}": random_data,
        "{{n_date_start}}": n_date_start,
        "{{n_date_end}}": n_date_end,
        "{{p_time_start}}": p_time_start,
        "{{p_time_end}}": p_time_end,
        "{{c_date_start}}": c_date_start,
        "{{c_date_end}}": c_date_end,
        "{{timestamp}}": timestamp,
        "{{current_time}}": current_time,
        "{{yesterday_time}}": yesterday_time,
        "{{c_date}}": c_date,
        "{{n_date}}": n_date,
        "{{y_date}}": y_date
    }
    return res


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
