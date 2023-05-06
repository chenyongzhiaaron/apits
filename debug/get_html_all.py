#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: get_html_all.py
@time: 2023/5/5 16:31
@desc:
"""
import requests
from requests_html import HTMLSession


def open_url(url):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    session = HTMLSession()
    resp = session.get(url, headers=headers)
    resp.html.render(timeout=20)
    return resp.html.html


def save_markdown_file(file_name, content):
    """
    保存Markdown文件
    :param file_name: 文件名
    :param content: 文件内容
    """
    with open(file_name + ".md", "w", encoding="utf-8") as file:
        file.write(content)


def get_detail():
    host = 'https://doc.itprojects.cn/0001.zhishi/python.0001.python3kuaisurumen/01.02.di1gepythonchengxu.md'
    headers = {'user-agent': 'PostmanRuntime/7.29.2'}
    resp = requests.get(host, headers=headers)
    resp.encoding = resp.apparent_encoding

    return resp.text


if __name__ == '__main__':
    # url = 'https://doc.itprojects.cn/0001.zhishi/python.0001.python3kuaisurumen/index.html#/README'
    # ret = open_url(url)
    # print(ret)
    res = get_detail()
    print(res)
