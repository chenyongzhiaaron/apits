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
        self.records = []

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.url = flow.request.url  # 接口url
        self.host = flow.request.host  # 域名
        self.path = flow.request.path  # 接口地址
        self.method = flow.request.method  # 请求方式
        self.params = dict(flow.request.query or {})
        self.content = flow.request.content
        self.timestamp_start = flow.request.timestamp_start  # 请求开始时间戳
        self.timestamp_end = flow.request.timestamp_end  # 请求结束时间戳
        self.headers = flow.request.headers  # 请求头
        self.body = flow.request.text  # 请求体

    def response(self, flow: mitmproxy.http.HTTPFlow):
        response_status_code = flow.response.status_code  # 响应状态码
        response_text = flow.response.text  # 响应体
        response_content = flow.response.content
        response_timestamp_start = flow.response.timestamp_start  # 响应开始时间
        response_timestamp_end = flow.response.timestamp_end  # 响应结束时间
        response_header = flow.response.headers  # 响应头

        self.records.append({
            "URL": self.url,
            "Method": self.method,
            "Headers": self.headers,
            "Params": self.params,
            "Body": self.body,
            "Response Text": response_text,
            "Status Code": response_status_code
        })

        """保存记录到 CSV 文件"""
        with open(r"filtered_requests.csv", "a+", newline="", encoding="utf-8") as csvfile:
            fieldnames = ["URL", "Method", "Headers", "Params", "Body", "Response Text", "Status Code"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for record in self.records:
                writer.writerow(record)


addons = [CaptureInfoWriteFile()]
