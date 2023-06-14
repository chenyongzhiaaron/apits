import re

import requests
import urllib3

from common.utils.hooks import Hooks


def req(host, url, method, **kwargs):
    """
    发送 http 请求
    @param host: 域名
    @param url: 接口 url
    @param method: http 请求方法
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

    # 执行 before_request 钩子函数
    request = requests.Request(method, url, **kwargs)
    request = Hooks.run_before_request_funcs(request)

    # 发送请求
    prepared_request = session.prepare_request(request)
    response = session.send(prepared_request)

    # 执行 after_request 钩子函数
    response = Hooks.run_after_request_funcs(response)

    return response
