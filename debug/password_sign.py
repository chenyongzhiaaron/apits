#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: password_sign.py
@time: 2023/5/8 17:12
@desc:
"""
import sys
import json
import hashlib
import random
import datetime
import time

import requests

now_time = time.time()
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
stamp = str(int(round(now_time * 1000)))
reqId = "ga1a838aad7c85992b71bg3f717975d9"
loginAccount = "17328565609"
iampwd = "9056749f0dde456780a336ea05640d0a"
path = "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias="
random_str = str(random.random())
header = {"Connection": "keep-alive", "Content-Type": "application/json", "accessToken": "administrator-token",
          "User-Agent": "IOT2020TEST", "version": "7.1.0", "Content-Length": "98",
          "Host": "mp-prod.smartmidea.net"}


class PasswordSign:
    def do_sign(self, data):  # 签名
        """

        Args:
            data:请求body 参数

        Returns:

        """
        key = "prod_secret123@muc" + json.dumps(data) + str(random.random())
        m = hashlib.md5()
        m.update(key.encode('utf-8'))
        sign_ = m.hexdigest()
        return sign_

    def get_login_id(self):
        global header
        global random_str
        global stamp
        url = path + "/v1/user/login/id/get"
        data = {"loginAccount": loginAccount,
                "stamp": stamp,
                "reqId": reqId}
        sign_ = self.do_sign(data, random_str)
        headers = {"sign": sign_, "random": random_str}
        header.update(header)
        res = requests.post(url=url, json=data, headers=headers).json()
        value = res['data']['loginId']
        print("loginID:", value)
        return value

    def do_password(self):
        value = self.get_login_id()
        pw = value + hashlib.sha256("mm123456".encode("utf-8")).hexdigest() + "ad0ee21d48a64bf49f4fb583ab76e799"
        password = hashlib.sha256(pw.encode("utf-8")).hexdigest()  # 加密密码
        print("加密后的 password:", password)
        return password, value


if __name__ == '__main__':
    body = sys.argv[1]
    ps = PasswordSign()
    pwd, sign = ps.do_password()
