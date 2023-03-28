# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_datetime.py
# Description:
# Author:       XiangjunZhao
# EMAIL:        2419352654@qq.com
# Date:         2021/1/12 14:03
# -------------------------------------------------------------------------------
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

__all__ = ['get_current_date', 'get_current_time', 'get_delta_time']


def get_current_date(fmt="%Y-%m-%d"):
    """
    获取当前日期，默认格式为：%Y-%m-%d
    Args:
        fmt: 日期格式

    Returns:

    """
    logger.info(f'执行方法：get_current_date({fmt})')
    return datetime.now().strftime(fmt)


def get_current_time(fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间：默认格式为：%Y-%m-%d %H:%M:%S
    Args:
        fmt: 时间格式

    Returns:

    """
    logger.info(f'执行方法：get_current_time({fmt})')
    return datetime.now().strftime(fmt)


def get_delta_time(days=0, hours=0, minutes=0, seconds=0, fmt="%Y-%m-%d %H:%M:%S"):
    """
    获取当前时间指定间隔后的时间
    Args:
        days:距离当前时间多少天
        hours:距离当前时间多少时
        minutes:距离当前时间多少分
        seconds: 距离当前时间多少秒
        fmt: 时间格式

    Returns:

    """
    logger.info(f'执行方法：get_delta_time({days}, {hours}, {minutes}, {seconds}, {fmt})')
    return (datetime.now() + timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)).strftime(fmt=fmt)
