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
            test_case['requestType'] = determine_request_type(details.get('requestBody'))
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

file = f'openapi.json'
res = process_openapi_file(file)
print(res)
