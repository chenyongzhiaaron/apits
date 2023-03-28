import sys
import time
import unittest
import traceback
import warnings
from rich import print

from ddt import ddt, data

sys.path.append("../../")
sys.path.append("../../common")
from common.extractor.assert_dict import AssertDict
from common.extractor.do_jsonpath import get_data
from common.dependence import Dependence
from common.extractor.dependent_parameter import DependentParameter
from common.encryption.do_encryption import do_encrypt
from common.do_sql.do_mysql import DoMysql
from common.extractor.data_extractor import DataExtractor
from common.tools.req import req
from common.tools.logger import MyLog
from common.comparator.loaders import load_built_in_functions
from common.dependence import Dependence
from .login import login
from .get_init import get_init

warnings.simplefilter('ignore', ResourceWarning)

excel_handle, init_data, test_case = get_init()
databases = init_data.get('databases')  # 获取数据库配置信息

mysql = DoMysql(databases)  # 初始化 mysql 链接

dep = Dependence()  # 实例化依赖


@ddt
class TestProjectApi(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        # 获取初始化基础数据

        setattr(Dependence, 'dependence', eval(init_data.get('initialize_data')))
        # dependence = getattr(Dependence, "dependence")
        headers = login(init_data.get("host"), init_data.get("account"), init_data.get("password"))
        # dependence["headers"] = headers
        dep.update_dependence("headers", headers)
        # setattr(Dependence, "dependence", dependence)
        # 加载内置方法
        for k, v in load_built_in_functions().items():
            # dependence[k] = v
            dep.update_dependence(k, v)
        # setattr(Dependence, "dependence", dependence)

        print(dep.get_dependence())

    def setUp(self) -> None:
        pass
        # dependence = getattr(Params, "dependence")
        # # r_tools = load_built_in_functions()
        # # for k, v in load_built_in_functions().items():
        # #     dependence[k] = v
        # # setattr(Params, "dependence", dependence)
        # print(dependence)

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        # self.assertIsNotNone(item.get("Id"), msg="用例 id 不能为空")
        test_result = None
        if item.get("Run").upper() == "YES":
            return
        if item.get("Method") == "TIME":
            try:
                time.sleep(int(item.get("Url")))
            except Exception as e:
                MyLog().my_log(f'序号:{item.get("Id")},暂停时间必须是数字')
                raise e
        # 首先执行sql替换,将sql替换为正确的sql语句
        sql = DependentParameter().replace_dependent_parameter(item.get("SQL"))
        print("执行sql替换：", sql)
        if item.get("Method") == "SQL":
            try:
                execute_sql_results = mysql.do_mysql(sql)
                if execute_sql_results and item.get("sql变量"):
                    DataExtractor(execute_sql_results).substitute_data(jp_dict=item.get("sql变量"))
            except Exception as e:
                MyLog().my_log(f'序号:{item.get("Id")},sql_file:{sql},异常:{traceback.format_exc()}')
                raise e

        if item.get("SQL"):
            # 执行 sql_file 操作
            sql_res = mysql.do_mysql(sql)
            # 将关联结果存入关联字典
            DataExtractor.substitute_data(item.get("Regular"), item.get("Regular Key"), sql_res,
                                          jp_dict=item.get("sql变量"))
        # 替换 URL, REQUEST, HEADER,期望值
        url = DataExtractor.do_regex(item.get("Url"))
        request_data = DataExtractor.do_regex(item.get("Request Data"))
        if item.get("Headers") is not None:
            headers = {**getattr(Dependence, "dependence").get("headers"), **eval(item.get("Headers"))}
        else:
            headers = getattr(Dependence, "dependence").get("headers")
        # 提取请求参数信息
        DataExtractor().substitute_data("", request_data, item.get("Request Tmp"), item.get("Id"))
        # 执行参数替换
        expected = DataExtractor.do_regex(item.get("ExpectedResult"))
        # 判断是否执行加密
        if item.get("Encryption"):
            request_data = do_encrypt(item.get("Encryption"), request_data)  # 数据加密：MD5 ｏｒ　ｓｈａ１
        # 执行请求操作
        try:
            res = req(init_data.get("host"), item.get("Method"), url, data=request_data, headers=headers)
        except Exception as e:
            MyLog().my_log(f'{item.get("Id")}-->{item.get("description")},异常:{e}')
            raise e
        else:
            try:
                result = res.json()
                print("--URL-- ", url)
                print("--HEADER-- ", headers)
                print("--BODY-- ", request_data)
                print("--RESPONSE-- ", result)
                # pprint(url, indent=2, width=300)
                # pprint(headers, indent=2, width=300)
                # pprint(request_data, indent=2, width=200)
                # pprint(sql, indent=2, width=300)
                # pprint(expected, indent=2, width=200)
                # pprint(result, indent=2, width=300)
            except Exception as e:
                MyLog().my_log(f"序号:{item.get('Id')},用例:{item.get('description')},无法 res.json()")
                raise e
        try:
            if not expected:
                self.assertEqual(res.status_code, 200, msg="返回的http_code != 200")
        except Exception as e:
            # excel_handle.write_back(item["sheet_name"], item["Id"], str(res.text), test_result, e)
            raise e
        # 提取响应
        try:
            DataExtractor.substitute_data(item["Regular"], item["Regular Key"], result,
                                          item["Correlation"], item["Id"], item["Jsonpath"])
        except Exception as e:
            MyLog().my_log(f"序号:{item['Id']},用例:{item['description']},提取响应失败")
            raise e
        try:
            if expected != "None" and expected is not None:
                if item.get("assert type") == "相等":
                    expected_res = get_data(result, expected[1])
                    self.assertEqual(expected[0], expected_res)
                else:
                    AssertDict().is_contain(expected, result)
                test_result = "通过"
        except Exception as e:
            test_result = "不通过"
            MyLog().my_log(f"\n\n序号:{item.get('Id')},用例:{item.get('description')},信息:{e}")
            raise e
        finally:
            print("--断言结果-- ", test_result)
            # 响应结果及测试结果回写 excel
            # excel_handle.write_back(item["sheet_name"], item["Id"], str(res.text), test_result, e)


if __name__ == '__main__':
    unittest.main()
