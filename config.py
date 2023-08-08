import os


class Config:
    # 根目录路径
    # *****************************************************************
    base_path = os.path.dirname(__file__)
    # *****************************************************************
    # 测试数据所在路径
    # *****************************************************************
    templates = os.path.join(base_path, "cases", "templates", "template.xlsx")  # 模板文件
    # test_case = os.path.join(base_path, "cases", "cases", "test_api.xlsx")
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
    test_report_file = os.path.join(base_path, "output", "reports","report.html")
    log_path = os.path.join(base_path, "output", "log")
    SCRIPTS_DIR = os.path.join(base_path, "scripts")

    # 邮件配置信息
    mail_data = {
        "host": "smtp.qq.com",  # 邮件服务地址
        "user": "262667641@qq.com",  # 用户名
        "password": "ztvqsnikiupvbghe",  # 密码（部分邮箱为授权码）# 密码
        "sender": "262667641@qq.com",  # 发送人
        "port": 465,  # smtp 端口号
        "receivers": ['262667641@qq.com', '125109524@qq.com']  # 接收方的邮箱
    }
    # 企业微信机器人配置信息
    weixin_notice = {
        "send_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=8b1647d4-dc32-447c-b524-548acf18a938",
        "upload_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?type=file&key=8b1647d4-dc32-447c-b524-548acf18a938",
        "file_lists": [test_report_file, test_case]  # 需要推送的文件的路径
    }
    # 钉钉机器人配置信息
    dingtalk_notice = {
        "url": "https://oapi.dingtalk.com/robot/send?access_token=7d1e11079e00a4ca9f11283f526349abd5ba3f792ef7bcb346909ff215af02de",
        "secret": "SEC441dbbdb8dbe150e5fc3e348bb449d3113b1be1a90be527b898ccd78c51566c1",
        "key": "",  # 安全关键字
        "atMobiles": "18127813600",  # 需要@指定人员的手机号
        "isAtAll": True,  # 是否@ 所有人
        "except_info": False  # 是否发送测试不通过的异常数据
    }


if __name__ == '__main__':
    test = Config()
    print(test.base_path)
    print(test.test_case)
    print(test.test_report)
    print(test.test_case)
    print(test.SCRIPTS_DIR)
