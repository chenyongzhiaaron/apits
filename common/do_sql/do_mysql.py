# -*- coding: utf-8 -*-
# @Time : 2019/11/13 14:51
# @Author : kira
# @Email : 262667641@qq.com
# @File : do_mysql.py
# @Project : risk_project

import sys
import pymysql.cursors

sys.path.append("../")
sys.path.append("./common")

from common.tools.logger import MyLog


class DoMysql:

    def __init__(self, db_base: dict):
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
        try:
            self.conn = pymysql.connect(**db_base)  # 传入字典，连接数据库
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
                    for sql_dat in sql_data:
                        for sql_name, sql_ in sql_dat.items():
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
        "select": [
            {
                "select_sale": "select sale from do_mysql.sales"
            }
        ]
    }
    database_2 = {
        "host": "localhost",
        "port": 3306,
        "database": "do_mysql",
        "user": "root",
        "password": "admin"
    }

    res = DoMysql(database_2).do_mysql(sql_2)
    print(res)
