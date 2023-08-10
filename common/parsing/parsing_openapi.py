#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: parsing_openapi.py
@time: 2023/8/8 10:58
@desc:
"""

import json


# @logger.log_decorator()
def parsing_openapi(file_path):
	"""解析swagger文件转为excel测试用例"""
	with open(file_path, 'r', encoding='utf-8') as file:
		data = json.load(file)
	count = 1
	test_cases = []
	paths = data.get('paths')
	for path, methods in paths.items():
		for method, details in methods.items():
			test_case = {
				"Id": count,
				"Name": "openapi",
				"Description": details.get("summary"),
				"Run": "yes",
				"Time": "0.1",
				'Method': method,
				'Url': path,
				'Headers': json.dumps(extract_parameters(details.get('parameters', []), 'header')),
				'HeadersCrypto': "",
				'QueryString': json.dumps(extract_parameters(details.get('parameters', []), 'query')),
				'RequestDataType': determine_request_type(details.get('requestBody')),
				'RequestData': json.dumps(extract_request_body(details.get('requestBody'))),
				'SetupScript': '',
				'RequestDataCrypto': '',
				'ExtractRequestData': '',
				'Jsonpath': '',
				'Regex': '',
				'RegexParamsList': '',
				'RetrieveValue': '',
				'SQL': '',
				'SqlParamsDict': '',
				'TeardownScript': '',
				'Expected': '',
				'Response': '',
				'Assertion': '',
				'ErrorLog': ''}
			test_cases.append(test_case)
			count += 1
	
	return test_cases


# @logger.log_decorator()
def extract_parameters(parameters, parameter_location):
	extracted_parameters = {}
	for param in parameters:
		if param.get('in') == parameter_location:
			param_name = param.get('name')
			param_example = param.get('example')
			if param_name and param_example:
				extracted_parameters[param_name] = param_example
	return extracted_parameters


# @logger.log_decorator()
def determine_request_type(request_body):
	if request_body:
		content = request_body.get('content', {})
		if 'multipart/form-data' in content:
			return 'files'
		elif 'application/json' in content:
			return 'json'
		elif 'application/x-www-form-urlencoded' in content:
			return 'data'
	return ''


# @logger.log_decorator()
def extract_request_body(request_body):
	if request_body:
		content = request_body.get('content', {})
		if 'multipart/form-data' in content:
			schema = content['multipart/form-data'].get('schema', {})
			if schema.get('type') == 'object':
				properties = schema.get('properties', {})
				extracted_body = {}
				for prop_name, prop_details in properties.items():
					if prop_details.get('type') == 'string':
						example = prop_details.get('example')
						if example:
							extracted_body[prop_name] = example
				return extracted_body
		elif 'application/json' in content:
			example = content['application/json'].get('example')
			if example:
				return example
		elif 'application/x-www-form-urlencoded' in content:
			schema = content['application/x-www-form-urlencoded'].get('schema', {})
			if schema.get('type') == 'object':
				properties = schema.get('properties', {})
				extracted_body = {}
				for prop_name, prop_details in properties.items():
					if prop_details.get('type') == 'string':
						example = prop_details.get('example')
						if example:
							extracted_body[prop_name] = example
				return extracted_body
	return {}


if __name__ == '__main__':
	file = f'../../cases/temporary_file/openapi.json'
	res = parsing_openapi(file)
	print(res)
	from common.file_handling.excel import DoExcel
	from config import Config
	
	templates = Config.TEMPLATES  # 使用标准模板
	ex = DoExcel(templates)
	ex.do_main("openapi.xlsx", *res)
