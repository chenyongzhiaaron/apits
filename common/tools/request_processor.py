from common.extractor.dependent_parameter import DependentParameter
from common.extractor.data_extractor import DataExtractor
from common.encryption.encryption_main import do_encrypt
from common.tools.hooks import Hooks
from common.tools.logger import MyLog

hooks = Hooks()
logger = MyLog()

dep_par = DependentParameter()  # 参数提取类实例化


@hooks.before_request
def update_url(request):
    """更新url"""
    request.url = dep_par.replace_dependent_parameter(request.url)
    logger.my_log(f"请求地址 --> {request.url}", "info")
    return request


@hooks.before_request
def update_header(request):
    """更新请求头"""
    request.headers = dep_par.replace_dependent_parameter(request.headers)
    logger.my_log(f"请求头 --> {request.headers}", "info")
    return request


@hooks.before_request
def update_body(request):
    """更新请求参数"""
    if request.json:
        request.json = dep_par.replace_dependent_parameter(request.json)
        if request.encryption:
            request.data = do_encrypt(request.encryption, request.json)  # 数据加密：MD5 ｏｒ　ｓｈａ１
        logger.my_log(f"请求 body --> {request.json}", "info")
    else:
        request.data = dep_par.replace_dependent_parameter(request.data)
        if request.encryption:
            request.data = do_encrypt(request.encryption, request.data)  # 数据加密：MD5 ｏｒ　ｓｈａ１
        logger.my_log(f"请求 body --> {request.data}", "info")

    return request


@hooks.before_request
def update_expected(request):
    """更新预期结果"""
    request.expected = dep_par.replace_dependent_parameter(request.expected)
    logger.my_log(f"预期结果 --> {request.expected}", "info")

    return request


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
