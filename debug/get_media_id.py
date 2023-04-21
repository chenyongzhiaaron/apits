#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: get_media_id.py
@time: 2023/4/18 12:17
@desc:
"""
import requests


class DingTalkRobot:
    # def __init__(self, webhook_url, secret):
    #     self.webhook_url = webhook_url
    #     self.secret = secret

    def send_file(self, file_path):
        url = "https://oapi.dingtalk.com/robot/send"
        params = {
            "access_token": "85df348a2e7e34f8849941f20ab2c1d4",
            "type": "file"
        }
        headers = {
            "Content-Type": "application/octet-stream"
        }
        with open(file_path, "rb") as f:
            response = requests.post(url, params=params, headers=headers, data=f)
        if response.status_code == 200:
            result = response.json()
            print(result)
            media_id = result["media_id"]  # 获取media_id
            return media_id
        else:
            raise Exception("Failed to upload file, status code: {}".format(response.status_code))


if __name__ == '__main__':
    DingTalkRobot().send_file("identify_results.txt")
