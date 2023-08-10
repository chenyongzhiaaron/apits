#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: parsing_postman.py
@time: 2023/8/8 10:58
@desc:
"""

import json

from common.file_handling.file_utils import FileUtils

id_count = 0
result = []


def parsing_postman(path):
	"""
	解析postman导出的json文件 转为excel测试用例
	Args:
	    path:
    
	Returns:
 
	"""
	data = FileUtils.read_json_data(path)
	
	def _parse_api(content):
		global result
		global id_count
		api = {}
		if isinstance(content, list):
			for item in content:
				_parse_api(content=item)
		elif isinstance(content, dict):
			if 'item' in content.keys():
				_parse_api(content=content.get('item'))
			elif 'request' in content.keys():
				id_count += 1
				api['Id'] = id_count
				api['Name'] = 'postman'
				api['Description'] = content.get('name')
				request = content.get('request')
				api['Run'] = 'yes'
				api['Time'] = 0.5
				if request:
					# api请求方法
					api['Method'] = request.get('method', 'GET').upper()
					header = request.get('header')
					header = {item.get('key'): item.get('value') for item in header} if header else {}
					auth = request.get('auth')
					if auth:
						auth_type = auth.get('type')
						if auth.get(auth_type):
							auth_value = {item.get('key'): item.get('value') for item in auth.get(auth_type) if
							              (item and item.get('key'))}
							header.update(auth_value)
					# api 请求地址
					url = request.get('url')
					if url:
						api['Url'] = url.get('raw')
					# if url and url.get('path'):
					#     # api请求URL
					#     api['Url'] = r'/'.join(url.get('path'))
					#
					# if url and url.get('query'):
					#     # api查询参数
					#     api['Request Data'] = '&'.join(
					#         [item.get('key') + '=' + (item.get('value') or '') for item in url.get('query') if item])
					# api请求头
					api['Headers'] = json.dumps(header, ensure_ascii=False)
					api['HeadersCrypto'] = ''
					api['QueryStr'] = ''
					body = request.get('body')
					if body:
						# api接口请求参数类型
						request_mode = body.get('mode')
						if 'raw' == request_mode:
							api['RequestDataType'] = 'json'
						elif 'formdata' == request_mode:
							api['RequestDataType'] = 'data'
						elif 'urlencoded' == request_mode:
							api['RequestDataType'] = 'data'
						
						# api接口请求参数
						request_data = body.get(request_mode)
						api['RequestData'] = {}
						if request_data and 'raw' == request_mode:
							api['RequestData'].update(
								json.loads(request_data.replace('\t', '').replace('\n', '').replace('\r', '')))
						elif request_data and 'formdata' == request_mode:
							if isinstance(request_data, list):
								for item in request_data:
									if item.get("type") == "text":
										api['RequestData'].update({item.get('key'): item.get("value", "")})
									elif item.get("type") == "file":
										api["RequestData"].update({item.get('key'): item.get("src", "")})
										api["RequestDataType"] = "files"
						api["RequestData"] = json.dumps(api["RequestData"], ensure_ascii=False)
						api['SetupScript'] = ''
						api['RequestDataCrypto'] = ''
						api['ExtractRequestData'] = ''
						api['Jsonpath'] = ''
						api['Regex'] = ''
						api['RegexParamsList'] = ''
						api['RetrieveValue'] = ''
						api['SQL'] = ''
						api['SqlParamsDict'] = ''
						api['TeardownScript'] = ''
						api['Expected'] = ''
						api['Response'] = ''
						api['Assertion'] = ''
						api['ErrorLog'] = ''
				
				result.append(api)
	
	for _ in data:
		_parse_api(content=data)
	return result


if __name__ == '__main__':
	pat = r'..\..\cases\temporary_file\postman.json'
	res = parsing_postman(pat)
	from common.file_handling.excel import DoExcel
	from config import Config
	
	templates = Config.TEMPLATES  # 使用标准模板
	ex = DoExcel(templates)
	ex.do_main("postman.xlsx", *res)
