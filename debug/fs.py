#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: fs.py
@time: 2023/6/19 17:17
@desc:
"""

from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    user_id = str(request.args.get("user_id"))
    return user_id


app.run()
