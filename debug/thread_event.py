#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: thread_event.py
@time: 2023/4/27 16:05
@desc:
"""
import threading
import time
import datetime

event = threading.Event()


class Boss(threading.Thread):
    def run(self) -> None:
        print("BOSS: 开始发版上线")
        event.set()  # 开始一个事件
        time.sleep(10)
        print("BOSS: 发版成功，大伙吃鸡腿去")
        event.set()


class Worker(threading.Thread):
    def run(self) -> None:
        print(f"Worker: 看看BOSS 发话了吗？{event.is_set()}")
        event.wait()  # 等待发号命令
        for i in range(5):
            print('拼命干，拼命干')
            time.sleep(0.5)
        event.clear()  # 干完了，给个信号 Boss,等下一次发话
        print(f"Worker: 去看看 Boss 说啥了？{event.is_set()}")
        event.wait()
        print(f"Worker：下班回家")


if __name__ == '__main__':
    event = threading.Event()
    thread = []
    for i in range(5):
        thread.append(Worker())

    thread.append(Boss())
    for t in thread:
        t.start()
    for t in thread:
        t.join()
    print("苦逼打工人，打车回家")
