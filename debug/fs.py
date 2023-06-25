#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: fs.py
@time: 2023/6/19 17:17
@desc:
"""

import json
import json

data = {
	"name": "kira",
	"age": 18,
	"hobby": ["唱歌", "吹牛"],
	"friends": [
		{"name": "刘德华"},
		{"name": "梁朝伟"}
	]
}
json_str = json.dumps(data)
print(json_str)

print(json.dumps(data, ensure_ascii=False))
print(json.dumps(data, ensure_ascii=False, indent=4))
print(json.dumps(data, ensure_ascii=False, indent=4, sort_keys=True))
