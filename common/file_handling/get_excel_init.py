#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: get_init.py
@time: 2023/3/16 10:33
@desc:
"""
from common.file_handling.do_excel import DoExcel
from common.utils.mylogger import MyLogger


@MyLogger().log_decorator("读取excel中初始化数据异常")
def get_init(test_file):
    """
    Returns:返回初始化数据及测试用例
    """

    MyLogger().info(f"读取测试用例excel文件：{test_file}", "info")
    excel_handle = DoExcel(test_file)  # 实例化对象
    try:
        excel_handle.clear_date()  # 清空 excel 中实际结果列的数据
        test_case = excel_handle.do_excel_yield()  # 获取 excel 中的测试用例
        init_data = excel_handle.get_excel_init()  # 获取初始化基本数据
        MyLogger().info(f"如下是初始化得到得数据：{init_data}")
    except Exception as e:
        raise e
    return excel_handle, init_data, test_case


if __name__ == '__main__':
    from common.config import Config
    init = get_init(Config.test_api)
    print(init)
