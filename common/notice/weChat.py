#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: weChat.py
@time: 2023/8/8 10:59
@desc:
"""

import requests
import urllib3

urllib3.disable_warnings()
from config import Config


class WeChat:
    headers = {"Content-Type": "application/json"}

    def __init__(self, notice_content):
        self.send_url = Config.weixin_notice.get('send_url')
        self.up_url = Config.weixin_notice.get("upload_url")
        self.notice_content = notice_content
        self.file_lists = Config.weixin_notice.get("file_lists")

    def send_markdown(self):
        """
        发送markdown 请求
        Returns:

        """
        notice_content = self.notice_content
        send_markdown_data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": notice_content
            }}
        # "markdown": {
        #     "content": f"# **提醒！自动化测试反馈**\n#### **请相关同事注意，及时跟进！**\n"
        #                f"> 项目名称：<font color=\"info\">{project_name}</font> \n"
        #                f"> 项目指定端：<font color=\"info\">{project_port}</font> \n"
        #                f"> 测试用例总数：<font color=\"info\">{total_cases}条</font>；测试用例通过率：<font color=\"info\">{pass_rate}</font>\n"
        #                "> **--------------------运行详情--------------------**\n"
        #                f"> **成功数：**<font color=\"info\">{success_cases}</font>\n**失败数：**<font color=\"warning\">{fail_cases}</font>\n "
        #                f"> **跳过数：**<font color=\"info\">{skip_cases}</font>\n**错误数：**<font color=\"comment\">{error_cases}</font>\n"
        #                f"> ##### **报告链接：** [jenkins报告,请点击后进入查看]{report_url}"
        #     # 加粗：**需要加粗的字**
        # 引用：> 需要引用的文字
        # 字体颜色(只支持3种内置颜色)
        # 标题 （支持1至6级标题，注意#与文字中间要有空格）
        # 绿色：info、灰色：comment、橙红：warning
        # }
        # }
        requests.post(url=self.send_url, headers=self.headers, json=send_markdown_data, verify=False).json()

    def send_file(self, file_path):
        """
        文件路径
        Args:
            file_path:

        Returns:

        """
        media_id = self.upload_media(file_path)
        for i in media_id:
            send_data = {"msgtype": "file", "file": {"media_id": i}}
            requests.post(self.send_url, headers=self.headers, json=send_data, verify=False)
            import time
            time.sleep(2)

    def upload_media(self, file_lists) -> list:
        """

        Args:
            file_lists: 文件路径

        Returns:上传文件后返回的每一个文件id

        """
        # print(f"file path: {file_path}")
        media_ids = []
        if file_lists:
            for fp in file_lists:
                with open(fp, "rb") as f:
                    send_data = {"media": f}
                    res_html = requests.post(self.up_url, files=send_data, verify=False).json()
                    media_id = res_html.get("media_id")
                    media_ids.append(media_id)
            return media_ids

    def send_main(self):
        """
        发送markdown及上传文件
        Args:
            dirs：文件夹路径或文件路径

        Returns:

        """
        try:
            self.send_markdown()
        except Exception as e:
            print("发送markdown信息异常", e)
        try:
            self.send_file(self.file_lists)
        except Exception as e:
            print("发送企业微信附件异常", e)
