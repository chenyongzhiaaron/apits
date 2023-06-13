# -*- coding: utf-8 -*-

import re
import sys

import requests
import urllib3

sys.path.append("../")
sys.path.append("./common")

from common.utils.logger import MyLog

# 初始化全局session
session = None


@MyLog().decorator_log("请求异常")
def req(host, url, method, **kwargs):
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
