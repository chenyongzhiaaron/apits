import sys
import unittest

from ddt import ddt, data

sys.path.append("../")
sys.path.append("../../common")
from common.file_handling.get_excel_init import get_init
from common.utils.logger import MyLog
from common.dependence import Dependence
from common.config import BaseDates
from test_script.script.baseclass import BaseClass

test_file = BaseDates.test_api  # 获取 excel 文件路径
excel_handle, init_data, test_case = get_init(test_file)
logger = MyLog()
host = init_data.pop("host")
path = init_data.pop("path")
databases = init_data.pop('databases')  # 获取数据库配置信息
Dependence.set_dep(eval(init_data.pop("initialize_data")))  # 初始化依赖表


@ddt
class TestProjectApi(BaseClass):

    def __init__(self, *args):
        kwargs = {
            "host": host,
            "path": path,
            "databases": databases
        }
        super().__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    @data(*test_case)  # {"":""}
    def test_api(self, item):  # item = {測試用例}
        is_run = item.get("Run")
        if not is_run or is_run.upper() != "YES":
            logger.my_log(f"测试用例:{item.pop('Id')} 不执行，跳过!!!")
            return
        # 开始执行
        self.do_process(item)
        # 断言
        try:
            self.assertNotIn("FAIL", self.result_tuples, "FAIL 存在结果元组中")
            result = "PASS"
        except Exception as e:
            result = "FAIL"
            raise e
        finally:
            # 响应结果及测试结果回写 excel
            # excel_handle.write_back(
            #     sheet_name=sheet,
            #     i=item_id,
            #     response_value=response.text,
            #     test_result=result,
            #     assert_log=str(result_tuple)
            # )
            pass

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()


if __name__ == '__main__':
    unittest.main()
