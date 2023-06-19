import json

import requests


class Hooks:
    def __init__(self):
        self.before_request_funcs = {}
        self.after_request_funcs = {}

    def before_request(self, func):
        """
        注册 before_request 钩子函数
        """
        self.before_request_funcs[func.__name__] = func
        return func

    def after_request(self, func):
        """
        注册 after_request 钩子函数
        """
        self.after_request_funcs[func.__name__] = func
        return func

    def run_before_request_hooks(self, func_names, request, json_data):
        """
        执行 before_request 钩子函数
        """
        for func_name in func_names:
            if func_name in self.before_request_funcs:
                func = self.before_request_funcs[func_name]
                json_data = func(request, json_data)
        return json_data

    def run_after_request_hooks(self, func_names, response):
        """
        执行 after_request 钩子函数
        """
        for func_name in func_names:
            if func_name in self.after_request_funcs:
                func = self.after_request_funcs[func_name]
                response = func(response)
        return response


hooks = Hooks()
session = requests.Session()


def req(url, method, **kwargs):
    """
    发送请求并返回响应对象
    """
    before_hooks = kwargs.pop('before_hooks', [])
    after_hooks = kwargs.pop('after_hooks', [])
    json_data = kwargs.pop('json', {})

    request = requests.Request(method=method, url=url, **kwargs)
    prepared_request = session.prepare_request(request)

    json_data = hooks.run_before_request_hooks(before_hooks, prepared_request, json_data)
    prepared_request.body = json.dumps(json_data)
    response = session.send(prepared_request)
    response = hooks.run_after_request_hooks(after_hooks, response)

    return response


@hooks.before_request
def add_authentication_headers(request, json_data):
    """
    添加认证头信息
    """
    print("前置钩子函数，添加认证头信息", request)
    request.headers["Authorization"] = "Bearer YOUR_AUTH_TOKEN"
    return json_data


@hooks.before_request
def handle_dependent_parameters(request, json_data):
    """
    处理依赖参数
    """
    print("前置钩子函数,处理依赖参数", request)

    json_data["verification_code"] = get_verification_code()
    return json_data


def get_verification_code():
    # 实现获取验证码的逻辑
    return "YOUR_VERIFICATION_CODE"


@hooks.after_request
def after_dependent_parameters(request, json_data):
    """
    处理后置
    """
    print("后置钩子函数,处理依赖参数", request)

    return json_data


def test_user_registration():
    url = "http://jsonplaceholder.typicode.com/posts"
    data = {
        "userId": "testuser",
        "title": "password123",
        "body": "测试玩家勇哥"
    }
    headers = {
        "Content-Type": "application/json"
    }
    before_hooks = [add_authentication_headers.__name__, handle_dependent_parameters.__name__]
    after_hooks = [after_dependent_parameters.__name__]
    kwargs = {"json": data, "headers": headers}

    return req(url, "post", before_hooks=before_hooks, after_hooks=after_hooks, **kwargs)
    # assert response.status_code == 200
    # assert response.json()["success"] is True


if __name__ == "__main__":
    res = test_user_registration()
    print(res, res.text)
