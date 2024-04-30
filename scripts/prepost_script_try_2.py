def setup(py):
    """这是某某sheet 中第 xx条测试用例的前置脚本"""
    """前置脚本处理请求对象的逻辑代码"""
    # 从request 对象获取数据信息
    import json
    request_obj = py.request
    print("前置脚本请求对象=", request_obj)
    print("获取请求URL:", request_obj.get("Url"))
    print("获取请求Header:", json.loads(request_obj.get("Headers")))
    print("获取请求数据:", json.loads(request_obj.get("RequestData")))
    py.update_environments("emailwww", "这个是你想要的值")  # 设置环境变量
    print(f"---->获取环境变量={py.get_environments('{{emailwww}}')}")
    return py


def teardown(py):
    """这是某某sheet 中第 xx条测试用例的前置脚本"""
    """后置脚本处理响应对象的逻辑代码"""
    print("后置脚本响应对象=", str(py.response).replace("<", "(").replace(">", ")"))
    response_text = py.response.text
    response_json = py.response.json()
    print("响应对象转json：", response_json)
    print("响应对象转text：", response_text)
    py.update_environments("response_json", response_json)  # 设置环境变量
    print("获取环境变量={}".format(py.get_environments('{{response_json}}')))
    return py
