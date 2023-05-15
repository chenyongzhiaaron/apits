import os


class BaseDates:
    # 根目录路径
    # *****************************************************************
    base_path = os.path.dirname(os.path.dirname(__file__))
    current_path = os.path.dirname(__file__)
    # *****************************************************************
    # 测试数据所在路径
    # *****************************************************************
    test_api = os.path.join(base_path, "data", "moduleA", "test_api.xlsx")
    # *****************************************************************

    # 测试用例脚本目录
    # *****************************************************************
    script = os.path.join(base_path, "test_script")
    # *****************************************************************

    # 测试报告及 log 所在路径
    # *****************************************************************
    test_report = os.path.join(base_path, "OutPut", "Reports")
    log_path = os.path.join(base_path, "OutPut", "Log")




if __name__ == '__main__':
    test = BaseDates()
    print(test.base_path)
    print(test.test_api)
    print(test.test_report)
    print(test.test_api)
    print(test.current_path)
