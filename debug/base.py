# -*- coding: utf-8 -*-
import datetime
import threading
import time

number = 0
lk = threading.Lock()


def update_num(args):
    """修改全局变量的函数"""
    global number
    # lk.acquire()  # 枷锁
    with lk:
        for i in range(100000000):
            number += 1
    print(
        f"当前线程：{threading.current_thread()},当前活跃线程：{threading.active_count()},当前任务执行后的结果：{number}")
    # lk.release()  # 释放锁


st = time.time()
ts = []
for i in range(2):
    # 实例2个线程
    t = threading.Thread(target=update_num, args=(lk,))  # 传入锁
    t.start()  # 启动线程
    ts.append(t)

for i in ts:
    i.join()  # 阻塞
e_t = time.time()
print("主线程结束", number, "耗时", e_t - st)
