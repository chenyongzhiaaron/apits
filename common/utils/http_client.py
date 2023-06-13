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


def log_decorator(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        log.info(f"请求地址 --> {response.request.url}")
        log.info(f"请求头 --> {response.request.headers}")
        log.info(f"请求 body --> {response.request.body}")
        log.info(f"接口状态--> {response.status_code}")
        log.info(f"接口耗时--> {response.elapsed}")
        log.info(f"接口响应--> {response.text}")
        return response

    return wrapper


@log.log_decorator("请求异常")
@log_decorator
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
    ...
