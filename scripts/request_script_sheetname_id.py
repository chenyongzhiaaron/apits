def setup(request):
    print(f"执行前置代码片段处理：{request}")
    """处理请求对象的逻辑代码"""
    return request


def teardown(response):
    print(f"执行后置代码片段处理：{response}")
    """处理响应对象的逻辑代码"""
    return response
