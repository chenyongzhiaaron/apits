import json
import sys
import time
import unittest

from ddt import ddt, data

sys.path.append("../../../")
sys.path.append("../../common")
from common.config import Config

from common.file_handling.get_excel_init import get_init
from common.data_extraction.dependent_parameter import DependentParameter
from common.data_extraction.data_extractor import DataExtractor
from common.crypto.encryption_main import do_encrypt
from common.database.mysql_client import MysqlClient
from common.utils.http_client import http_client
from common.utils.mylogger import MyLogger
from common.validation import loaders
from common.dependence import Dependence as dep
from common.validation.validator import Validator
from common import bif_functions
from common.utils.load_and_execute_script import load_and_execute_script

test_file = Config.test_api  # 获取 excel 文件路径
excel_handle, init_data, test_case = get_init(test_file)
databases = init_data.get('databases')  # 获取数据库配置信息
mysql = MysqlClient(databases)  # 初始化 mysql 链接
dep.set_dep(eval(init_data.get("initialize_data")))  # 初始化依赖表
dep_par = DependentParameter()  # 参数提取类实例化
log = MyLogger()
host = init_data.get('host', "") + init_data.get("path", "")