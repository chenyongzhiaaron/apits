from common.data_extraction.dependent_parameter import DependentParameter
from common.crypto.encryption_main import do_encrypt
from common.http_client.request_hooks import Hooks
from common.utils.mylogger import MyLogger

dep_par = DependentParameter()  # 参数提取类实例化
logger = MyLogger()
hooks = Hooks()


@logger.log_decorator()
@hooks.before_request
def update_url(request):
	"""更新url"""
	request.url = dep_par.replace_dependent_parameter(request.url)
	print(request.url)
	return request


@logger.log_decorator()
@hooks.before_request
def update_header(request):
	"""更新请求头"""
	request.headers = dep_par.replace_dependent_parameter(request.headers)
	print(request.headers)
	return request


@logger.log_decorator()
@hooks.before_request
def update_body(request):
	"""更新请求参数"""
	if request.json:
		request.json = dep_par.replace_dependent_parameter(request.json)
		if request.encryption:
			request.data = do_encrypt(request.encryption, request.json)  # 数据加密：MD5 ｏｒ　ｓｈａ１
	else:
		request.data = dep_par.replace_dependent_parameter(request.data)
		if request.encryption:
			request.data = do_encrypt(request.encryption, request.data)  # 数据加密：MD5 ｏｒ　ｓｈａ１
	
	return request


@logger.log_decorator()
@hooks.before_request
def update_expected(request):
	"""更新预期结果"""
	request.expected = dep_par.replace_dependent_parameter(request.expected)
	print(request.expected)
	return request


@logger.log_decorator()
@hooks.after_request
def parse_json(response):
	"""
	尝试将响应中的内容解析为 JSON 格式
	"""
	try:
		response.json_data = response.json()
	except ValueError:
		response.json_data = None
	return response
