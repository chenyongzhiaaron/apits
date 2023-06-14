# -*- coding: utf-8 -*-

import re
import sys

import requests
import urllib3

sys.path.append("../")
sys.path.append("./common")

from common.utils.mylogger import MyLogger

# 初始化全局session
session = None

log = MyLogger()


def log_decorator(msg="请求异常"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                log.info(f"发送请求的参数： {kwargs}")
                response = func(*args, **kwargs)
                log.info(f"请求地址 --> {response.request.url}")
                log.info(f"请求头 --> {response.request.headers}")
                log.info(f"请求 body --> {response.request.body}")
                log.info(f"接口状态--> {response.status_code}")
                log.info(f"接口耗时--> {response.elapsed}")
                log.info(f"接口响应--> {response.text}")
                return response
            except Exception as e:
                log.error(f"发送请求失败")

        return wrapper

    return decorator


@log_decorator()
def http_client(host, url, method, **kwargs):
    """
    发送 http 请求
    @param host: 域名
    @param url: 接口 url
    @param method: http 请求方法
    # @param request_data_type: 请求数据类型
    # @param headers: 请求头部信息，默认为 None
    @param kwargs: 接受 requests 原生的关键字参数
    @return: 响应对象
    """
    # 关闭 https 警告信息
    urllib3.disable_warnings()
    global session
    if not session:
        session = requests.Session()
    if not url:
        raise ValueError("URL 不能为 None")
    url = f'{host}{url}' if not re.match(r"https?", url) else url
    func = getattr(session, method.lower())
    return func(url, verify=True, timeout=30, **kwargs)


if __name__ == '__main__':
    url = 'https://bimdc.bzlrobot.com/bsp/test/user/ugs/auth/loginByNotBip'
    method = 'post'
    kwargs = {
        'json': '{"account": "18127813600", "password": "WD6Y0+LJLHXuFaplzUtSCnwktA7KgXCpjCS+OVvIFGTEoz2gbqK2oOOuJUf7ao0m2YYGiGi1pQTMBnkrxIY1cztGYbVp97kvIQwZLN4UhrOAe3h1asY/NLnDwB/byl7agcGv9WI4oy6B1Z93HVHmQiAKn7QqnDgPVITu4jthNc8="}',
        'headers': '{"Content-Type": "application/json"}'}
    http_client("", url, method, **kwargs)
