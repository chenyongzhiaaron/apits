import sys
import time
import unittest

from ddt import ddt, data

from common.config import Config

sys.path.append("../../")
sys.path.append("../../common")
from common.file_handling.get_excel_init import get_init
from common.data_extraction.dependent_parameter import DependentParameter
from common.data_extraction.data_extractor import DataExtractor
from common.crypto.encryption_main import do_encrypt
from common.database.do_mysql import DoMysql
from common.utils.http_client import http_client
from common.utils.logger import MyLog
from common.validation import loaders
from common.dependence import Dependence as dep
from common.validation.validator import Validator
from common import bif_functions

test_file = Config.test_api  # 获取 excel 文件路径
excel_handle, init_data, test_case = get_init(test_file)
databases = init_data.get('databases')  # 获取数据库配置信息
mysql = DoMysql(databases)  # 初始化 mysql 链接
dep.set_dep(eval(init_data.get("initialize_data")))  # 初始化依赖表
dep_par = DependentParameter()  # 参数提取类实例化
logger = MyLog()
host = init_data.get('host', "") + init_data.get("path", "")


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        logger.my_log("开始加载内置方法...", "info")
        loaders.set_bif_fun(bif_functions)  # 加载内置方法
        logger.my_log("内置方法加载完成", "info")
        logger.my_log(f"所有用例执行开始...", "info")

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # f"""用例描述：{item.get("name")}_{item.get("desc")}"""
        sheet = item.get("sheet")
        item_id = item.get("Id")
        name = item.get("name")
        description = item.get("description")
        url = item.get("Url")
        request_data_type = item.get("request_data_type", "params")  # excel 不填写，默认为get请求的传参
        method = item.get("Method")
        sql_variable = item.get("sql变量")
        sqlps = item.get("SQL")
        item_headers = item.get("Headers", {})
        request_data = item.get("Request Data", {})
        parameters_key = item.get("提取请求参数")
        is_request_data_encryption = item.get("请求参数是否加密")
        is_headers_encryption = item.get("Headers是否加密")
        regex = item.get("正则表达式")
        keys = item.get("正则变量")
        deps = item.get("绝对路径表达式")
        jp_dict = item.get("Jsonpath")
        expect = item.get("预期结果")
        if not item.get("Run") or item.get("Run").upper() != "YES":
            logger.my_log(f"测试用例:{item.pop('Id')} 不执行，跳过!!!")
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
        try:
            execute_sql_results = mysql.execute_sql(sql)
            logger.my_log(f'sql 执行成功:{execute_sql_results}', "info")
            if execute_sql_results and sql_variable:
                # 执行sql数据提取
                DataExtractor(execute_sql_results).substitute_data(jp_dict=sql_variable)
                logger.my_log(f'sql 提取成功', "info")
                if method == "SQL" and mysql:
                    return
        except Exception as e:
            logger.my_log(f'执行 sql 失败:{sql},异常信息:{e}')
            raise e

        # 替换 URL, PARAMETERS, HEADER,期望值
        url = dep_par.replace_dependent_parameter(url)
        request_data = dep_par.replace_dependent_parameter(request_data)
        headers = dep_par.replace_dependent_parameter(item_headers)
        expected = dep_par.replace_dependent_parameter(expect)

        # 提取请求参数信息
        DataExtractor(request_data).substitute_data(jp_dict=parameters_key)
        # 判断是否执行加密
        if is_headers_encryption:
            headers = do_encrypt(is_headers_encryption, headers)  # 请求头参数加密:md5,sha1,sha256...

        if is_request_data_encryption:
            request_data = do_encrypt(is_request_data_encryption, request_data)  # 请求参数加密:md5,sha1,sha256...
        logger.my_log(f"当前用例所在的 sheet --> {sheet}", "info")
        logger.my_log(f"执行 SQL 语句 --> {sql}", "info")
        logger.my_log(f"预期结果 --> {expected}", "info")
        try:
            # 执行请求操作
            kwargs = {
                request_data_type: request_data,
                'headers': headers
            }
            response = http_client(host, url, method, **kwargs)
            logger.my_log(f"请求地址 --> {response.request.url}", "info")
            logger.my_log(f"请求头 --> {response.request.headers}", "info")
            logger.my_log(f"请求 body --> {response.request.body}", "info")
            logger.my_log(f"接口状态--> {response.status_code}", "info")
            logger.my_log(f"接口耗时--> {response.elapsed}", "info")
            logger.my_log(f"接口响应--> {response.text}", "info")
        except Exception as e:
            result = "失败"
            logger.my_log(f'用例id:{item_id}-->{name}_{description},异常:{e}')
            raise e

        result_tuple = Validator().run_validate(expected, response.json())  # 执行断言 返回结果元组
        result = "PASS"
        try:

            self.assertNotIn("FAIL", result_tuple, "FAIL 存在结果元组中")
        except Exception as e:
            result = "FAIL"
            raise e
        finally:
            # pass
            # 响应结果及测试结果回写 excel
            excel_handle.write_back(
                sheet_name=sheet,
                i=item_id,
                response_value=response.text,
                test_result=result,
                assert_log=str(result_tuple)
            )
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

    @classmethod
    def tearDownClass(cls) -> None:
        logger.my_log(f"所有用例执行完毕")


if __name__ == '__main__':
    unittest.main()
