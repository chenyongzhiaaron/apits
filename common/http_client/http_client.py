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
    def http_client(self):
        """
        发送 http 请求
        """
        # 关闭 https 警告信息
        urllib3.disable_warnings()
        # 发送请求
        prepared_request = requests.Request(**self.request).prepare()
        self.response = self.session.send(prepared_request, timeout=(15, 20), verify=True)
        self.post_response()

    def processing_data(self, host, url, method, **kwargs):
        """
        处理请求参数
        :param host: 主机地址
        :param url: 资源路径
        :param method: 请求方法
        :param kwargs: 额外的请求参数，支持如headers、json、params、files等关键字参数。
        :return:
        """
        kwargs["method"] = method.lower()
        if not url:
            raise ValueError("URL cannot be None")
        __url = f'{host}{url}' if not re.match(r"https?", url) else url
        kwargs["url"] = __url
        #  兼容处理 headers,json 参数为字符串类型的情况
        for key in ['headers', 'json']:
            if key in kwargs and isinstance(kwargs[key], str):
                kwargs[key] = json.loads(kwargs[key])
        kwargs['params'] = json.loads(kwargs['params']) if isinstance(kwargs['params'], str) and kwargs[
            'params'] else kwargs.get('params')

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

        self.request = kwargs

    def post_response(self):
        # 处理响应结果
        [i.close() for i in self.files if len(self.files) > 0]  # 关闭文件
        self.files.clear()  # 清空文件列表
        self.update_environments("response_status_code", self.response.status_code)
        self.update_environments("response_time", round(self.response.elapsed.total_seconds() * 1000, 2))
        self.update_environments("response", self.response.text)
        try:
            self.response_json = self.response.json()
        except Exception as e:
            ResponseJsonConversionError(self.response.text, str(e))
            self.response_json = None


if __name__ == '__main__':
    hst = 'http://localhost:3000'
    ul = '/get'
    meth = 'get'
    kwarg = {
        'headers': {},
        'data': {},
        "params": "",
        # 'files': ['test.txt']
    }
    pyt = HttpClient()
    pyt.http_client(hst, ul, meth, **kwarg)
