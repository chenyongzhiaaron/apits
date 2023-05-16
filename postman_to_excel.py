#!/usr/bin/env python
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
from common.files_tools.excel import DoExcel
from common.tools.parsing_postman import parsing_postman


def main(postman_filename, output_filename):
    """将postman导出的json文件转为excel测试用例"""
    postman_to_excel = parsing_postman(postman_filename)
    test_postman_case = BaseDates.templates  # 使用标准模板
    excel = DoExcel()
    excel.do_main(test_postman_case, *postman_to_excel, output_filename=output_filename)


if __name__ == '__main__':
    postman_to_json = r'D:\apk_api\api-test-project\temp\postman.json'  # postman导出的json文件
    out_file = os.path.join(BaseDates.base_path, 'data', 'test_cases', 'test_postman_cases.xlsx')  # 转化后的文件保存的位置
    main(postman_to_json, out_file)
