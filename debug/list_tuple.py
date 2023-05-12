#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: list_tuple.py
@time: 2023/5/11 9:24
@desc:
"""

"""
1. 写代码，有如下列表，按照要求实现每一个功能。

```python
li = ["test", "pre", "pro", 'mock']
```

    * 计算列表长度并打印
    * 通过步长获取索引为偶数的所有值，并打印
    * 在列末尾添加元素 "dev"
    * 在列表第3个位置插入元素 "debug",并输出修改后的列表
    * 将 li2 = ["TEST","PRE","PRO","MOCK"] 的每一个元素追加到 li 中，并输出添加后的列表
    * 将 字符串 s = '123456' 的每一个元素添加到列表 li 中，一行代码实现，不允许使用循环
    * 删除 li 中的元素 "mock",并输出删除后的列表
    * 删除 li 中第二个元素,并输出删除后元素的列表
    * 删除列表 li 中第2至第4个元素，并输出删除元素后的列表
    * 将字符串 s = "['abcdefg']",快速转换为列表：['abcdefg']，要求尽可能使用多种方法
"""
# 解
# li = ["test", "pre", "pro", 'mock']
# print("列表长度：", len(li))
#
# print("通过步长获取索引为偶数的所有值:", li[::2])
#
# li.append("dev")
# print("在列末尾添加元素 "dev"",li)
#
# li.insert(2, "debug")
# print("在列表第3个位置插入元素\"debug\"", li)
# li2 = ["TEST", "PRE", "PRO", "MOCK"]
# li.extend(li2)
# print("将 li2 = [\"TEST\",\"PRE\",\"PRO\",\"MOCK\"] 的每一个元素追加到 li 中:", li)

# 将 字符串 s = '123456' 的每一个元素添加到列表 li 中，一行代码实现，不允许使用循环
# s = "123456"
# li.extend(list(s))
# print(li)


# li.remove("mock") # 删除 li 中的元素 "mock",并输出删除后的列表
# print(li)

# li.pop(1)  # 删除 li 中第二个元素,并输出删除后元素的列表
# print(li)

# del li[1:5]  # 删除列表中第二至第四个元素
# print(li)

# 将字符串 s = "['abcdefg']",快速转换为列表：['abcdefg']
# s = "['abcdefg']"
# lis = [s.replace("['", "").replace("']", "")]  # 方法一
# print(lis)
#
# lis = eval(s)  # 方法二
# print(lis)
#
# lis = json.loads(json.dumps(s))  # 方法三
# print(lis)
#
# lis = s[2:-2].split("，")  # 方法四
# print(lis)

"""

2. 写代码，有如下列表，按照要求实现每一个功能

```python
lis = [2, 3, "k", ["qwe", 20, ["k1", ["tt", 3, "1"]], 89], "ab", "adv"]
```
    * 将 lis 中的 'k' 变成大写，并打印
    * 将 lis 中的所有数字 3 变更成 100
    * 对 lis 切片，获取新列表 ["tt","1"]
    * 对 lis 切片，获取新列表 ["ab","k"]
"""

lis = [2, 3, "k", ["qwe", 20, ["k1", ["tt", 3, "1"]], 89], "ab", "adv"]

# 将 lis 中的 'k' 变成大写，并打印
# for i in range(len(lis)):
#     if lis[i] == 'k':
#         lis[i] = lis[i].upper()
# print(lis)

# 将 lis 中的所有数字 3 变更成 100
lis = [2, 3, "k", ["qwe", 20, ["k1", ["tt", 3, "1"]], 89], "ab", "adv"]

# 方式一，深层for循环
# for i in range(len(lis)):
#     if isinstance(lis[i], int) and lis[i] == 3:
#         lis[i] = 100
#     elif isinstance(lis[i], list):
#         for j in range(len(lis[i])):
#             if isinstance(lis[i][j], int) and lis[i][j] == 3:
#                 lis[i][j] = 100
#             elif isinstance(lis[i][j], list):
#                 for k in range(len(lis[i][j])):
#                     if isinstance(lis[i][j][k], int) and lis[i][j][k] == 3:
#                         lis[i][j][k] = 100
#                     elif isinstance(lis[i][j][k], list):
#                         for h in range(len(lis[i][j][k])):
#                             if isinstance(lis[i][j][k][h], int) and lis[i][j][k][h] == 3:
#                                 lis[i][j][k][h] = 100
# print(lis)

# 方式二，递归在原列表上修改
# def modify_three(lst):
#     """使用递归"""
#     for i, v in enumerate(lst):
#         if isinstance(v, int) and v == 3:
#             lst[i] = 100
#         elif isinstance(v, list):
#             modify_three(v)
#
#
# modify_three(lis)
# print(lis)

# 方式三，递归在原列表上修改
# def replace_num(lst):
#     new_lst = []
#     for i, item in enumerate(lst):
#         if isinstance(item, list):
#             new_lst.append(replace_num(item))
#         elif item == 3:
#             new_lst.append(100)
#         else:
#             new_lst.append(item)
#     return new_lst
# lis = [2, 3, "k", ["qwe", 20, ["k1", ["tt", 3, "1"]], 89], "ab", "adv"]

# 方式四，在原列表上修改
# stack = [lis]
# while stack:
#     lst = stack.pop()
#     for i in range(len(lst)):
#         if isinstance(lst[i], int) and lst[i] == 3:
#             lst[i] = 100
#         elif isinstance(lst[i], list):
#             stack.append(lst[i])
#
# print(lis)

# 对 lis 切片，获取新列表 ["tt","1"]
# sublist = lis[3][2][1][1::2]
# print(sublist)
#
# # 对 lis 切片，获取新列表 ["ab","k"]
# sublist = lis[-2::-2]
# print(sublist)

"""
3. 代码循环输出元素 `user_list = ["aa","bb","cc"]`
```shell
1 aa
2 bb
3 cc
```
"""
user_list = ["aa", "bb", "cc"]
for i in range(len(user_list)):
    print(i + 1, user_list[i])

# 面试题
"""
1. 比较值 v1 = (1) 和 v2 = 1 和 v3 = (1,) 有什么区别？
2. 比较值 v1 = ((1),(2),(3)) 和 v2 = ((1,),(2,),(3,),) 有什么区别？
"""

# 1. 比较值 v1 = (1) 和 v2 = 1 和 v3 = (1,) 有什么区别？
# v1 是数字1，v2 也是数字1，v3 是元组

# 2. 比较值 v1 = ((1),(2),(3)) 和 v2 = ((1,),(2,),(3,),) 有什么区别？
# v1 元组中存的元素都是数字，V2 元组中存的元素都是一个个的元组

