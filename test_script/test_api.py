import time
import unittest

from ddt import ddt, data

from common import bif_functions
from common.action import Action
from common.config import Config
from common.database.mysql_client import MysqlClient
from common.file_handling.do_excel import DoExcel
from common.utils.mylogger import MyLogger

test_file = Config.test_api  # 获取 excel 文件路径
excel = DoExcel(test_file)
init_data, test_case = excel.get_excel_init_and_cases()

databases = init_data.get('databases')  # 获取数据库配置信息
mysql = MysqlClient(databases)  # 初始化 mysql 链接

logger = MyLogger()
initialize_data = eval(init_data.get("initialize_data"))
host = init_data.get('host', "") + init_data.get("path", "")


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None
    action = Action()

    @classmethod
    def setUpClass(cls) -> None:
        cls.action.set_variable(initialize_data)  # 加载初始化数据
        cls.action.set_bif_fun(bif_functions)  # 加载内置方法

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # f"""用例描述：{item.get("name")}_{item.get("desc")}"""
        # 不填写，默认为get请求的传参
        request_data_type = item.pop("Request Data Type") if item.get("Request Data Type") else 'params'
        sql_params_dict = item.pop("Sql Params Dict")
        sqlps = item.pop("SQL")

        sheet, item_id, condition, st, name, desc, headers_crypto, request_crypto, method = self.__base_info(item)
        regex, keys, deps, jp_dict, extract_request_data = self.__extractor_info(item)

        if self.is_run(condition):
            return

        self.pause_execution(st)

        # 首先执行sql替换,将sql替换为正确的sql语句
        sql = self.action.replace_dependent_parameter(sqlps)
        if sql:
            try:
                execute_sql_results = mysql.do_mysql(sql)
                if execute_sql_results and sql_params_dict:
                    # 执行sql数据提取
                    self.action.substitute_data(execute_sql_results, jp_dict=sql_params_dict)
                    # self.extractor.substitute_data(execute_sql_results, jp_dict=sql_params_dict)
                    if method == "SQL" and mysql:
                        return
            except Exception as e:
                logger.error(f'执行 sql 失败:{sql},异常信息:{e}')
                raise e

        # 拼接动态代码段文件
        prepost_script = f"prepost_script_{sheet}_{item_id}.py"

        item = self.action.load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "setup", item)

        # 替换 URL, PARAMETERS, HEADER,期望值
        item = self.action.replace_dependent_parameter(item)
        url = item.pop("Url")
        request_data = item.pop("Request Data")
        headers = item.pop("Headers")
        expected = item.pop("Expected")
        # 提取请求参数信息
        self.action.substitute_data(request_data, jp_dict=jp_dict)

        headers, request_data = self.action.encrypt_data.encrypt_data(headers_crypto, headers, request_crypto,
                                                                      request_data)

        result_tuple = None
        result = "PASS"
        response = None

        try:
            # 执行请求操作
            kwargs = {
                request_data_type: request_data,
                'headers': headers
            }
            response = self.action.http_client(host, url, method, **kwargs)
            # 执行后置代码片段
            self.action.load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "teardown", response)

            result_tuple = self.action.run_validate(expected, response.json())  # 执行断言 返回结果元组
            self.assertNotIn("FAIL", result_tuple, "FAIL 存在结果元组中")
            try:
                # 提取响应
                self.action.substitute_data(response.json(), regex=regex, keys=keys,
                                            deps=deps, jp_dict=jp_dict)

            except Exception as err:
                logger.error(f"提取响应失败：{sheet}_{item_id}_{name}_{desc}"
                             f"\nregex={regex};"
                             f" \nkeys={keys};"
                             f"\ndeps={deps};"
                             f"\njp_dict={jp_dict}"
                             f"\n{err}")
        except Exception as e:
            result = "FAIL"
            logger.error(f'异常用例: {sheet}_{item_id}_{name}_{desc}\n{e}')
            raise e
        finally:
            response_value = response.text if response is not None else str(response)
            assert_log = str(result_tuple)
            # 响应结果及测试结果回写 excel
            # excel.write_back(sheet_name=sheet, i=item_id, response=response_value, test_result=result,
            #                         assert_log=assert_log)

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"所有用例执行完毕")

    @staticmethod
    def __base_info(item):
        """
        获取基础信息
        Args:
            item:

        Returns:

        """
        sheet = item.pop("sheet")
        item_id = item.pop("Id")
        condition = item.pop("Run")
        sleep_time = item.pop("Time")
        name = item.pop("Name")
        desc = item.pop("Description")
        headers_crypto = item.pop("Headers Crypto")
        request_data_crypto = item.pop("Request Data Crypto")
        method = item.pop("Method")
        return sheet, item_id, condition, sleep_time, name, desc, headers_crypto, request_data_crypto, method

    @staticmethod
    def __extractor_info(item):
        """
        获取提取参数的基本字段信息
        Args:
            item:

        Returns:

        """
        regex = item.pop("Regex")
        keys = item.pop("Regex Params List")
        deps = item.pop("Retrieve Value")
        jp_dict = item.pop("Jsonpath")
        extract_request_data = item.pop("Extract Request Data")
        return regex, keys, deps, jp_dict, extract_request_data

    @staticmethod
    def __request_info(item):
        url = item.pop("Url")
        query_str = item.pop("Query Str")
        request_data = item.pop("Request Data")
        headers = item.pop("Headers")
        expected = item.pop("Expected")
        request_data_type = item.pop("Request Data Type") if item.get("Request Data Type") else 'params'
        return url, query_str, request_data_type, request_data, headers, expected

    @staticmethod
    def is_run(condition):
        is_run = condition
        if not is_run or is_run.upper() != "YES":
            return True

    @staticmethod
    def pause_execution(sleep_time):
        if sleep_time:
            try:
                time.sleep(sleep_time)
            except Exception as e:
                logger.error("暂时时间必须是数字")
                raise e


if __name__ == '__main__':
    unittest.main()
