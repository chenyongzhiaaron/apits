# !/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: prepost_script.py
@time: 2023/6/16 16:58
@desc:
"""

from common.action import Action
from temp.hooks import hooks


@hooks.before_request
def add_authentication_headers(url, method, **kwargs):
    """
    添加认证头信息
    """
    print("------开始执行前置操作-----")
    headers = kwargs.get('headers', {})
    headers["Authorization"] = "Bearer " + "这是token"
    kwargs['headers'] = headers
    return kwargs


@hooks.before_request
def handle_dependent_parameters(url, method, **kwargs):
    """
    处理依赖参数
    """
    print("------开始执行后置操作-----")
    payload = kwargs.get('json', {})
    payload["title"] = payload.get("title")
    kwargs['json'] = payload
    return kwargs


# if __name__ == '__main__':
# 	action = Action()
# 	code = 'def setup(action):\n print(action.vars)\n print(action.get_variable())'
# 	ast_obj = ast.parse(code, mode='exec')
# 	compiled = compile(ast_obj, '<string>', 'exec')
# 	print("======>", compiled)
# 	result = exec(compiled, {"action": action})
if __name__ == '__main__':
    import ast
    
    action = Action()
    func_str = '\ndef setup(action):\n    print("action.vars",action.vars)\n    print("action.get_cariable()",action.get_variable())\n    \nsetup(action)'
    
    # 解析代码字符串为抽象语法树
    ast_obj = ast.parse(func_str, mode='exec')
    # 编译抽象语法树
    compiled = compile(ast_obj, '<string>', 'exec')
    # 执行编译后的代码
    exec(compiled, {"action": action})


