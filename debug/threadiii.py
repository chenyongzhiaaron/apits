#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: thread.py
@time: 2023/4/26 10:24
@desc:
"""
import time
import threading


def ts():
    for i in range(10):
        print(f"--------ts:{threading.current_thread().name}---------")
        time.sleep(2)


print("main_process")

t = threading.Thread(target=ts)  # 创建1个线程
t.setDaemon(True)  # 设置为守护线程
t.start()  # 启动线程
t.join(3)  # 阻塞主线程结束，等待3秒前置结束
