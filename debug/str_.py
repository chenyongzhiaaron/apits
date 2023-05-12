"""
------start-----
"""
import random

"""
1. 对用户输入的数据使用"+"切割（如果没有"+",提示用户重新输入），判断输入的值是否都是数字？
    如输入：5+9、test+999;输出:[5,9],["test",999]
"""
# while 1:
#     s = input("请输入如：5+9或9+5等，两个数字相加的表达式：")
#     if s.count("+") > 1 or s.find("+") == -1:
#         print("数据输入要求不能大于1个“+”且输入的数据不能不带“+”，请重新输入")
#         continue
#     if s.startswith("+") or s.endswith("+"):
#         print("输入的数据不“+”号开头或者“+”号结尾，请重新输入！")
#         continue
#     # 首先统计是否有 ：+号在里面，同时要求 +号 在第二位
#     if s.count("+") == 1:
#         res = s.split("+")
#         if len(res) < 2:
#             continue
#         num1, num2 = res
#         if num1.strip().isdigit() and num2.strip().isdigit():
#             print(f"是输入两数相加的表达式，{num1},{num2}")
#         print("切割结果", res)
#         break

"""
2. 写代码实现一个整数加法计算器（两数相加）。需求：要求能够处理用户输入如此的数据：“5 +9” 或 “ 5 + 9”，如果不带 ”+“，则让用户重新输入
   ，计算出两个值的和并打印。（提示：先“+号”分割，再判断相加处理）
"""
# while True:
#     input_res = input("请输入两数相加：")
#     if "+" not in input_res or input_res.count("+") > 1:
#         print("输入的数据必须包含 ”+“ 号且不能输入多个”++“，请重新输入！")
#         continue
#     if input_res.startswith("+") or input_res.endswith("+"):
#         print("输入的数据不“+”号开头或者“+”号结尾，请重新输入！")
#         continue
#     # 将字符串切割
#     print('')
#     num1, num2 = input_res.split("+")
#     if not num1.strip().isdigit() or not num2.strip().isdigit():
#         print("输入的表达式存在非数字，请重新输入！")
#         continue
#     if input_res.count("+") == 1:
#         print(f"计算结果：{int(num1) + int(num2)}")
#         break


"""
3. 补充代码实现用户认证。
   需求：提示用户输入手机号、验证码，全都验证通过之后才算登录成功（验证码大小写不敏感）,代码如下：

```
import random
code = random.randrange(1000,9999) # 生成动态验证码
msg = f"欢迎登录PythonTest系统，您的验证码为：{code},手机号为：{15131266666}"
print(msg)
# 请补充代码
```
"""
# random_code = random.randrange(1000, 9999)
# count = 0
# while count < 5:
#     phone = input("请输入手机号：")
#     code = input("请输入验证码：")
#     if not code.isdigit():
#         print("验证码必须是数字!")
#         count += 1
#         continue
#     if not phone.isdigit():
#         print("手机号必须是数字!")
#         count += 1
#         continue
#     if phone == "15131266666" and random_code == int(code):
#         msg = f"欢迎登录PythonTest系统，您的验证码为：{code},手机号为：{15131266666}"
#         print(msg)
#         break
#     else:
#         count += 1
#         if count == 4:
#             print("账号锁定")
#             break
#         print("手机号或者验证码不正确,请重新输入！")

"""
1. 有字符串 strs = "Auto Test",完成下面的操作：
    * 将 strs 变量对应的值中的 所有的 ”t” 替换为 “s”,并输出结果
    * 将 strs 变量对应的值中的 第一个 ”t” 替换为 “s”,并输出结果
    * 将 strs 变量对应的值根据第一个 ”t” 分割,并输出结果
    * 将 strs 变量对应的值变大写,并输出结果
    * 将 strs 变量对应的值变小写,并输出结果
    * 请输出 strs 变量对应的值的第 2 个字符
    * 请输出 strs 变量对应的值的前 3 个字符
    * 请输出 strs 变量对应的值的后 2 个字符
"""
# strs = "Auto Test"
# print(strs.replace("t", "s"))  # strs 变量对应的值中的 所有的 ”t” 替换为 “s”,并输出结果
# print(strs.replace("t", "s", 1))  # * 将 strs 变量对应的值中的 第一个 ”t” 替换为 “s”,并输出结果
# print(strs.split("t", 1))
# print(strs.upper())
# print(strs.lower())
# print(strs[1])
# print(strs[:3])
# print(strs[-2:])

"""
2. 有字符串s = “123a4b5c”
    * 通过对s切片形成新的字符串 “123”
    * 通过对s切片形成新的字符串 “a4b”
    * 通过对s切片形成字符串 “c”
    * 通过对s切片形成字符串 “ba2”
"""
# s = "123a4b5c"
# print(s[:3])
# print(s[3:6])
# print(s[-1:])
# print(s[-3::-2])

"""
3. 使用while和for循环对s=”321”进行循环，打印的内容依次是：”倒计时3秒”，”倒计时2秒”，”倒计时1秒”，”出发！”。
"""
# count = 0
# s = "321"
# while count < len(s):
#     print(f"倒计时{s[count]}秒")
#     count += 1
#     if count == len(s):
#         print("出发！")
#
# for i in range(len(s)):
#     print(f"倒计时{s[i]}秒")
#
#     if i + 1 == len(s):
#         print("出发！")

"""
4. 获取两次输入的内容，然后将所有数据获取并相加
```
 要求：
     将num1中的的所有数字找到并拼接起来
     将num1中的的所有数字找到并拼接起来
     然后将两个数字进行相加。
 num1 = input("请输入：") # 例如输入：asdfd123sf2312，那么将所有的数字找出来并拼接成：1232312
 num2 = input("请输入：") # 例如输入：a12dfd183sf23， 那么将所有的数字找出来并拼接成：1218323
 最后输出 res = 1232312 + 1218323
 提示：循环遍历判断数字则强转然后拼接然后强转再相加

 # 请补充代码
```
"""
# num1 = input("请输入：")
# num2 = input("请输入：")
# if not num1.strip() or not num2.strip():
#     print("不允许输入纯空格字符串")
#     exit()
#
# s1 = ""
# for i in num1:
#     if i.isdigit():
#         s1 += i
#
# s2 = ""
# for j in num2:
#     if j.isdigit():
#         s2 += j
# if not s1 or not s2:
#     print("存在输入的字符串中没有数字，无法继续")
#     exit()
#
# print(s1, s2)
# print("相加结果：", int(s1) + int(s2))

# s = "123sk"
# print(s[::2])
# print(s[-3:2:-1])
# print(s[4:2:-1])

lst = [1, 2, 3, 4, 5]
new_lst = lst[1:3]  # 切片得到新的列表 [2, 3]
lst.insert(2, 12)
print(lst)
print(new_lst)

