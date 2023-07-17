# 前置脚本代码
def setup(pm):
    print("pm---------------->", pm.get_variables())
    # request_data = pm.get_variables()  # 获取得到请求数据
    """
    request_data 的值:  {'Url': '/login',
     'Headers': '{"Content-Type": "application/json"}',
      'Query Str': None,
       'Request Data Type': 'params',
       'Request Data': '{"account": "{{account}}", "password": "{{passwd}}"}',
       'Expected': None, 'Response': '', 'Assertion': '', 'Error Log': ''
       }
    """
    BSP_TOKEN = pm.get_environments("{{BSP_TOKEN}}")  # 获取环境变量
    pm.update_environments("BSP_TOKEN_NEWS", BSP_TOKEN + "修改了环境变量")  # 设置环境变量
    print("---->pm.get_environments", pm.get_environments("{{BSP_TOKEN_NEWS}}"))
    print("---->pm.get_variables", pm.get_variables())


setup(pm)


# 后置脚本代码
def tear_down(pm):
    vars_data = pm.get_environments("{{变量名称}}")  # 获取环境变量
    response = pm.get_variables()  # 获取得到响应结果对象
    response.json()
    print(f"请求地址 --> {response.request.url}")
    print(f"请求头 --> {response.request.headers}")
    print(f"请求 body --> {response.request.body}")
    print(f"接口状态--> {response.status_code}")
    print(f"接口耗时--> {response.elapsed}")
    print(f"接口响应--> {response.text}")
    token = response.json()['token']
    pm.update_environments("BSP_TOKEN_NEWS", token + vars_data)  # 重新设置环境变量
    print("---->pm.get_environments", pm.get_environments("{{BSP_TOKEN_NEWS}}"))
    print("---->pm.get_variables", pm.get_variables())


tear_down(pm)
