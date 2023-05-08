import requests
import json
import time
import datetime
import random
import hashlib

# import setting

# from test3 import AES128_de, AES128_en
# from Lib.readexcel import ReadExcel

# from sendrequests import SendRequests

now_time = time.time()
# timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
stamp = str(int(round(now_time * 1000)))


# -------------- 固定参数 --------------
# reqId = "ga1a838aad7c85992b71bg3f717975d9"
# loginAccount = "17328565609"
# iampwd = "9056749f0dde456780a336ea05640d0a"
# path = "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias="
# header = {"Connection": "keep-alive", "Content-Type": "application/json", "accessToken": "administrator-token",
#           "User-Agent": "IOT2020TEST", "version": "7.1.0", "Content-Length": "98",
#           "Host": "mp-prod.smartmidea.net"}


# -------------- 开始加签加密，并返回登录请求body --------------


class Login:
    def __init__(self, data, login_account, req_id, iam_pwd, pwd):
        self.data = data
        self.random_str = str(random.random())
        self.timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.reqId = req_id
        self.loginAccount = login_account
        self.iampwd = iam_pwd
        self.pwd = pwd
        self.path = "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias="
        self.headers = {"Connection": "keep-alive", "Content-Type": "application/json",
                        "accessToken": "administrator-token",
                        "User-Agent": "IOT2020TEST", "version": "7.1.0", "Content-Length": "98",
                        "Host": "mp-prod.smartmidea.net"}

    @staticmethod
    def md5(st: str) -> str:
        """
        Args:
            st:待加密字符串

        Returns: 返回MD5 加密后的字符串
        """
        md = hashlib.md5()  # 创建MD5对象
        md.update(st.encode(encoding="utf-8"))
        return md.hexdigest()

    @staticmethod
    def do_sign(data, random_int):
        """加签"""
        key = "prod_secret123@muc" + json.dumps(data) + random_int
        return Login.md5(key)

    def get_login_id(self):
        """获取登录id"""
        url = self.path + "/v1/user/login/id/get"
        data = {"loginAccount": self.loginAccount,
                "stamp": stamp,
                "reqId": self.reqId}
        sign = self.do_sign(data, self.random_str)
        headers = {"sign": sign, "random": self.random_str}
        headers.update(self.headers)
        res = requests.post(url=url, json=data, headers=headers).json()
        return res.get('data').get('loginId')

    def do_password(self):
        login_id = self.get_login_id()
        # 加密拼接
        pw = login_id + hashlib.sha256("mm123456".encode("utf-8")).hexdigest() + "ad0ee21d48a64bf49f4fb583ab76e799"
        # 如果原始密码是变的，那就用这条
        # pw = login_id + hashlib.sha256("mm123456".encode("utf-8")).hexdigest() + self.pwd
        password = hashlib.sha256(pw.encode("utf-8")).hexdigest()  # 二次加密密码
        print("加密后的 password:", password)
        return password, login_id

    def login(self, data):
        url = self.path + "/mj/user/login"
        password, login_id = self.do_password()

        data = {"iotData": {
            "loginAccount": self.loginAccount,
            "password": password,
            "clientType": 2,
            "loginId": login_id,
            "iotAppId": "900",
            "iampwd": self.iampwd,
            "reqId": self.reqId
        }, "data": {
            "appVersion": "6.2.0",
            "osVersion": "13.3",
            "appKey": "46579c15",
            "deviceId": "990008698831355",
            "deviceName": "OD105",
            "platform": 2
        }, "timestamp": self.timestamp}
        sign_ = self.do_sign(data, random_str)
        header = {"Connection": "keep-alive",
                  "Content-Type": "application/json",
                  "accessToken": "administrator-token",
                  "sign": sign_,
                  "random": random_str,
                  "User-Agent": "IOT2020TEST",
                  "version": "7.1.0",
                  "Content-Length": "98",
                  "Host": "mp-prod.smartmidea.net"}
        print(f"{sign_},{password},{self.timestamp}")

        res = requests.post(url=url, json=data, headers=header)
        print("登录接口请求接口", res.text)


if __name__ == '__main__':
    # val = get_login_id()
    # login()
    ...
