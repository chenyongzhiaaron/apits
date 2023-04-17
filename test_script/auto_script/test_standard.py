import sys
import time
import unittest
import warnings

from ddt import ddt, data

from common.base_datas import BaseDates

sys.path.append("../../")
sys.path.append("../../common")
from test_script.auto_script.login import login
from common.files_tools.get_excel_init import get_init
from common.extractor.dependent_parameter import DependentParameter
from common.extractor.data_extractor import DataExtractor
from common.encryption.encryption_main import do_encrypt
from common.do_sql.do_mysql import DoMysql
from common.tools.req import req
from common.tools.logger import MyLog
from common.comparator import loaders
from common.dependence import Dependence
from common.comparator.validator import Validator
from common import bif_functions

warnings.simplefilter('ignore', ResourceWarning)

test_file = BaseDates.test_api  # 获取 excel 文件路径
excel_handle, init_data, test_case = get_init(test_file)
databases = init_data.get('databases')  # 获取数据库配置信息
mysql = DoMysql(databases)  # 初始化 mysql 链接
dep = Dependence
dep.set_dep(eval(init_data.get("initialize_data")))  # 初始化依赖表
dep_par = DependentParameter()  # 参数提取类实例化
logger = MyLog()


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        loaders.set_bif_fun(bif_functions)  # 加载内置方法
        # 获取初始化基础数据
        cls.host = init_data.get('host')
        cls.path = init_data.get("path")
        username = dep.get_dep("{{account}}")
        password = dep.get_dep("{{passwd}}")
        cls.headers = login(cls.host + cls.path, username, password)
        dep.update_dep("headers", cls.headers)
        # 加载内置方法
        logger.my_log(f"内置方法：{dep.get_dep()}", "info")

    def setUp(self) -> None:
        logger.my_log(f"获取当前依赖参数表：{dep.get_dep()}")
        logger.my_log("-----------------------------------start_test_api-----------------------------------", "info")

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # f"""用例描述：{item.get("name")}_{item.get("desc")}"""
        sheet = item.get("sheet")
        item_id = item.get("Id")
        name = item.get("name")
        description = item.get("description")
        host = self.__class__.host
        path = self.__class__.path
        url = item.get("Url")
        headers = self.__class__.headers
        print("---------》", headers)
        run = item.get("Run")
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
                logger.my_log(f"暂存成功:{url}", "info")
                return
            except Exception as e:
                MyLog().my_log(f'暂停时间必须是数字')
                raise e
        # 首先执行sql替换,将sql替换为正确的sql语句
        sql = dep_par.replace_dependent_parameter(sqlps)
        if method == "SQL" and mysql:
            try:
                execute_sql_results = mysql.do_mysql(sql)
                logger.my_log(f'sql执行成功:{execute_sql_results}', "info")
                if execute_sql_results and sql_variable:
                    # 执行sql数据提取
                    DataExtractor(execute_sql_results).substitute_data(jp_dict=sql_variable)
                    logger.my_log(f'sql 提取成功', "info")
                    return
            except Exception as e:
                logger.my_log(f'sql:{sql},异常:{e}')
                raise e

        try:
            # 执行 sql 操作
            sql_res = mysql.do_mysql(sql)
            # 执行sql数据提取
            DataExtractor(sql_res).substitute_data(jp_dict=sql_key)
        except:
            sql_res = "想啥呢？数据库都没有配置还想执行数据库操作？"
            logger.my_log(sql_res)
        # 替换 URL, PARAMETERS, HEADER,期望值
        url = dep_par.replace_dependent_parameter(url)
        parameters = dep_par.replace_dependent_parameter(parameters)
        item_headers = dep_par.replace_dependent_parameter(item_headers)
        headers = {**headers, **item_headers}
        expected = dep_par.replace_dependent_parameter(expect)
        # 提取请求参数信息
        DataExtractor(parameters).substitute_data(jp_dict=parameters_key)
        # 判断是否执行加密
        if encryption:
            parameters = do_encrypt(encryption, parameters)  # 数据加密：MD5 ｏｒ　ｓｈａ１
        logger.my_log(f"当前用例所在的sheet--> {sheet}", "info")
        logger.my_log(f"请求地址--> {host + path + url}", "info")
        logger.my_log(f"请求头--> {headers}", "info")
        logger.my_log(f"请求body--> {parameters}", "info")
        logger.my_log(f"执行SQL语句--> {sql}", "info")
        logger.my_log(f"执行sql结果--> {sql_res}", "info")
        logger.my_log(f"预期结果--> {expected}", "info")
        try:
            # 执行请求操作
            response = req(host + path, url, method, headers=headers, data=parameters)
            logger.my_log(f"接口响应--> {response.text}", "info")
            logger.my_log(f"接口耗时--> {response.elapsed}", "info")
        except Exception as e:
            result = "失败"
            logger.my_log(f'{result}:{item_id}-->{name}_{description},异常:{e}')
            raise e

        result_tuple = Validator().run_validate(expected, response.json())  # 执行断言 返回结果元组
        result = "PASS"
        try:
            self.assertNotIn("FAIL", result_tuple, "FAIL 存在结果元组中")
        except Exception as e:
            result = "FAIL"
            raise e
        finally:
            pass
            # 响应结果及测试结果回写 excel
            # excel_handle.write_back(
            #     sheet_name=sheet,
            #     i=item_id,
            #     response_value=response.text,
            #     test_result=result,
            #     assert_log=str(result_tuple)
            # )
        try:
            # 提取响应
            DataExtractor(response.json()).substitute_data(regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
        except:
            logger.my_log(
                f"提取响应失败：{name}_{description}:"
                f"\nregex={regex},"
                f" \nkeys={keys}, "
                f"\ndeps={deps}, "
                f"\njp_dict={jp_dict}")

    def tearDown(self) -> None:
        logger.my_log("-----------------------------------end_test_api-----------------------------------", "info")

    @classmethod
    def tearDownClass(cls) -> None:
        pass


if __name__ == '__main__':
    unittest.main()
