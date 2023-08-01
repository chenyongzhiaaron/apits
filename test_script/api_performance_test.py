#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: api_performance_test.py
@time: 2023/7/26 11:50
@desc:
"""
import time

from locust import HttpUser, task, between

from common import bif_functions
from common.action import Action
from common.config import Config
from common.file_handling.do_excel import DoExcel
from common.log_utils.mylogger import MyLogger

# 初始化接口自动化测试框架的相关配置
test_file = Config.test_case
excel = DoExcel(test_file)
init_data, test_case = excel.get_excel_init_and_cases()
databases = init_data.get('databases')
initialize_data = eval(init_data.get("initialize_data"))
host = init_data.get('host', "") + init_data.get("path", "")
action = Action(initialize_data, bif_functions, databases)
logger = MyLogger()


class User(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_api(self):
        for item in test_case:
            sheet, iid, condition, st, name, desc, h_crypto, r_crypto, method, expected = self.__base_info(item)
            if self.__is_run(condition):
                continue
            
            regex, keys, deps, jp_dict, ex_request_data = self.__extractor_info(item)
            setup_script, teardown_script = self.script(item)
            
            # 首执行 sql
            self.__exc_sql(item)
            if method.upper() == 'SQL':
                continue
            
            # 执行动态代码
            item = action.execute_dynamic_code(item, setup_script)
            
            # 修正参数
            item = action.replace_dependent_parameter(item)
            url, query_str, request_data, headers, request_data_type = self.__request_info(item)
            
            # 分析请求参数信息
            headers, request_data = action.analysis_request(request_data, h_crypto, headers, r_crypto, ex_request_data)
            result_tp = None
            result = "PASS"
            
            # 执行请求操作
            kwargs = {request_data_type: request_data, 'headers': headers, "params": query_str}
            response = self.client.request(method, url, **kwargs)
            
            try:
                # 提取响应
                action.substitute_data(response.json(), regex=regex, keys=keys, deps=deps, jp_dict=jp_dict)
            except Exception as err:
                self.environment.events.request_failure.fire(request_type=method, name=f"{sheet}_{iid}_{name}_{desc}",
                                                             response_time=0, exception=err, response=response)
                continue
            
            # 修正断言
            expected = action.replace_dependent_parameter(expected)
            try:
                # 执行断言 返回结果元组
                result_tp = action.run_validate(expected, response.json())
                # self.assertNotIn("FAIL", result_tp, "FAIL 存在结果元组中")
            except Exception as e:
                result = "FAIL"
                self.environment.events.request_failure.fire(request_type=method, name=f"{sheet}_{iid}_{name}_{desc}",
                                                             response_time=response.elapsed.total_seconds() * 1000,
                                                             exception=e, response=response)
            finally:
                # 响应结果及测试结果回写 excel
                excel.write_back(sheet_name=sheet, i=iid, response=response.text, test_result=result,
                                 assert_log=str(result_tp))
    
    @staticmethod
    def __base_info(item):
        """
        获取基础信息
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
        expected = item.pop("Expected")
        return sheet, item_id, condition, sleep_time, name, desc, headers_crypto, request_data_crypto, method, expected
    
    @staticmethod
    def __sql_info(item):
        sql = item.pop("SQL")
        sql_params_dict = item.pop("Sql Params Dict")
        return sql, sql_params_dict
    
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
        """
        请求数据
        """
        url = item.pop("Url")
        query_str = item.pop("Query Str")
        request_data = item.pop("Request Data")
        headers = item.pop("Headers")
        request_data_type = item.pop("Request Data Type") if item.get("Request Data Type") else 'params'
        
        return url, query_str, request_data, headers, request_data_type
    
    @staticmethod
    def script(item):
        setup_script = item.pop("Setup Script")
        teardown_script = item.pop("Teardown Script")
        return setup_script, teardown_script
    
    @staticmethod
    def __is_run(condition):
        is_run = condition
        if not is_run or is_run.upper() != "YES":
            return True
    
    @staticmethod
    def __pause_execution(sleep_time):
        if sleep_time:
            try:
                time.sleep(sleep_time)
            except Exception as e:
                logger.error("暂时时间必须是数字")
                raise e
    
    def __exc_sql(self, item):
        sql, sql_params_dict = self.__sql_info(item)
        sql = action.replace_dependent_parameter(sql)
        if sql:
            try:
                execute_sql_results = action.execute_sql(sql)
                if execute_sql_results and sql_params_dict:
                    action.substitute_data(execute_sql_results, jp_dict=sql_params_dict)
            except Exception as e:
                logger.error(f'执行 sql 失败:{sql},异常信息:{e}')
                raise e
