import gc


# 引用计数示例
# a = [1, 2, 3]
# b = a
# print(sys.getrefcount(a)-1)  # 输出2，a和b都引用了该对象
# b = None
# print(sys.getrefcount(a)-1)  # 输出1，只有a引用了该对象
#
# # 标记-清除算法示例
class Node:
    def __init__(self):
        self.next = None


node1 = Node()
node2 = Node()
node1.next = node2
node2.next = node1

res = gc.collect()  # 执行垃圾回收，循环引用的对象会被清除

# # 分代回收示例
# a = [1, 2, 3]
# gc.collect()
# print(gc.get_count())  # 输出(0, 0, 0)，第0代对象计数为1
# b = [4, 5, 6]
# c = [7, 8, 9]
# gc.collect()
# print(gc.get_count())  # 输出(1, 0, 0)，第0代对象计数为0，第1代对象计数为2
# d = [10, 11, 12]
# e = [13, 14, 15]
# gc.collect()
# print(gc.get_count())  # 输出(2, 0, 0)，第0代对象计数为0，第1代对象计数为0，第2代对象计数为2
#
# # 对象的代信息
# print(gc.get_objects())  # 输出对象的代信息
