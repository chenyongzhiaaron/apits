import datetime
import threading
import time

number = 0


def add():
    global number  # global声明此处的number是外面的全局变量number
    for _ in range(10000000):  # 进行一个大数级别的循环加一运算
        number += 1
    times = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{times}-"当前活跃的线程个数：{threading.active_count()}"')
    print("子线程%s运算结束后，number = %s" % (threading.current_thread().getName(), number))
    print('------------------------------')


for i in range(2):  # 用2个子线程，就可以观察到脏数据
    t = threading.Thread(target=add)
    t.start()

time.sleep(2)  # 等待2秒，确保2个子线程都已经结束运算。

print("主线程执行完毕后，number = ", number)