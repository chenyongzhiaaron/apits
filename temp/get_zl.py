#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: parse_html.py
@time: 2023/5/5 16:58
@desc:
"""
import threading
import queue
import requests
from queue import Queue
from collections import namedtuple
from requests_html import HTMLSession
from bs4 import BeautifulSoup

"""
多线程爬取网站html内容并保存
"""


def save_markdown_file(folder_path, file_name, content):
    """
    保存Markdown文件
    :param file_name: 文件名
    :param content: 文件内容
    :param folder_path: 文件夹路劲
    """
    path = f'{folder_path}/{file_name}.md'
    with open(path, "w", encoding="utf-8") as file:
        file.write(content)


def get_url_list(url):
    headers = {
        'user-agent': 'PostmanRuntime/7.29.2',
        'Accept-Encoding': 'gzip,deflate,br'
    }
    session = HTMLSession()
    resp = session.get(url, headers=headers)
    resp.html.render(timeout=30, sleep=5)
    soup = BeautifulSoup(resp.html.html, "html.parser")
    links = soup.find_all(name='a')
    Links = namedtuple('Link', ["url", 'href', 'text'])
    links_list = []
    # 所有连接存到命名元组中
    for link in links:
        if link.get("href").startswith("#"):
            links_list.append(Links(url, link.get("href"), link.text))
    print("links_list: ", links_list)
    q = Queue()
    for link in links_list:
        q.put(link)
    return q


class DetailThread(threading.Thread):
    """
    获取详情html页面信息的线程
    """

    def __init__(self, links_queue, detail_queue):
        super().__init__()
        self.links_queue = links_queue  # 地址队列
        self.detail_queue = detail_queue  # 详情队列

    def run(self):
        """
        执行线程
        """
        Ls = namedtuple("Ls", ["title", "response"])
        while True:
            try:
                links = self.links_queue.get(timeout=1)
                print(links.href)
            except queue.Empty:
                # 队列已经为空，退出循环
                break
            host = links.url.split("index")[0]
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Cookie': 'Hm_lvt_16719b41a1a7ca625adff82eb7d38292=1683512202; csrftoken=gbS4N1JIYG7dkTe5dFAV0jtQlgbVXwI3tcu7FDOT0chMJ4h7jhhNxYqIfhdSlSYU; avsessionid=y1qlutzpuxy73iznsxk9we06o9dvawyp; Hm_lpvt_16719b41a1a7ca625adff82eb7d38292=1683603143; avsessionid=y1qlutzpuxy73iznsxk9we06o9dvawyp',
                'Pragma': 'no-cache',
                'Referer': 'https://pythonav.com/wiki/',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.35',
                'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"'
            }
            resp = requests.get(host + links.href.replace("#", "") + ".md", headers=headers)
            resp.encoding = resp.apparent_encoding
            self.detail_queue.put(Ls(title=links.text, response=resp.text))


class SaveDetailThread(threading.Thread):
    """
    保存详情地址的线程
    """

    def __init__(self, folder_path, detail_queue):
        super().__init__()
        self.detail_queue = detail_queue
        self.folder_path = folder_path

    def run(self):
        """
        执行线程
        """
        # 将详情地址保存在“detail.txt”文件中
        while True:
            try:
                detail = self.detail_queue.get(timeout=1)
            except queue.Empty:
                # 队列已经为空，退出循环
                break
            save_markdown_file(self.folder_path, detail.title, detail.response)


def main(folder_path, url):
    """
    主函数
    """
    url_q = get_url_list(url)
    print("url_q", url_q)
    # 创建队列
    detail_queue = queue.Queue()
    # 创建保存详情线程
    save_thread = SaveDetailThread(folder_path, detail_queue)

    # 创建获取详情地址的线程并启动
    detail_threads = [DetailThread(url_q, detail_queue) for _ in range(2)]
    [t.start() for t in detail_threads]

    # 启动保存详情地址的线程
    save_thread.start()
    # 等待所有获取详情地址的线程完成
    [t.join() for t in detail_threads]

    # 等待保存详情地址的线程完成
    save_thread.join()


if __name__ == "__main__":
    import os
    from common.files_tools.read_file import read_file
    #
    # js = read_file('index.json')
    # for folder, url in js.items():
    #     if not os.path.exists(folder):
    #         os.mkdir(folder)
    #     main(folder, url)
    get_url_list()