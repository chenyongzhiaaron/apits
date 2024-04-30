def setup(py):
	print(f"执行前置代码片段处理：{py.request}")
	"""处理请求对象的逻辑代码"""
	return py


def teardown(py):
	print(f"执行后置代码片段处理：{py.response}")
	"""处理响应对象的逻辑代码"""
	return py
