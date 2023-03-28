# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_random.py
# Description:
# Author:       XiangjunZhao
# EMAIL:        2419352654@qq.com
# Date:         2021/1/12 14:02
# -------------------------------------------------------------------------------
import logging
import random
import string

logger = logging.getLogger(__name__)

__all__ = ['random_choice', 'gen_random_num', 'gen_random_str']


def random_choice(args):
    """
    随机选择
    Args:
        args:

    Returns:

    """
    logger.info(f'执行方法：random_choice({args})')
    return random.choice(args)


def gen_random_num(length):
    """
    随机生成指定长度的数字
    Args:
        length: 指定长度

    Returns:

    """
    logger.info(f'执行方法：gen_random_num({length})')
    return random.randint(int('1' + '0' * (length - 1)), int('9' * length))


def gen_random_str(length):
    """
    生成指定长度的随机字符串
    Args:
        length: 指定长度

    Returns:

    """
    logger.info(f'执行方法：gen_random_str({length})')
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
