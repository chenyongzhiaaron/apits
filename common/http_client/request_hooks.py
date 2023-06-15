class Hooks:
    def __init__(self):
        self.before_request_funcs = []  # 存放 before_request 钩子函数的列表
        self.after_request_funcs = []  # 存放 after_request 钩子函数的列表

    def before_request(self, func):
        """
        注册 before_request 钩子函数，将其添加到 before_request_funcs 列表中
        """
        self.before_request_funcs.append(func)
        print(self.before_request_funcs)
        return func

    def after_request(self, func):
        """
        注册 after_request 钩子函数，将其添加到 after_request_funcs 列表中
        """
        self.after_request_funcs.append(func)
        print(self.after_request_funcs)
        return func

    def run_before_request_funcs(self, request):
        """
        依次执行 before_request 钩子函数，处理请求参数并返回处理后的请求对象
        """
        for func in self.before_request_funcs:
            request = func(request)
        return request

    def run_after_request_funcs(self, response):
        """
        依次执行 after_request 钩子函数，处理响应结果并返回处理后的响应对象
        """
        for func in self.after_request_funcs:
            response = func(response)
        return response
