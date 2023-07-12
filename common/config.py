import os


class Config:
    # 根目录路径
    # *****************************************************************
    base_path = os.path.dirname(os.path.dirname(__file__))
    current_path = os.path.dirname(__file__)
    # *****************************************************************
    # 测试数据所在路径
    # *****************************************************************
    templates = os.path.join(base_path, "cases", "templates", "template.xlsx")  # 模板文件
    test_case = os.path.join(base_path, "cases", "cases", "test_cases.xlsx")
    test_files = os.path.join(base_path, 'cases', 'files')
    # *****************************************************************
    
    # 测试用例脚本目录
    # *****************************************************************
    script = os.path.join(base_path, "test_script")
    # *****************************************************************
    
    # 测试报告及 logger 所在路径
    # *****************************************************************
    test_report = os.path.join(base_path, "output", "reports")
    log_path = os.path.join(base_path, "output", "log")
    SCRIPTS_DIR = os.path.join(base_path, "scripts")


if __name__ == '__main__':
    test = Config()
    print(test.base_path)
    print(test.test_case)
    print(test.test_report)
    print(test.test_case)
    print(test.current_path)
    print(test.SCRIPTS_DIR)
