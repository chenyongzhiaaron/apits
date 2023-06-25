def setup(request):
    """前置脚本处理请求对象的逻辑代码"""
    # rquest 对象输出如下：
    """{'Run': 'YES', 'Time': 1, 
    'Url': '/auth/loginByNotBip', 
    'Headers': '{"Content-Type": "application/json"}', 
    'Params': None,
    'Request Data': '{"account": "{{account}}", "password": "{{passwd}}"}',
    'Expected': None,
    'Response': '',
    'Assertion': '', 
    'Error log': '',
    None: None}"""

    # 获取请求参数
    request.get("Request Data")  # 获取到的结果是一个json字符串，使用需要转字典
    return request


def teardown(response):
    # print(f"执行后置代码片段处理：{response.json}")
    """后置脚本处理响应对象的逻辑代码"""
    return response
