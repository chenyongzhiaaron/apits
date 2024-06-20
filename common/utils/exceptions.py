# !/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: exceptions.py
@time: 2023/8/1 9:12
@desc:
"""
from common.log_utils.mylogger import MyLogger

logger = MyLogger()


class MyBaseException(Exception):
    def __init__(self, msg):
        self.msg = msg
        self.logger = logger

    def __str__(self):
        return self.msg


class RequestSendingError(MyBaseException):
    """请求异常"""
    ERROR_CODE = 1001

    def __init__(self, request_info, reason):
        msg = f"请求异常：request_info={request_info}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class DatabaseExceptionError(MyBaseException):
    """数据库异常"""
    ERROR_CODE = 1002

    def __init__(self, operation_info, reason):
        msg = f"数据库异常：操作信息={operation_info}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class ParameterExtractionError(MyBaseException):
    """参数提取异常"""
    ERROR_CODE = 1003

    def __init__(self, parameter_info, reason):
        msg = f"参数提取异常：参数信息={parameter_info}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class ParameterReplacementError(MyBaseException):
    """参数替换异常"""
    ERROR_CODE = 1004

    def __init__(self, parameter_info, reason):
        msg = f"参数替换异常：参数名称={parameter_info}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class AssertionFailedError(MyBaseException):
    """断言异常"""
    ERROR_CODE = 1005

    def __init__(self, assertion, reason):
        msg = f"执行断言失败：断言信息={assertion}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class ExecuteDynamiCodeError(MyBaseException):
    """执行动态代码异常"""
    ERROR_CODE = 1006

    def __init__(self, code_info, reason):
        msg = f"执行动态代码异常：动态代码信息={code_info}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class InvalidSleepTimeError(MyBaseException):
    """无效的暂停时间异常"""
    ERROR_CODE = 1007

    def __init__(self, sleep_time, reason):
        msg = f"无效的暂停时间：sleep_time={sleep_time}，原因={reason}"
        super().__init__(msg)

        self.logger.error(msg)


class ScriptNotFoundError(MyBaseException):
    """脚本不存在异常"""
    ERROR_CODE = 1008

    def __init__(self, script_info, reason):
        msg = f"脚本不存在异常：script_info={script_info}，原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class ScriptExecuteError(MyBaseException):
    """脚本执行存在异常"""
    ERROR_CODE = 10013

    def __init__(self, script_info, reason):
        msg = f"脚本执行异常：script_info={script_info}，原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class InvalidParameterFormatError(MyBaseException):
    """无效的参数格式异常"""
    ERROR_CODE = 1009

    def __init__(self, parameter_info, reason):
        msg = f"无效的参数格式异常：parameter_info={parameter_info}，原因={reason}"
        super().__init__(msg)
        self.logger.warning(msg)


class ResponseJsonConversionError(MyBaseException):
    """响应内容转换为 JSON 格式异常"""
    ERROR_CODE = 1010

    def __init__(self, response_text, reason):
        msg = f"响应内容转换为 JSON 格式异常：响应内容={response_text}, 原因={reason}"
        super().__init__(msg)
        self.logger.warning(msg)


class DynamicLoadingError(MyBaseException):
    """动态加载模块或文件异常"""
    ERROR_CODE = 1011

    def __init__(self, code_info, reason):
        msg = f"动态加载模块或文件发生异常：动态模块或文件={code_info}, 原因={reason}"
        super().__init__(msg)
        self.logger.error(msg)


class EncryptionError(MyBaseException):
    """加密失败异常"""
    ERROR_CODE = 1012

    def __init__(self, method_name, error_message):
        msg = f"加密失败异常:  加密方法={method_name} 原因={error_message}"
        super().__init__(msg)
        self.logger.error(msg)


if __name__ == '__main__':
    raise EncryptionError("111", "222")
