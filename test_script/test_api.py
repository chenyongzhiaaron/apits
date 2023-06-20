import time
import unittest

from ddt import ddt, data

from common import bif_functions
from common.crypto.encrypt_data import encrypt_data
from common.http_client.http_client import http_client
from common.utils.load_and_execute_script import load_and_execute_script
from common.validation import loaders
from test_script import *


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None
    extractor = DataExtractor()

    @classmethod
    def setUpClass(cls) -> None:
        loaders.set_bif_fun(bif_functions)  # 加载内置方法

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # f"""用例描述：{item.get("name")}_{item.get("desc")}"""
        sheet = item.pop("sheet")
        item_id = item.pop("Id")
        name = item.pop("Name")
        description = item.pop("Description")
        sleep_time = item.pop("Time")
        # 不填写，默认为get请求的传参
        request_data_type = item.pop("Request Data Type") if item.get("Request Data Type") else 'params'
        method = item.pop("Method")
        sql_params_dict = item.pop("Sql Params Dict")
        sqlps = item.pop("SQL")
        parameters_key = item.pop("Extract Request Data")
        request_data_crypto = item.pop("Request Data Crypto")
        headers_crypto = item.pop("Headers Crypto")
        regex = item.pop("Regex")
        regex_params_list = item.pop("Regex Params List")
        retrieve_value = item.pop("Retrieve Value")
        json_path = item.pop("Jsonpath")
        is_run = item.pop("Run")
        if not is_run or is_run.upper() != "YES":
            return
        self.pause_execution(sleep_time)

        # 首先执行sql替换,将sql替换为正确的sql语句
        sql = dep_par.replace_dependent_parameter(sqlps)
        if sql:
            try:
                execute_sql_results = mysql.do_mysql(sql)
                if execute_sql_results and sql_params_dict:
                    # 执行sql数据提取
                    self.extractor.substitute_data(execute_sql_results, jp_dict=sql_params_dict)
                    if method == "SQL" and mysql:
                        return
            except Exception as e:
                logger.error(f'执行 sql 失败:{sql},异常信息:{e}')
                raise e

        # 拼接动态代码段文件
        prepost_script = f"prepost_script_{sheet}_{item_id}.py"

        item = load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "setup", item)

        # 替换 URL, PARAMETERS, HEADER,期望值
        item = dep_par.replace_dependent_parameter(item)
        url = item.pop("Url")
        request_data = item.pop("Request Data")
        headers = item.pop("Headers")
        expected = item.pop("Expected")
        # 提取请求参数信息
        self.extractor.substitute_data(request_data, jp_dict=parameters_key)

        headers, request_data = encrypt_data(headers_crypto, headers, request_data_crypto, request_data)

        result_tuple = None
        result = "PASS"
        response = None

        try:
            # 执行请求操作
            kwargs = {
                request_data_type: request_data,
                'headers': headers
            }
            response = http_client(host, url, method, **kwargs)
            # 执行后置代码片段
            load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "teardown", response)

            result_tuple = validator.run_validate(expected, response.json())  # 执行断言 返回结果元组
            self.assertNotIn("FAIL", result_tuple, "FAIL 存在结果元组中")
            try:
                # 提取响应
                self.extractor.substitute_data(response.json(), regex=regex, keys=regex_params_list,
                                               deps=retrieve_value,
                                               jp_dict=json_path)

            except Exception as err:
                logger.error(f"提取响应失败：{sheet}_{item_id}_{name}_{description}"
                             f"\nregex={regex};"
                             f" \nkeys={regex_params_list};"
                             f"\ndeps={retrieve_value};"
                             f"\njp_dict={json_path}"
                             f"\n{err}")
        except Exception as e:
            result = "FAIL"
            logger.error(f'异常用例: {sheet}_{item_id}_{name}_{description}\n{e}')
            raise e
        finally:
            response_value = response.text if response is not None else str(response)
            assert_log = str(result_tuple)
            # 响应结果及测试结果回写 excel
            # excel.write_back(sheet_name=sheet, i=item_id, response=response_value, test_result=result,
            #                         assert_log=assert_log)

    def pause_execution(self, sleep_time):
        if sleep_time:
            try:
                time.sleep(sleep_time)
            except Exception as e:
                logger.error("暂时时间必须是数字")
                raise e

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info(f"所有用例执行完毕")


if __name__ == '__main__':
    unittest.main()
