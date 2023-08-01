#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: get_set.py
@time: 2023/7/21 17:07
@desc:
"""
import csv

import mitmproxy.http


class RequestRecorder:
    def __init__(self):
        self.records = []
        self.url = None
        self.body = None
        self.params = None
        self.method = None
        self.headers = None
    
    def request(self, flow: mitmproxy.http.HTTPFlow):
        """获取请求数据"""
        if "bimdc.bzlrobot.com" in flow.request.url:
            self.url = flow.request.url
            self.method = flow.request.method
            self.headers = dict(flow.request.headers)
            self.params = dict(flow.request.query or {})
            self.body = flow.request.text
    
    def response(self, flow: mitmproxy.http.HTTPFlow):
        if "bimdc.bzlrobot.com" in flow.request.url:
            response_text = flow.response.text
            response_status_code = flow.response.status_code
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


addons = [
    RequestRecorder()
]
