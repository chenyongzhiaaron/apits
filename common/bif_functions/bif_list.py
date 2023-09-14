# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_list.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 15:15
# -------------------------------------------------------------------------------
from common.bif_functions import logger

__all__ = ['list_slice', 'sublist']


@logger.catch
def list_slice(obj, index=None, start=None, end=None, step=1):
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
    if isinstance(obj, (str, tuple, list)):
        if index is not None:
            try:
                return obj[index]
            except IndexError:
                return
        else:
            return obj[start:end:step]
    return None


@logger.catch
def sublist(raw_list, start=None, end=None):
    """
    截取子列表
    Args:
        raw_list: 原始列表
        start: 字符串开始位置
        end: 字符串结束位置

    Returns: 截取的字符串或子列表

    """
    if isinstance(raw_list, (str, list)) and isinstance(start, (int, str)) and isinstance(end, (int, str)):
        try:
            start = int(start) if isinstance(start, str) and start.isdigit() else start
            end = int(end) if isinstance(end, str) and end.isdigit() else end
            if isinstance(raw_list, str):
                return list(raw_list[start:end])
            else:
                return raw_list[start:end]
        except TypeError:
            pass

    return []


if __name__ == '__main__':
    # lst = [1, 2, 3, 4, 5]
    # print(list_slice(lst, index=2))  #  3
    # print(list_slice(lst, start=1, end=4))  #  [2, 3, 4]
    # print(list_slice(lst, start=1, end=4, step=2))  #  [2, 4]
    # print(list_slice(123))  #  None
    raw_list = ['a', 'b', 'c', 'd', 'e']
    print(sublist(raw_list, start=1, end=4))  # ['b', 'c', 'd']
    print(sublist(raw_list, start='1', end='4'))  # ['b', 'c', 'd']
    print(sublist(raw_list, start='x', end='4'))  # []
    print(sublist(raw_list, start=1, end=10))  # ['b', 'c', 'd', 'e']
    print(sublist('abcdef', start=1, end=4))  # ['b', 'c', 'd']
    print(sublist(123, start=1, end=4))  # []
