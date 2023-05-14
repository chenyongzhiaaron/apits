import os


class BaseDates:
    # 根目录路径
    # *****************************************************************
    base_path = os.path.dirname(os.path.dirname(__file__))
    current_path = os.path.dirname(__file__)
    # *****************************************************************
    # 测试数据所在路径
    # *****************************************************************
    test_api = os.path.join(base_path, "data", "moduleA", "test_cases", "test_api.xlsx")
    # *****************************************************************

    # 测试用例脚本目录
    # *****************************************************************
    # script = os.path.join(base_path, "test_script", "test_script")
    script = os.path.join(base_path, "test_script")
    # *****************************************************************

    # 测试报告及 log 所在路径
    # *****************************************************************
    test_report = os.path.join(base_path, "OutPut", "Reports")
    log_path = os.path.join(base_path, "OutPut", "Log")

    wx_send_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
    wx_up_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?type=file&key="


if __name__ == '__main__':
    test = BaseDates()
    print(test.base_path)
    print(test.test_api)
    print(test.test_report)
    print(test.test_api)
    print(test.current_path)
