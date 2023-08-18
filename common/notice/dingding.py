#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: dingding.py
@time: 2023/8/8 10:59
@desc:
"""
import base64
import hashlib
import hmac
import time
import urllib.parse

import requests

from config.config import Config


class DingTalk:
    """顶顶通知"""

    def __init__(self, title, notice_content, except_info):
        """"""
        self.url = Config.DINGTALK_NOTICE.get("url")
        self.notice_content = notice_content
        self.title = title
        self.except_info = except_info
        self.secret = Config.DINGTALK_NOTICE.get("secret")

    def sign(self):
        """加签"""
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return {"sign": sign, "timestamp": timestamp}

    def content(self):
        """markdown 内容"""
        if Config.DINGTALK_NOTICE.get("except_info"):
            self.notice_content += '\n ### 未通过用例详情：\n'
            self.notice_content += self.except_info
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title": '{}({})'.format(self.title, Config.DINGTALK_NOTICE.get("key")),
                "text": self.notice_content
            },
            "at": {
                "atMobiles": Config.DINGTALK_NOTICE.get("atMobiles"),
                "isAtAll": Config.DINGTALK_NOTICE.get("isatall")
            }
        }
        return data

    def send_info(self):
        """发送钉钉消息"""
        notice_content = self.content()
        if self.secret:
            sign = self.sign()
        else:
            sign = None
        try:
            requests.post(url=self.url, json=notice_content, params=sign)
        except Exception as e:
            print("发送钉钉异常", e)


if __name__ == '__main__':
    texts = "#### 杭州天气 @150XXXXXXXX \n > 9度，西北风1级，空气良89，相对温度73%\n > ![screenshot](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png)\n > ###### 10点20分发布 [天气](https://www.dingtalk.com) \n"
    print(DingTalk("杭州天气", texts).send_info())
