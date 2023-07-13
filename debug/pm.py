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
