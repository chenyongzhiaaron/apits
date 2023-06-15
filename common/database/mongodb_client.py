import sys
import os
import json
import re
import jsonpath
import pymongo

from dateutil import parser
from common.config import Config
from common.file_handling.do_excel import DoExcel

sys.path.append("../")
sys.path.append("./common")


class MongodbClient(object):

    def __init__(self, db_info):
        self.mongo_info = eval(db_info)  # mongo数据库配置信息,字典形式
        self.mongo_client = pymongo.MongoClient(host=self.mongo_info["host"], port=self.mongo_info["port"])  # 获取连接实例
        self.my_db = self.mongo_client.admin  # 连接系统默认数据库 admin
        self.my_db.authenticate(self.mongo_info["username"], self.mongo_info["password"],
                                mechanism='SCRAM-SHA-1')  # 让 admin数据库去认证密码登录
        self.db = self.mongo_client[self.mongo_info["database"]]  # 连接自己的数据库需要操作的数据库

    def do_mongo(self, **data):
        """
        Args:
            **data: sql_file 操作语句
        Returns:
        """
        result = {}
        for method, sql_dates in data.items():
            if method == "select":
                for table_name, sql_s in sql_dates.items():
                    for index, sql in enumerate(sql_s):
                        result_obj = self.db[table_name].find_one(sql)
                        result["${" + "{}".format(index) + "}"] = result_obj
            if method == "delete":
                for table_name, sql_s in sql_dates.items():
                    for index, sql in enumerate(sql_s):
                        self.db[table_name].delete_many(sql)
                        result["#{0}:{1}".format(table_name, sql)] = "删除成功"
            if method == "insert":
                for table_name, sql_s in sql_dates.items():
                    for index, sql in enumerate(sql_s):
                        self.db[table_name].insert_one(sql)
                        result["#{0}:{1}".format(table_name, sql)] = "插入成功"
        self.mongo_client.close()
        return result

    def insert_data(self):
        base_path = os.path.join(Config.base_path, "data")
        names = os.listdir(base_path)
        for name in names:
            if re.match(r"(.+?).json", name):
                table_name = re.match(r"(.*?)\.json", name).group(1)
                print(table_name)
                actuator = self.db[table_name]
                with open(base_path + "\\{}.json".format(table_name), encoding='utf-8') as f:
                    data = json.load(f)
                result_data = []
                for sql in data:
                    if "_id" in sql.keys():
                        sql.pop("_id")
                        created_at = jsonpath.jsonpath(sql, "$.createdAt.$date")[0]
                        updated_at = jsonpath.jsonpath(sql, "$.updatedAt.$date")[0]
                        sql["createdAt"] = parser.parse(created_at)
                        sql["updatedAt"] = parser.parse(updated_at)
                        if "intentionPaymentDate" in sql.keys():
                            intention_payment_date = jsonpath.jsonpath(sql, "$..intentionPaymentDate.$date")[0]
                            sql["intentionPaymentDate"] = parser.parse(intention_payment_date)
                            result_data.append(sql)
                        else:
                            result_data.append(sql)
                actuator.insert_many(result_data)
                print("*" * 50)
                self.mongo_client.close()


if __name__ == "__main__":
    db_file = Config.test_data_address
    excel_handle = DoExcel(db_file)
    excel_init = excel_handle.get_excel_init()
    mongo_base = excel_init["test_databases"]
    MongodbClient(mongo_base).insert_data()
    # site = {'name': '我的博客地址', 'alexa': 10000, 'url': 'http://blog.csdn.net/uuihoo/'}
    # pop_obj = site.pop('name')  # 删除要删除的键值对，如{'name':'我的博客地址'}这个键值对
    # print(pop_obj)  # 输出 ：我的博客地址
    # print(site)
