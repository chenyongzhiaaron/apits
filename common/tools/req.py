# -*- coding: utf-8 -*-

import re
import sys

import requests
import urllib3

sys.path.append("../")
sys.path.append("./common")

from common.tools.logger import MyLog


@MyLog().decorator_log("请求异常")
def req(host, url, method, headers=None, **kwargs):
    """
    发送 http 请求
    @param host: 域名
    @param url: 接口 url
    @param method: http 请求方法
    @param headers: 请求头部信息，默认为 None
    @param kwargs: 接受 requests 原生的关键字参数
    @return: 响应对象
    """
    # 关闭 https 警告信息
    urllib3.disable_warnings()

    if not url:
        raise ValueError("URL 不能为 None")
    with requests.Session() as session:

        url = f'{host}{url}' if not re.match(r"https?", url) else url
        # 利用反射动态获取requests 模块中对应的请求方法,会有少量性能开销
        func = getattr(session, method.lower())
        # 默认请求信息
        default_headers = {"Content-Type": "application/json;charset=UTF-8"}
        # 更新请求头
        if headers:
            default_headers.update(headers)
        headers = default_headers
        # 取出传入的 data 和 headers, 如果没有传入则使用默认值
        data = kwargs.pop("data", None)
        if "application/x-www-form-urlencoded" in default_headers.values():
            return func(url, headers=headers, params=data, data=data, verify=False, timeout=30, **kwargs)
        else:
            return func(url, headers=headers, params=data, json=data, verify=False, timeout=30, **kwargs)


if __name__ == '__main__':
    h = 'https://bimdc.bzlrobot.com'
    # u = r'/bsp/test/user/ugs/ibs/api/ibs-material/material/jobRequire/pages?t=1681118956000'
    hea = {"BSP_TOKEN": "fc8fc6626920b8a8c729c6e003fbfc4f"}
    # da = {"ncCode": "", "applyTimeBegin": "", "applyTimeEnd": "", "applyUserName": "", "auditStatus": "",
    #       "buildingCode": "", "code": "", "name": "", "purchaseType": "", "size": 10, "current": 1,
    #       "projectId": "104966"}
    u = r'/bsp/test/user/ugs/ibs/api/ibs-material/checkAccept/todo/count'
    da = {"t": "1681120148000", "userId": "216483504447804297", "projectId": "104966"}

    reqs = req(h, u, "get", headers=hea, data=da).json()
    print(reqs)
