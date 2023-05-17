#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: openapi_to_excel.py
@time: 2023/5/17 11:15
@desc:
"""
from temp.tests import DoExcel

# !/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: postman_to_excel.py
@time: 2023/5/16 16:35
@desc:
"""
import os.path

from common.base_datas import BaseDates
# from common.files_tools.excel import DoExcel

from common.tools.parsing_openapi import parsing_openapi


def main(openapi_filename, output_filename):
    """将openapi导出的json文件转为excel测试用例"""
    openapi_to_json = parsing_openapi(openapi_filename)  # 解析 openapi 文件
    print(openapi_to_json)
    template = BaseDates.templates  # 获取标准模板
    DoExcel(template).do_main(output_filename, *openapi_to_json)  # 参照模板文件，写入数据


if __name__ == '__main__':
    openapi_to_json = r'D:\apk_api\api-test-project\data\temporary_file\openapi.json'  # postman导出的json文件
    out_file = os.path.join(BaseDates.base_path, 'data', 'test_cases', 'test_openapi_cases.xlsx')  # 转化后的文件保存的位置
    main(openapi_to_json, out_file)
