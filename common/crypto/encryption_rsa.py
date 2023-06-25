#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: encryption_rsa.py
@time: 2023/4/3 10:33
@desc:
"""
import base64
import rsa


class Rsa:
	def __init__(self, st: str):
		self.st = st
	
	# rsa加密
	def rsa_encrypt(self):
		# 生成公钥、私钥
		(pubkey, privkey) = rsa.newkeys(1024)
		print("公钥: ", pubkey)
		print("私钥: ", privkey)
		# 明文编码格式
		content = self.st.encode('utf-8')
		# 公钥加密
		crypto = rsa.encrypt(content, pubkey)
		# # 一般加密的密文会以base64编码的方式输出
		b_res = base64.b64encode(crypto).decode()
		return b_res, privkey
	
	# rsa解密
	def rsa_decrypt(self, pk):
		# 私钥解密
		st = base64.b64decode(self.st.encode())
		content = rsa.decrypt(st, pk)
		con = content.decode('utf-8')
		
		return con
