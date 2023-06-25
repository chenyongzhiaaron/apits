#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: captcha.py
@time: 2022/1/11 10:26
@desc:
"""

import ddddocr


def captcha(file_path):
	"""
	失败图片验证码
	Args:
	    file_path:
    
	Returns:返回图片的验证码
 
	"""
	orc = ddddocr.DdddOcr()
	
	with open(file_path, 'rb') as f:
		img_bytes = f.read()
	res = orc.classification(img_bytes)
	print(str(res))


if __name__ == '__main__':
	file = r'/image/origina388l.png'
	captcha(file)
