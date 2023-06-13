# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_str.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 15:12
# -------------------------------------------------------------------------------
from common.utils.logger import MyLog

__all__ = ['substr', 'str_join']

logger = MyLog()


def substr(raw_str, start=None, end=None):
    """
    截取字符串
    Args:
        raw_str: 原始字符串
        start: 字符串开始位置
        end: 字符串结束位置

    Returns: 截取的字符串

    """
    logger.my_log(f'执行方法：substr({raw_str}, {start}, {end})', "info")
    try:
        start = int(start) if (isinstance(start, str) and start.isdigit()) else start
        end = int(end) if (isinstance(end, str) and end.isdigit()) else end
        return raw_str[start:end]
    except TypeError as e:
        return ''


def str_join(obj, connector=","):
    """
    连接任意数量的字符
    Args:
        obj: 被连接对象，类型：list、tuple
        connector: 连接符

    Returns:

    """
    logger.my_log(f'执行方法：str_join({obj}, {connector})', "info")
    if not isinstance(connector, str):
        connector = str(connector)
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, (list, tuple)):
        temp_obj = []
        for item in obj:
            if not isinstance(item, str):
                item = str(item)
            temp_obj.append(item)
        return connector.join(temp_obj)
