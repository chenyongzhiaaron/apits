#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: logger_decortor.py
@time: 2023/3/15 11:26
@desc:
"""
import logging
import os

"""
* %(asctime)s   即日志记录时间，精确到毫秒@breif: 
* %(levelname)s 即此条日志级别@param[in]: 
* %(filename)s  即触发日志记录的python文件名@retval: 
* %(funcName)s  即触发日志记录的函数名
* %(lineno)s    即触发日志记录代码的行号
* %(message)s   即这项调用中的参数
"""

file_name = "../../OutPut/Log/log.log"
if not os.path.exists(file_name):
    file = open(file_name, "w")

logging.basicConfig(
    filename=file_name,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s"
)

"""
* @breif: 日志修饰器，为函数添加日志记录服务
* @param[in]: err -> 发生异常时返回的错误信息
* @retval: 加载日志服务的功能函数
"""


def logger(err):
    def log(func):
        def warp():

            return warp

    return log
