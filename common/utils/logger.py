# -*- coding: utf-8 -*-
# @Time : 2019/11/18 10:17
# @Author : kira
# @Email : 262667641@qq.com
# @File : logger.py.py
# @Project : risk_api_project


import logging
import time
from logging import handlers

from common.config import Config


class MyLog:
    level_relations = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critic": logging.CRITICAL
    }  # 日志级别关系映射

    def my_log(self, msg, level="error", when="D", back_count=10):
        """
        实例化 TimeRotatingFileHandler
        interval 是时间间隔， backupCount 是备份文件的个数，如果超过这个个数，就会自动删除，when 是间隔的时间单位，单位有以下几种
        S 秒
        M 分
        H 小时
        D 天
        每星期（interval == 0 时代表星期一
        midnight 每天凌晨
        """
        file_name = Config.log_path

        my_logger = logging.getLogger()  # 定义日志收集器 my_logger
        my_logger.setLevel(self.level_relations.get(level))  # 设置日志级别

        format_str = logging.Formatter(
            "%(asctime)s-%(levelname)s-%(filename)s-[ line:%(lineno)d ] - 日志信息:%(message)s")  # 设置日志格式
        # 创建输出渠道
        sh = logging.StreamHandler()  # 往屏幕输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        current = time.strftime("%Y-%m-%d", time.localtime())  # 设置当前日期
        if level == "error":
            th = handlers.TimedRotatingFileHandler(filename=f'{file_name}/{current}_{level}.logger', when=when,
                                                   backupCount=back_count, encoding="utf-8")
        else:
            th = handlers.TimedRotatingFileHandler(filename=file_name + "/{}_info.logger".format(current), when=when,
                                                   backupCount=back_count,
                                                   encoding="utf-8")  # 往文件里写日志

        th.setFormatter(format_str)  # 设置文件里写入的格式
        my_logger.addHandler(sh)  # 将对象加入logger里
        my_logger.addHandler(th)

        if level == "debug":
            my_logger.debug(msg)
        elif level == "error":
            my_logger.error(msg)
        elif level == "info":
            my_logger.info(msg)
        elif level == "warning":
            my_logger.warning(msg)
        else:
            my_logger.critical(msg)

        my_logger.removeHandler(sh)
        my_logger.removeHandler(th)
        logging.shutdown()

    def decorator_log(self, msg=None):
        def warp(fun):
            def inner(*args, **kwargs):
                try:
                    return fun(*args, **kwargs)
                except Exception as e:
                    self.my_log(f"{msg}: {e}", "error")

            return inner

        return warp


if __name__ == '__main__':
    # for i in range(2):
    #     MyLog().my_log("hhhh{}".format(i), "info")
    #     time.sleep(0.04)
    @MyLog().decorator_log("知错了嘛？")
    def add():
        print("试一下")
        raise "不好使，异常了。"


    add()
