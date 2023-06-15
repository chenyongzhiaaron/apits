import json
import sys
import time
import unittest

from ddt import ddt, data
#
# sys.path.append("../../../")
# sys.path.append("../../common")
# from common.config import Config
#
# from common.file_handling.get_excel_init import get_init
# from common.data_extraction.dependent_parameter import DependentParameter
# from common.data_extraction.data_extractor import DataExtractor
# from common.crypto.encryption_main import do_encrypt
# from common.database.mysql_client import MysqlClient
# from common.utils.http_client import http_client
# from common.utils.mylogger import MyLogger
# from common.validation import loaders
# from common.dependence import Dependence as dep
# from common.validation.validator import Validator
# from common import bif_functions
# from common.utils.load_and_execute_script import load_and_execute_script
#
# test_file = Config.test_api  # 获取 excel 文件路径
# excel_handle, init_data, test_case = get_init(test_file)
# databases = init_data.get('databases')  # 获取数据库配置信息
# mysql = MysqlClient(databases)  # 初始化 mysql 链接
# dep.set_dep(eval(init_data.get("initialize_data")))  # 初始化依赖表
# dep_par = DependentParameter()  # 参数提取类实例化
# log = MyLogger()
# host = init_data.get('host', "") + init_data.get("path", "")

from test_script.automation import bif_functions
from test_script.automation import host
from test_script.automation import test_case,log,dep_par,dep,mysql,loaders


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        log.info("开始加载内置方法...")
        loaders.set_bif_fun(bif_functions)  # 加载内置方法
        log.info("内置方法加载完成")
        log.info(f"所有用例执行开始...")

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # f"""用例描述：{item.get("name")}_{item.get("desc")}"""
        sheet = item.pop("sheet")
        item_id = item.pop("Id")
        name = item.pop("name")
        description = item.pop("description")
        sleep_time = item.get("Time")
        request_data_type = item.pop("request_data_type", "params")  # excel 不填写，默认为get请求的传参
        method = item.pop("Method")
        sql_variable = item.pop("sql变量")
        sqlps = item.pop("SQL")
        parameters_key = item.pop("提取请求参数")
        is_request_data_encryption = item.pop("请求参数是否加密")
        is_headers_encryption = item.pop("Headers是否加密")
        regex = item.pop("正则表达式")
        keys = item.pop("正则变量")
        deps = item.pop("绝对路径表达式")
        jp_dict = item.pop("Jsonpath")

        if not item.get("Run") or item.get("Run").upper() != "YES":
            log.info(f"测试用例:{item_id} 不执行，跳过!!!")
            return

        if sleep_time:
            try:
                time.sleep(int(sleep_time))
                log.info(f"暂停:{sleep_time}")
            except Exception as e:
                log.info(f'暂停时间必须是数字')
                raise e

        # 首先执行sql替换,将sql替换为正确的sql语句
        sql = dep_par.replace_dependent_parameter(sqlps)

        try:
            execute_sql_results = mysql.execute_sql(sql)
            log.info(f'sql 执行成功:{execute_sql_results}')
            if execute_sql_results and sql_variable:
                # 执行sql数据提取
                DataExtractor(execute_sql_results).substitute_data(jp_dict=sql_variable)
                log.info('sql 提取成功')
                if method == "SQL" and mysql:
                    return
        except Exception as e:
            log.error(f'执行 sql 失败:{sql},异常信息:{e}')
            raise e

        # 拼接动态代码段文件
        prepost_script = f"prepost_script_{sheet}_{item_id}.py"
        item = load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "setup", item)
        print(f"前置脚本后的:{item}")
        # 替换 URL, PARAMETERS, HEADER,期望值
        item = dep_par.replace_dependent_parameter(item)
        print(f"参数替换后:{item}")
        url = item.pop("Url")
        request_data = item.pop("Request Data", {})
        headers = item.pop("Headers", {})
        expected = item.pop("预期结果")

        # 提取请求参数信息
        DataExtractor(request_data).substitute_data(jp_dict=parameters_key)

        # 判断是否执行加密
        if is_headers_encryption:
            headers = do_encrypt(is_headers_encryption, headers)  # 请求头参数加密:md5,sha1,sha256...

        if is_request_data_encryption:
            request_data = do_encrypt(is_request_data_encryption, request_data)  # 请求参数加密:md5,sha1,sha256...

        result_tuple = None
        result = "PASS"
        response = None

        try:
            kwargs = {
                request_data_type: json.loads(request_data) if request_data is not None else {},
                'headers': json.loads(headers) if headers is not None else {}
            }
            response = http_client(host, url, method, **kwargs)
            result_tuple = Validator().run_validate(expected, response.json())  # 执行断言 返回结果元组
            self.assertNotIn("FAIL", result_tuple, "FAIL 存在结果元组中")
            # 执行后置代码片段
            load_and_execute_script(Config.SCRIPTS_DIR, prepost_script, "teardown", response)
            try:
                # 提取响应
                DataExtractor(response.json()).substitute_data(regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
            except Exception as err:
                log.error(f"提取响应失败：{sheet}_{item_id}_{name}_{description}"
                          f"\nregex={regex};"
                          f" \nkeys={keys};"
                          f"\ndeps={deps};"
                          f"\njp_dict={jp_dict}"
                          f"\n{err}")
        except Exception as e:
            result = "FAIL"
            log.error(f'异常用例: {sheet}_{item_id}_{name}_{description}\n{e}')
            raise e
        finally:
            response_value = response.text if response is not None else str(response)
            assert_log = str(result_tuple)
            # 响应结果及测试结果回写 excel
            excel_handle.write_back(sheet_name=sheet, i=item_id, response_value=response_value, test_result=result,
                                    assert_log=assert_log)

    @classmethod
    def tearDownClass(cls) -> None:
        log.info(f"所有用例执行完毕")


if __name__ == '__main__':
    unittest.main()
