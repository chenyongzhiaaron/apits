import threading


class MyLock:
    """锁实现"""

    def __init__(self):
        self.locked = False
        self.locked_by = None
        self.count = 0

    def acquire(self):
        """枷锁"""
        current_threading = threading.current_thread()  # 获取当前线程
        # 如果被锁了且不是当前线程去锁他，那么开始等待锁释放
        if self.locked and self.locked_by != current_threading:
            while self.locked:
                pass
        # 执行枷锁

        self.locked = True
        self.locked_by = current_threading
        self.count += 1

    def released(self):
        """释放锁"""
        current_threading = threading.current_thread()
        # 如果锁没有被锁或者不是当前线程的锁，直接退出释放
        if not self.locked or self.locked_by != current_threading:
            return
        # 执行释放锁
        self.count -= 1
        if self.locked == 0:
            # 锁定次数为0后，则完全释放锁
            self.locked = False
            self.locked_by = None
