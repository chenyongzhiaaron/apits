# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_list.py
# Description:
# Author:       chenyongzhi
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 15:15
# -------------------------------------------------------------------------------
import logging
from common.utils.logger import MyLog

__all__ = ['slice', 'sublist']

logger = MyLog()


def slice(obj, index=None, start=None, end=None, step=1):
    """
    切片方法
    Args:
        obj:
        index: 索引
        start: 开始索引
        end: 结束索引（不含）
        step: 步长

    Returns:

    """
    logger.my_log(f'执行方法：slice({obj}, {index}, {start}, {end}, {step})', "info")
    if isinstance(obj, (str, tuple, list)):
        if index != None:
            try:
                result = obj[index]
            except IndexError:
                logger.my_log(f'列表{obj}，下标{index}，异常原因：下标越界')
                result = None
            return result
        else:
            step = step or 1
            return obj[start:end:step]
    logger.my_log("obj参数格式不正确")
    return None


def sublist(raw_list, start=None, end=None):
    """
    截取子列表
    Args:
        raw_list: 原始列表
        start: 字符串开始位置
        end: 字符串结束位置

    Returns: 截取的字符串

    """
    logger.my_log(f'执行方法：sublist({raw_list}, {start}, {end})', "info")
    try:
        start = int(start) if (isinstance(start, str) and start.isdigit()) else start
        end = int(end) if (isinstance(end, str) and end.isdigit()) else end
        return raw_list[start:end]
    except TypeError as e:
        return []
