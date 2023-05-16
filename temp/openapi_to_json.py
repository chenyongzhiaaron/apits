import json

import json

import json
import json

import json
import json

import json

import json

import json

import json

def process_openapi_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    test_cases = []
    paths = data.get('paths')
    for path, methods in paths.items():
        for method, details in methods.items():
            test_case = {}
            test_case['url'] = path
            test_case['headers'] = extract_parameters(details.get('parameters', []), 'header')
            test_case['method'] = method
            test_case['params'] = extract_parameters(details.get('parameters', []), 'query')
            test_case['body'] = extract_request_body(details.get('requestBody'))
            test_cases.append(test_case)

    return test_cases

def extract_parameters(parameters, parameter_location):
    extracted_parameters = {}
    for param in parameters:
        if param.get('in') == parameter_location:
            param_name = param.get('name')
            param_example = param.get('example')
            if param_name and param_example:
                extracted_parameters[param_name] = param_example
    return extracted_parameters

def extract_request_body(request_body):
    if request_body:
        content = request_body.get('content', {})
        for media_type, details in content.items():
            if media_type == 'application/json':
                example = details.get('example')
                if example:
                    return example
    return {}


if __name__ == '__main__':
    file = f'openapi.json'
    res = process_openapi_file(file)
    print(res)
