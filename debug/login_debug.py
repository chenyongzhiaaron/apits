import requests
import json
import time
import datetime
import random
import hashlib

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


def do_sign(dj, r):  # 签名
    key = "prod_secret123@muc" + json.dumps(dj) + r
    m = hashlib.md5()
    m.update(key.encode('utf-8'))
    sign_ = m.hexdigest()
    return sign_


def get_login_id():
    global header
    global random_str
    global stamp
    url = path + "/v1/user/login/id/get"
    data = {"loginAccount": loginAccount,
            "stamp": stamp,
            "reqId": reqId}
    sign = do_sign(data, random_str)
    headers = {"sign": sign, "random": random_str}
    header.update(header)
    res = requests.post(url=url, json=data, headers=headers).json()
    value = res['data']['loginId']
    print("loginID:", value)
    return value


def do_password():
    value = get_login_id()
    pw = value + hashlib.sha256("mm123456".encode("utf-8")).hexdigest() + "ad0ee21d48a64bf49f4fb583ab76e799"
    password = hashlib.sha256(pw.encode("utf-8")).hexdigest()  # 加密密码
    print("加密后的 password:", password)
    return password, value


def login():
    global loginAccount
    global iampwd
    global reqId
    global timestamp
    url = path + "/mj/user/login"
    password, login_id = do_password()
    data = {"iotData": {
        "loginAccount": loginAccount,
        "password": password,
        "clientType": 2,
        "loginId": login_id,
        "iotAppId": "900",
        "iampwd": iampwd,
        "reqId": reqId
    }, "data": {
        "appVersion": "6.2.0",
        "osVersion": "13.3",
        "appKey": "46579c15",
        "deviceId": "990008698831355",
        "deviceName": "OD105",
        "platform": 2
    }, "timestamp": timestamp}
    sign_ = do_sign(data, random_str)
    header = {"Connection": "keep-alive",
              "Content-Type": "application/json",
              "accessToken": "administrator-token",
              "sign": sign_,
              "random": random_str,
              "User-Agent": "IOT2020TEST",
              "version": "7.1.0",
              "Content-Length": "98",
              "Host": "mp-prod.smartmidea.net"}
    print(f"sign:{sign_}\ndata:{data}\nrandom:{random_str}")
    # res = requests.post(url=url, json=data, headers=header)
    # print("登录接口请求接口", res.text)


if __name__ == '__main__':
    val = get_login_id()
    login()

    print(len('d8c004809add1768bc130f2bd07380af'))
    print(len('940a7447601aca97583f49b06bea7aaa'))