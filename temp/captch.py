#!/usr/bin/env python
# encoding: utf-8
'''
@author: kira
@contact: 262667641@qq.com
@file: captch.py
@time: 2022/1/11 10:26
@desc:
'''

import ddddocr


def captcha(file_path):
    orc = ddddocr.DdddOcr()

    with open(file_path, 'rb') as f:
        img_bytes = f.read()
    res = orc.classification(img_bytes)
    print(res)


if __name__ == '__main__':
    file = r'D:\api-test-project\image\origina388l.png'
    captcha(file)
