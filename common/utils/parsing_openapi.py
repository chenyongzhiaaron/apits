import json

from common.utils import logger


# @logger.log_decorator()
def parsing_openapi(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    count = 1
    test_cases = []
    paths = data.get('paths')
    for path, methods in paths.items():
        for method, details in methods.items():
            test_case = {
                "id": count,
                "name": "openapi",
                "description": details.get("summary"),
                "Run": "yes",
                "Time": "0.1",
                'method': method,
                'url': path,
                'headers': json.dumps(extract_parameters(details.get('parameters', []), 'header')),
                'Headers是否加密': "",
                'params': json.dumps(extract_parameters(details.get('parameters', []), 'query')),
                'request_data_type': determine_request_type(details.get('requestBody')),
                'request_data': json.dumps(extract_request_body(details.get('requestBody'))),
                '请求参数是否加密': '',
                '提取请求参数': '',
                'Jsonpath': '',
                '正则表达式': '',
                '正则变量': '',
                '绝对路径表达式': '',
                'SQL': '',
                'sql变量': '',
                '预期结果': '',
                '响应结果': '',
                '断言结果': '',
                '报错日志': ''}
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
