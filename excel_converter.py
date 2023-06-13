import os.path

from common.config import BaseDates
from common.file_handling.excel import DoExcel
from common.utils.parsing_postman import parsing_postman
from common.utils.parsing_openapi import parsing_openapi


class ExcelConverter:
    tool_mapping = {
        'postman': 'convert_postman_to_excel',
        'openapi': 'convert_openapi_to_excel'
    }

    def __init__(self, tool_type, input_file, output_file):
        self.tool_type = tool_type
        self.input_file = input_file
        self.output_file = output_file
        # 使用标准模板
        self.excel = DoExcel(BaseDates.templates)

    def convert_openapi_to_excel(self):
        """将openapi导出的json文件转为excel测试用例"""
        openapi_to_json = parsing_openapi(self.input_file)  # 解析 openapi 文件
        self.excel.do_main(self.output_file, *openapi_to_json)  # 参照模板文件，写入数据

    def convert_postman_to_excel(self):
        """将postman导出的json文件转为excel测试用例"""
        postman_to_excel = parsing_postman(self.input_file)
        self.excel.do_main(self.output_file, *postman_to_excel)

    def main(self):
        conversion_method = self.tool_mapping.get(self.tool_type)
        if conversion_method:
            getattr(self, conversion_method)()


if __name__ == '__main__':
    postman_to_json = r'.\data\temporary_file\postman.json'  # postman导出的json文件
    postman_out_file = os.path.join(BaseDates.base_path, 'cases', 'test_cases', 'test_postman_cases.xlsx')  # 转化后的文件保存的位置
    openapi_to_json = r'.\data\temporary_file\openapi.json'  # postman导出的json文件
    openapi_out_file = os.path.join(BaseDates.base_path, 'cases', 'test_cases', 'test_openapi_cases.xlsx')  # 转化后的文件保存的位置
    ExcelConverter('postman', postman_to_json, postman_out_file).main()
    ExcelConverter('postman', openapi_to_json, openapi_out_file).main()
