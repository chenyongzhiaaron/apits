import threading

num = 0

mutex = threading.Lock()


def add1():
    global num
    for i in range(10000000):
        mutex.acquire()
        num += 1
        mutex.release()

    print(f"add1:{num}")


def add2():
    global num
    for i in range(10000000):
        mutex.acquire()
        num += 1
        mutex.release()

    print(f"add2:{num}")


if __name__ == '__main__':
    import threading

    t1 = threading.Thread(target=add1)
    t2 = threading.Thread(target=add2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(num)
