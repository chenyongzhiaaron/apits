# `使用一行代码实现将字符串 v = “k1|v1,k2|v2,k3|v3…” 转换成字典 {‘k1’:’v1’,’k2’:’v2’,’k3’:’v3’..}`
# 方法一
v = "k1|v1,k2|v2,k3|v3"
d = {i.split("|")[0]: i.split("|")[1] for i in v.split(",")}
print(d)

# 方法二
d = dict(i.split("|") for i in v.split(","))
print(d)
