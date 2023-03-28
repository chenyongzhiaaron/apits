import sys
import time
import unittest
import warnings
from rich import print

from ddt import ddt, data

sys.path.append("../../")
sys.path.append("../../common")
from .login import login
from .get_init import get_init
from common.extractor.dependent_parameter import DependentParameter
from common.extractor.data_extractor import DataExtractor
from common.encryption.do_encryption import do_encrypt
from common.do_sql.do_mysql import DoMysql
from common.tools.req import req
from common.tools.logger import MyLog
from common.comparator.loaders import load_built_in_functions
from common.dependence import Dependence
from common.comparator.validator import Validator

warnings.simplefilter('ignore', ResourceWarning)

excel_handle, init_data, test_case = get_init()
databases = init_data.get('databases')  # 获取数据库配置信息
mysql = DoMysql(databases)  # 初始化 mysql 链接
dep = Dependence()  # 依赖表实例化
setattr(Dependence, "dependence", eval(init_data.get("initialize_data")))  # 初始化依赖表
# dep.set_dep(eval(init_data.get("initialize_data")))  # 初始化依赖表
print("--------------------->", getattr(Dependence, "dependence"))
deper = DependentParameter()  # 参数提取类实例化
logger = MyLog()

validator = Validator() \
 \
            @ ddt


class TestProjectApi(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        # 获取初始化基础数据
        cls.host = init_data.get('host')
        cls.path = init_data.get("path")
        username = dep.get_dep("{{account}}")
        password = dep.get_dep("{{password}}")
        cls.headers = login(cls.host + cls.path, username, password)
        dep.update_dep("headers", cls.headers)
        # 加载内置方法
        for k, v in load_built_in_functions().items():
            dep.update_dep(k, v)
        print(dep.get_dep())

    def setUp(self) -> None:
        logger.my_log("-----------------------------------start_test_api-----------------------------------", "info")

    @logger.decorator_log()
    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # print(self.host, self.headers)
        sheet = item.get("sheet_name")
        item_id = item.get("Id")
        name = item.get("name")
        description = item.get("description")
        host = self.host
        path = self.path
        headers = self.headers
        url = item.get("url")
        run = item.get("Run")
        print("123111", run)
        method = item.get("Method")
        sql_variable = item.get("sql变量")
        sqlps = item.get("SQL")
        item_headers = item.get("Headers") if item.get("Headers") else {}
        parameters = item.get("请求参数")
        parameters_key = item.get("提取请求参数")
        encryption = item.get("参数加密方式")
        regex = item.get("正则表达式")
        keys = item.get("正则变量")
        deps = item.get("绝对路径表达式")
        jp_dict = item.get("Jsonpath")
        sql_key = item.get("sql变量")
        expect = item.get("预期结果")
        if run.upper() != "YES":
            return
        if method == "TIME":
            try:
                time.sleep(int(url))
                return
            except Exception as e:
                MyLog().my_log(f'暂停时间必须是数字')
                raise e
        # 首先执行sql替换,将sql替换为正确的sql语句
        sql = deper.replace_dependent_parameter(sqlps)
        print("2334241234", sql)
        if method == "SQL":
            try:
                execute_sql_results = mysql.do_mysql(sql)
                if execute_sql_results and sql_variable:
                    # 执行sql数据提取
                    DataExtractor(execute_sql_results).substitute_data(jp_dict=sql_variable)
            except Exception as e:
                logger.my_log(f'sql:{sql},异常:{e}')
                raise e

        # 执行 sql 操作
        sql_res = mysql.do_mysql(sql)
        # 执行sql数据提取
        DataExtractor(sql_res).substitute_data(jp_dict=sql_key)
        # 替换 URL, PARAMETERS, HEADER,期望值
        url = deper.replace_dependent_parameter(url)
        parameters = deper.replace_dependent_parameter(parameters)
        item_headers = deper.replace_dependent_parameter(item_headers)
        headers = {**headers, **item_headers}
        expected = deper.replace_dependent_parameter(expect)
        # 提取请求参数信息
        DataExtractor(parameters).substitute_data(deps=parameters_key)
        # 执行参数替换
        # 替换预期结果
        # 判断是否执行加密
        if encryption:
            parameters = do_encrypt(encryption, parameters)  # 数据加密：MD5 ｏｒ　ｓｈａ１
        try:
            print("--URL-- ", url)
            print("--HEADER-- ", headers)
            print("--BODY-- ", parameters)
            print("--SQL--", sql)
            print("--SQL_RESULT--", sql_res)
            # 执行请求操作
            host = host + path
            response = req(host, method, url, data=parameters, headers=headers)
            # pprint(url, indent=2, width=300)
            # pprint(headers, indent=2, width=300)
            print("--RESPONSE-- ", response.text)
            print("--EXPECTED-- ", expected)
        except Exception as e:
            logger.my_log(f'{item_id}-->{name}_{description},异常:{e}')
            # excel_handle.write_back(sheet, item_id, response.text, result)
            raise e
        # 执行断言
        result_tuple = validator.run_validate(expected, response.json())  # 返回结果元组
        if "FAIL" in result_tuple:
            result = "失败"
            excel_handle.write_back(sheet, item_id, response.text, result)
        else:
            result = "通过"
            # 响应结果及测试结果回写 excel
            excel_handle.write_back(sheet, item_id, response.text, result)
            raise result_tuple
        try:
            # 提取响应
            DataExtractor(response.json()).substitute_data(regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
        except:
            logger.my_log(
                f"提取响应失败：{name}_{description}:regex={regex}, keys={keys}, deps={deps}, jp_dict={jp_dict}")

    def tearDown(self) -> None:
        logger.my_log("-----------------------------------end_test_api-----------------------------------", "info")


if __name__ == '__main__':
    unittest.main()
