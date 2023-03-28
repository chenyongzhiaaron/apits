# -*- coding: utf-8 -*-

import re
import sys

import requests
import urllib3

sys.path.append("../")
sys.path.append("./common")

from common.tools.logger import MyLog


def req(hosts, methods, url, **kwargs):
    """
    简单封装 requests 请求
    Args:
        hosts:域名IP
        methods (str): 请求方法 GET,POST,PUT,PATCH
        url (str):请求地址，http/https开头者直接使用，否则拼接后使用
    Returns:响应结果对象

    """
    # 关闭 https 警告信息
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if re.match(r"https?", url):
        url = url
    else:
        url = hosts + url
    res = None
    data = kwargs.get("data", None)
    headers = kwargs.get("headers")
    if methods.lower() == 'post':
        try:
            if "application/x-www-form-urlencoded" in headers.values():
                res = requests.post(url=url, data=data, headers=headers, verify=False,
                                    timeout=30)
            else:
                res = requests.post(url=url, json=data, headers=headers, verify=False,
                                    timeout=30)
        except Exception as e:
            MyLog().my_log(f"post 请求异常:{e}\nURL:{url}\n参数:{data}")
    elif methods.lower() == 'get':
        try:
            res = requests.get(url=url, params=data, headers=headers, verify=False, timeout=30)
        except Exception as e:
            MyLog().my_log(f"get 请求异常:{e}\nURL:{url}\n参数:{data}")
    return res


if __name__ == '__main__':
    pass
