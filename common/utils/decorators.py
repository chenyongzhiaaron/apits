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


def singleton(cls):
    """
    Args:
    cls:Decorated class
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
    """Retry on Failed Requests"""
    from common.utils.exceptions import RequestSendingError

    def request_decorator(func):
        @wraps(func)
        def wrapper(self):
            last_exception = None

            for i in range(retries):
                try:
                    func(self)
                    print(f"| 请求地址 --> {self.response.request.url}")
                    print(f"| 请求方法 --> {self.response.request.method}")
                    print(f"| 请求头 --> {self.response.request.headers}")
                    print(f"| 请求 body --> {self.response.request.body}")
                    print(f"| 接口状态--> {self.response.status_code}")
                    print(f"| 接口耗时--> {self.response.elapsed}")
                    try:
                        print(f"| 接口响应--> {self.response.json()}")
                    except ValueError:
                        print(f"| 接口响应--> {self.response.text}")
                    break
                except Exception as error:
                    last_exception = error
                    print(f"| 第{i + 1}次请求参数=【{self.request}】")
                    print(f"| 请求失败，原因: {error}")
                    time.sleep(delay)
            if last_exception:
                raise RequestSendingError(f"Failed to send request after {retries} retries.", last_exception)

        return wrapper

    return request_decorator


def list_data(datas):
    """
    :param datas: Test data
    :return:
    """

    def wrapper(func):
        setattr(func, "PARAMS", datas)
        return func

    return wrapper


def yaml_data(file_path):
    """
    :param file_path:YAML file path
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
    :param file_path: YAML file path
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


def run_count(count, interval, func, *args, **kwargs):
    """Run Count"""
    for i in range(count):
        try:
            func(*args, **kwargs)
        except Exception as e:
            # print("====用例执行失败===", e)
            # traceback.print_exc()
            if i + 1 == count:
                raise e
            else:
                print("==============开始第{}次重运行=============".format(i))
                time.sleep(interval)
        else:
            break


def rerun(count, interval=2):
    """
     Decorator for rerunning a single test case; note that if using ddt, this method should be used before ddt
    :param count: Number of retries on failure
    :param interval: Interval time between each retry, default is three seconds
    :return:
    """

    def wrapper(func):
        def decorator(*args, **kwargs):
            run_count(count, interval, func, *args, **kwargs)

        return decorator

    return wrapper


def install_dependencies(func):
    """Checking and Installing Dependencies"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        try:
            print("---------------- Checking and Installing Dependencies ----------------")
            subprocess.check_call(["pipenv", "install"])
            print("---------------- Successfully Installed All Dependencies ----------------")

        except Exception as e:
            print(f"Failed to install dependencies: {str(e)}")
            sys.exit(1)
        else:
            return func(*args, **kwargs)

    return wrapper


def send_request_decorator(func):
    """Decorator to handle the logic of sending requests."""

    def decorator(self):
        """Handles setup, request execution, and teardown logic for sending requests.

               Args:
                   self: The instance of the class.
               Returns:
                   The response from the request.
               """
        # 执行 excel 与 指定模块文件中的动态代码
        self.analysis_request()
        self.execute_dynamic_code(self.setup_script)
        self.execute_prepost_script(self.scripts_dir, self.prepost_script, "setup")
        func(self)
        self.execute_dynamic_code(self.teardown_script)
        self.execute_prepost_script(self.scripts_dir, self.prepost_script, "teardown")

    return decorator
