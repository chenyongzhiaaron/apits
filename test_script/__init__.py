import sys

sys.path.append("../../")
sys.path.append("../common")

from common.config import Config
from common.validation.validator import Validator

from common.data_extraction.data_extractor import DataExtractor

from common.file_handling.do_excel import DoExcel
from common.data_extraction.dependent_parameter import DependentParameter
from common.database.mysql_client import MysqlClient
from common.utils.mylogger import MyLogger
from common.dependence import Dependence

test_file = Config.test_api  # 获取 excel 文件路径
excel = DoExcel(test_file)
init_data, test_case = excel.get_excel_init_and_cases()

databases = init_data.get('databases')  # 获取数据库配置信息
mysql = MysqlClient(databases)  # 初始化 mysql 链接

Dependence.set_dep(eval(init_data.get("initialize_data")))  # 初始化依赖表
host = init_data.get('host', "") + init_data.get("path", "")

validator = Validator()
dep_par = DependentParameter()  # 参数提取类实例化
logger = MyLogger()
