# -*- coding:utf-8 -*-
"""
Time: 2020/6/17/017 10:52
Author: 陈勇志
Email:262667641@qq.com
Project:api_project
"""
import time

import requests
import urllib3

from common.file_handling.get_all_path import get_all_path

urllib3.disable_warnings()


class WxWorkSms:
    # header = {"Content-Type": "multipart/form-data"}
    headers = {"Content-Type": "application/json"}

    def __init__(self, key):
        self.send_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
        self.up_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type=file"

    def send_markdown(self, project_name, project_port, total_cases, pass_rate, success_cases, fail_cases, skip_cases,
                      error_cases, report_url):
        """
        发送markdown 请求
        Returns:

        """
        send_markdown_data = {
            "msgtype": "markdown",  # 消息类型，此时固定为markdown
            "markdown": {
                "content": f"# **提醒！自动化测试反馈**\n#### **请相关同事注意，及时跟进！**\n"
                           f"> 项目名称：<font color=\"info\">{project_name}</font> \n"
                           f"> 项目指定端：<font color=\"info\">{project_port}</font> \n"
                           f"> 测试用例总数：<font color=\"info\">{total_cases}条</font>；测试用例通过率：<font color=\"info\">{pass_rate}</font>\n"
                           "> **--------------------运行详情--------------------**\n"
                           f"> **成功数：**<font color=\"info\">{success_cases}</font>\n**失败数：**<font color=\"warning\">{fail_cases}</font>\n "
                           f"> **跳过数：**<font color=\"info\">{skip_cases}</font>\n**错误数：**<font color=\"comment\">{error_cases}</font>\n"
                           f"> ##### **报告链接：** [jenkins报告,请点击后进入查看]{report_url}"
                # 加粗：**需要加粗的字**
                # 引用：> 需要引用的文字
                # 字体颜色(只支持3种内置颜色)
                # 标题 （支持1至6级标题，注意#与文字中间要有空格）
                # 绿色：info、灰色：comment、橙红：warning
            }
        }
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
            time.sleep(2)

    def upload_media(self, file_path) -> list:
        """

        Args:
            file_path: 文件路径

        Returns:上传文件后返回的每一个文件id

        """
        # print(f"file path: {file_path}")
        media_ids = []
        for fp in file_path:
            with open(fp, "rb") as f:
                send_data = {"media": f}
                res_html = requests.post(self.up_url, files=send_data, verify=False).json()
                media_id = res_html.get("media_id")
                media_ids.append(media_id)
        return media_ids

    def send_main(self, folder_path, project_name, project_port, total_cases, pass_rate, success_cases, fail_cases,
                  skip_cases,
                  error_cases, report_url):
        """
        发送markdown及上传文件
        Args:
            dirs：文件夹路径

        Returns:

        """
        self.send_markdown(
            project_name, project_port, total_cases, pass_rate, success_cases, fail_cases, skip_cases,
            error_cases, report_url
        )
        file_path = get_all_path(folder_path)
        self.send_file(file_path)




if __name__ == '__main__':
    dirs = r'D:\apk_api\api-test-project\OutPut\Reports'
    WxWorkSms('8b1647d4-dc32-447c-b524-548acf18a938').send_main(dirs, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    # WxWorkSms('8b1647d4-dc32-447c-b524-548acf18a938').send_markdown(1, 2, 3, 4, 5, 6, 7, 8, 9)
