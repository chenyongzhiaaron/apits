# -*- coding: utf-8 -*-
# @Time : 2019/11/13 14:51
# @Author : kira
# @Email : 262667641@qq.com
# @File : do_mysql.py
# @Project : risk_project
import json
import sys
import pymysql.cursors

sys.path.append("../")
sys.path.append("./common")

from common.tools.logger import MyLog
from common.tools.singleton import singleton


@singleton
class DoMysql:

    def __init__(self, db_base):
        """

        Args:
            db_base:数据库字典
            {
                "host": "xxxx.xxx.xxx.xx",
                "port": 3306,
                "database": "db_name",
                "user": "root",
                "password": "xxxx"
            }
        """

        # self.sql = sql
        if not db_base:
            return
        try:
            db_base = db_base if isinstance(db_base, dict) else json.loads(db_base)
            self.conn = pymysql.connect(**db_base, connect_timeout=15)  # 传入字典，连接数据库
            self.cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 操作结果为字典的游标
        except Exception as e:
            MyLog().my_log(f"数据库链接失败: {e}")

    def do_mysql(self, sql):
        """
        执行 mysql 数据库操作
                    sql: sql字典嵌套字典嵌套列表集合{
                "select": [{"查xxx": "select * from tab"},{"":""}],
                "delete":[{"删除xxx"："delete from xxxx where xxx"}],
                "update":[],
                "insert":[]
                 }
        :sql:
        :return: 返回操作结果，以字典形式返回
        """
        # print(f"type:{type(sql)}")
        if not sql:
            return
        result = None
        for method in sql.keys():
            if method not in ["delete", "update", "insert", "select"]:
                MyLog().my_log("sql字典集编写格式不符合规范")
                raise
            if method in ["delete", "update", "insert"]:
                for sql_list in sql.values():
                    for sql_name, sql_ in sql_list.items():
                        # 执行 提交 sql
                        try:
                            self.cur.execute(str(sql_))
                        except Exception as err:
                            MyLog().my_log("执行 sql 异常: {}".format(sql_))
                            self.conn.rollback()  # 异常回滚
                            raise err
                    self.conn.commit()  # 提交事务
            else:
                sql_result = {}
                for sql_data in sql.values():
                    for sql_name, sql_ in sql_data.items():
                        try:
                            self.cur.execute(sql_)  # 执行查询 sql_file
                            sql_result[f"{sql_name}"] = self.cur.fetchall()  # 返回所有查询结果
                        except Exception as err:
                            print(f"--->查询异常 sql: {sql_}")
                            raise err
                    result = sql_result
            return result

    def __del__(self):
        try:
            self.cur.close()  # 关闭游标
            self.conn.close()  # 关闭链接
        except Exception as e:
            MyLog().my_log(f"关闭数据库失败: {e}")


if __name__ == '__main__':
    sql_2 = {
        "select":
            {
                "select_sale": "select count(1) total, (case when t1.status = 1 then '待整改' when t1.status = 2 then '待复查' when t1.status = 3 then '整改完成' else '未知类型' end) orderStatus from ibs_ai_iot.ai_rectification_main t1 left join ibs_ai_iot.work_order t3 on t1.id = t3.rectification_id where t1.project_id = 103672 and t1.delete_flag = 0 and t3.is_delete = 0 group by t1.status order by orderStatus desc;",
                "select_sale_1": "select count(1) total, (case when t1.status = 1 then '待整改' when t1.status = 2 then '待复查' when t1.status = 3 then '整改完成' else '未知类型' end) orderStatus from ibs_ai_iot.ai_rectification_main t1 left join ibs_ai_iot.work_order t3 on t1.id = t3.rectification_id where t1.project_id = 103672 and t1.delete_flag = 0 and t3.is_delete = 0 group by t1.status order by orderStatus desc;"
            }

    }
    database_2 = {
        "host": "10.8.203.25",
        "port": 3306,
        "database": "ibs_lms_base",
        "user": "root",
        "password": "gd1234"
    }
    res = DoMysql(database_2).do_mysql(sql_2)
    print(res)
    from common.extractor.data_extractor import DataExtractor
    from common.dependence import Dependence

    DataExtractor(res).substitute_data(jp_dict={"total": "$.select_sale[0].total", "total_1": "$..total"})
    print(Dependence.get_dep())
