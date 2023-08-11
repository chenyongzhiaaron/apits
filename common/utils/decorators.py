#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: decorators.py
@time: 2023/3/21 17:41
@desc:
"""
import json
import subprocess
import sys
from functools import wraps

import yaml

from common.utils.exceptions import RequestSendingError


def singleton(cls):
    """
    Args:
    cls:被装饰类
    Returns:
    """
    instance = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance


def request_retry_on_exception(retries=2, delay=1.5):
    """失败请求重发"""

    def request_decorator(func):
        e = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal e
            for i in range(retries):
                try:

                    response = func(*args, **kwargs)
                    print(f"| 请求地址 --> {response.request.url}")
                    print(f"| 请求头 --> {response.request.headers}")
                    print(f"| 请求 body --> {response.request.body}")
                    print(f"| 接口状态--> {response.status_code}")
                    print(f"| 接口耗时--> {response.elapsed}")
                    print(f"| 接口响应--> {response.text}")

                except Exception as error:
                    print(f"| 第{i + 1}次发送请求的参数：{args} -- {kwargs}")
                    e = error
                    time.sleep(delay)
                else:
                    return response
            raise RequestSendingError(kwargs, e)

        return wrapper

    return request_decorator


def list_data(datas):
    """
    :param datas: 测试数据
    :return:
    """

    def wrapper(func):
        setattr(func, "PARAMS", datas)
        return func

    return wrapper


def yaml_data(file_path):
    """
    :param file_path: yaml文件路径
    :return:
    """

    def wrapper(func):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                datas = yaml.load(f, Loader=yaml.FullLoader)
        except:
            with open(file_path, "r", encoding="gbk") as f:
                datas = yaml.load(f, Loader=yaml.FullLoader)
        setattr(func, "PARAMS", datas)
        return func

    return wrapper


def json_data(file_path):
    """
    :param file_path: json文件路径
    :return:
    """

    def wrapper(func):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                datas = json.load(f)
        except:
            with open(file_path, "r", encoding="gbk") as f:
                datas = json.load(f)
        setattr(func, "PARAMS", datas)
        return func

    return wrapper


import time
import traceback


def run_count(count, interval, func, *args, **kwargs):
    """运行计数"""
    for i in range(count):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print("====用例执行失败===")
            traceback.print_exc()
            if i + 1 == count:
                raise e
            else:
                print("==============开始第{}次重运行=============".format(i))
                time.sleep(interval)
        else:
            break


def rerun(count, interval=2):
    """
    单个测试用例重运行的装饰器,注意点，如果使用了ddt,那么该方法要在用在ddt之前
    :param count: 失败重运行次数
    :param interval: 每次重运行间隔时间,默认三秒钟
    :return:
    """

    def wrapper(func):
        def decorator(*args, **kwargs):
            run_count(count, interval, func, *args, **kwargs)

        return decorator

    return wrapper


def install_dependencies(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            print("---------------- 檢測并且安装依赖文件 ----------------")
            subprocess.check_call(["pipenv", "install"])
            print("---------------- 成功安装所有依赖文件 ----------------")

        except Exception as e:
            print(f"Failed to install dependencies: {str(e)}")
            sys.exit(1)
        else:
            return func(*args, **kwargs)

    return wrapper
