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
					api['Headers Crypto'] = ''
					api['Query Str'] = ''
					body = request.get('body')
					if body:
						# api接口请求参数类型
						request_mode = body.get('mode')
						if 'raw' == request_mode:
							api['Request Data Type'] = 'json'
						elif 'formdata' == request_mode:
							api['Request Data Type'] = 'data'
						elif 'urlencoded' == request_mode:
							api['Request Data Type'] = 'data'
						
						# api接口请求参数
						request_data = body.get(request_mode)
						api['Request Data'] = {}
						if request_data and 'raw' == request_mode:
							api['Request Data'].update(
								json.loads(request_data.replace('\t', '').replace('\n', '').replace('\r', '')))
						elif request_data and 'formdata' == request_mode:
							if isinstance(request_data, list):
								for item in request_data:
									if item.get("type") == "text":
										api['Request Data'].update({item.get('key'): item.get("value", "")})
									elif item.get("type") == "file":
										api["Request Data"].update({item.get('key'): item.get("src", "")})
										api["Request Data Type"] = "files"
						api["Request Data"] = json.dumps(api["Request Data"], ensure_ascii=False)
						api['Setup Script'] = ''
						api['Request Data Crypto'] = ''
						api['Extract Request Data'] = ''
						api['Jsonpath'] = ''
						api['Regex'] = ''
						api['Regex Params List'] = ''
						api['Retrieve Value'] = ''
						api['SQL'] = ''
						api['Sql Params Dict'] = ''
						api['Teardown Script'] = ''
						api['Expected'] = ''
						api['Response'] = ''
						api['Assertion'] = ''
						api['Error Log'] = ''
				
				result.append(api)
	
	for _ in data:
		_parse_api(content=data)
	return result


if __name__ == '__main__':
	pat = r'..\..\cases\temporary_file\postman.json'
	res = parsing_postman(pat)
	from common.file_handling.excel import DoExcel
	from common.config import Config
	
	templates = Config.templates  # 使用标准模板
	ex = DoExcel(templates)
	ex.do_main("postman.xlsx", *res)
