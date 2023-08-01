#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: cap.py
@time: 2023/7/28 16:12
@desc:
"""
import csv

import mitmproxy.http


class CaptureInfoWriteFile:
    def __init__(self):
        pass
    
    def request(self, flow: mitmproxy.http.HTTPFlow):
        flow_request = flow.request  # 获取请求对象
        self.url = flow_request.url  # 接口url
        self.host = flow_request.host  # 域名
        self.path = flow_request.path  # 接口地址
        self.method = flow_request.method  # 请求方式
        self.content = flow_request.content
        self.timestamp_start = flow_request.timestamp_start  # 请求开始时间戳
        self.timestamp_end = flow_request.timestamp_end  # 请求结束时间戳
        self.header = flow_request.headers  # 请求头
        self.text = flow_request.text  # 请求体
    
    def response(self, flow: mitmproxy.http.HTTPFlow):
        flow_response = flow.response  # 获取响应对象
        response_status_code = flow_response.status_code  # 响应状态码
        response_text = flow_response.text  # 响应体
        response_content = flow_response.content
        response_timestamp_start = flow_response.timestamp_start  # 响应开始时间
        response_timestamp_end = flow_response.timestamp_end  # 响应结束时间
        response_header = flow_response.headers  # 响应头
        
        with open(r'test15.csv', 'a+', newline='', encoding='utf8') as f:
            f_csv = csv.writer(f)
            f_csv.writerows([[self.url, self.host, self.path, self.method, self.header, self.text, response_status_code,
                              response_header, response_text]])


addons = [CaptureInfoWriteFile()]
