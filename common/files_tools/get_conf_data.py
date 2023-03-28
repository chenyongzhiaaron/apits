# -*- coding: utf-8 -*-
import json
import sys
from configparser import RawConfigParser

sys.path.append("../")
from common.do_sql.do_mysql import DoMysql


class GetConfigData:

    @staticmethod
    def get_config_data(file_path, section, option):
        """
        读取配置文件
        :param file_path:   配置文件路径
        :param section:     文件 section
        :param option:      文件 option
        :return:
        """
        cf = RawConfigParser()
        cf.read(file_path, encoding="UTF-8")
        value = eval(cf.get(section, option))
        return value

    @staticmethod
    def get_json_data(file_path):
        with open(file_path, 'r', encoding='utf-8') as fb:
            json_data = json.load(fb)
        return json_data


if __name__ == '__main__':
    pat = r"D:\api-test-project\data\bgy\ai_sql.json"
    t = GetConfigData.get_json_data(pat)
    database_2 = {
        "host": "10.8.203.25",
        "port": 3306,
        "database": "ibs_ai_iot",
        "user": "root",
        "password": "gd1234"
    }
    data = DoMysql(database_2, **t).do_mysql()
    # print(t)
    print(data)
