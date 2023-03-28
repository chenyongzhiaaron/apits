# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_re.py
# Description:
# Author:       XiangjunZhao
# EMAIL:        2419352654@qq.com
# Date:         2021/1/12 15:11
# -------------------------------------------------------------------------------
import json
import logging
import re

logger = logging.getLogger(__name__)

__all__ = ['regex_extract']


def regex_extract(string, pattern, group=None):
    """
    根据正则表达式提取内容
    Args:
        string: 字符串
        pattern: 正则表达式
        group: 分组组号

    Returns:

    """
    logger.info(f'执行方法：regex_extract({string}, {pattern}, {group})')
    if not isinstance(string, str):
        string = json.dumps(string, ensure_ascii=False)
    re_obj = re.search(pattern, string)
    result = None
    if re_obj:
        result = re_obj.group(0)
        if group:
            try:
                result = re_obj.group(group)
            except IndexError:
                pass
    return result
