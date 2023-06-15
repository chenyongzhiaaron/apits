import re

import requests
import urllib3

from common.http_client.request_hooks import Hooks

hooks = Hooks()


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

    session = requests.Session()
    if not url:
        raise ValueError("URL 不能为 None")
    url = f'{host}{url}' if not re.match(r"https?", url) else url

    # 执行 before_request 钩子函数
    request = requests.Request(method, url, **kwargs)
    request = hooks.run_before_request_funcs(request)

    # 发送请求
    prepared_request = session.prepare_request(request)
    response = session.send(prepared_request)

    # 执行 after_request 钩子函数
    response = hooks.run_after_request_funcs(response)

    return response


if __name__ == '__main__':
    url = "https://ibs-test.bzlrobot.com/api/ibs-auth/ibs_platform/login?t=1686740475000"
    payload = {
        "grantType": "password",
        "account": "luoshunwen005",
        "password": "TTdNRuVHxmOI7P8G2yjrfRBaMyQzmy8XGzS1rvbV8X/WqQuJpTAVgTqTAkIswJ0xbGpA2rvoVRnsW3Dg+vmtiJrm/hNUmd7nRV42tMltWDzFAgCC4KOFBC1b+mRkACby+nuiS+N7J6xEAieXJXh6Ml5jWy9qbt2rziteB8npxsMsOygiuRpUmoSkHz8wshQGtqOAr9uQRhglNLJdLWzZtas6TQvypeOMOGSatA2arJ7ipGE3oW+AiATyDu22Eh+PBO+eR7wLWOyO2XxeWhK+5EGiiIVmKRyaMY3JedVHSjpnWmnZ1Vj9pZjUaenJQfCgSS5CBnxLX/AoxB5TvJmMEA==",
        "isBip": False
    }
    headers = {
        'Content-Type': 'application/json'
    }
    kg = {'json': payload, "headers": headers}
    res = req("", url, 'post', **kg)
    # print(res.before_request_funcs)
    # print(res.after_request_funcs)
    print(res, res.json())
