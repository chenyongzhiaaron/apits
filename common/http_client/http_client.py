# -*- coding: utf-8 -*-
"""
@Time : 2021/5/8 10:36
@Author : kira
@Email : 262667641@qq.com
@File : http_client.py
"""

import json
import mimetypes
import re
import sys

import requests
import urllib3

sys.path.append("../")
sys.path.append("./common")

from common.validation.load_modules_from_folder import LoadModulesFromFolder
from common.file_handling.file_utils import FileUtils
from common.utils.decorators import request_retry_on_exception
from common.utils.exceptions import ResponseJsonConversionError


class HttpClient(LoadModulesFromFolder):
    session = requests.Session()

    def __init__(self):
        super().__init__()
        self.request = None
        self.response = None
        self.response_json = None
        self.files = []

    @request_retry_on_exception()
    def http_client(self, host, url, method, **kwargs):
        """
        发送 http 请求
        @param host: 域名
        @param url: 接口 __url
        @param method: http 请求方法
        @param kwargs: 接受 requests 原生的关键字参数
        @return: 响应对象
        """
        # 关闭 https 警告信息
        urllib3.disable_warnings()
        kwargs = self.processing_data(host, url, method, **kwargs)

        # 发送请求
        self.request = requests.Request(**kwargs)
        self.response = self.session.send(self.request.prepare(), timeout=(15, 20), verify=True)
        # 关闭文件
        [i.close() for i in self.files if len(self.files) > 0]

        self.post_response()

        return self.response

    def processing_data(self, host, url, method, **kwargs):
        kwargs["method"] = method
        if not url:
            raise ValueError("URL cannot be None")
        __url = f'{host}{url}' if not re.match(r"https?", url) else url
        kwargs["url"] = __url
        #  兼容处理 headers 参数为字符串类型的情况
        if 'headers' in kwargs and isinstance(kwargs['headers'], str):
            kwargs['headers'] = json.loads(kwargs['headers'])

        # 兼容处理 json 参数为字符串类型的情况
        if 'json' in kwargs and isinstance(kwargs['json'], str):
            kwargs['json'] = json.loads(kwargs['json'])

        kwargs['params'] = json.loads(kwargs['params']) if isinstance(kwargs['params'], str) else None

        # 处理 files 参数的情况
        if 'files' in kwargs:
            file_paths = kwargs['files']
            if isinstance(file_paths, str):
                file_paths = json.loads(file_paths)
            files = []
            file_utils = FileUtils()
            for i, file_path in enumerate(file_paths):
                file_type = mimetypes.guess_type(file_path)[0]
                file_path_completion = file_utils.get_file_path(file_path)
                f = open(file_path_completion, 'rb')
                self.files.append(f)
                files.append(
                    ('file', (f'{file_path}', f, file_type))
                )
            kwargs['files'] = files
        return kwargs

    def post_response(self):
        # 处理响应结果
        self.update_environments("responseStatusCode", self.response.status_code)
        self.update_environments("responseTime", round(self.response.elapsed.total_seconds() * 1000, 2))
        try:
            self.response_json = self.response.json()
        except Exception as e:
            ResponseJsonConversionError(self.response.text, str(e))
            self.response_json = None


if __name__ == '__main__':
    hst = 'https://kkk.ll.com'
    ul = '/bsp/test/'
    meth = 'post'
    kwarg = {
        'headers': {},
        'data': {},
        'files': ['test.txt']
    }
    pyt = HttpClient()
    pyt.http_client(hst, ul, meth, **kwarg)
