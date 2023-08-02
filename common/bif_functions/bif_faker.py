# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_time.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 14:03
# -------------------------------------------------------------------------------
import datetime

from faker import Faker

__all__ = [
    'fk', 'random_phone',
    "random_string", "random_ssn",
    "random_email", "random_id_card",
    "random_int", "random_male_name",
    "random_female_name", "random_current_time"
]

f = Faker(locale='Zh-CN')


def fk():
    """
    :return:faker 对象
    """
    return f


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


def random_phone() -> int:
    """
    :return: 随机生成手机号码
    """
    return f.phone_number()


def random_id_card() -> int:
    """
 
    :return: 随机生成身份证号码
    """

    return f.ssn()


def random_female_name() -> str:
    """
 
    :return: 女生姓名
    """
    return f.name_male()


def random_male_name() -> str:
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
