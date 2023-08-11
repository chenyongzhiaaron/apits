#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: mysql_client.py
@time: 2023/6/14 17:58
@desc: mysql数据库操作封装
"""

import json

import pymysql



# from DBUtils.PooledDB import PooledDB
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

from common.utils.decorators import singleton
from common.utils.exceptions import DatabaseExceptionError, InvalidParameterFormatError


@singleton
class MysqlClient:
    def __init__(self, db_config):
        """
        初始化连接配置
        Args:
            db_config: 数据库连接配置字典
        """
        if not db_config:
            return
        self.result = {}
        try:
            self.db_base = db_config if isinstance(db_config, dict) else json.loads(db_config)
            self.pool = PooledDB(creator=pymysql, maxconnections=10, **self.db_base)
            self.conn = self.pool.connection()
            self.cursor = self.conn.cursor(DictCursor)
        except Exception as e:
            DatabaseExceptionError(self.db_base, e)
            # raise

    def execute_sql(self, sql):
        """
        执行 SQL 语句

        Args:
            sql: SQL 语句字典
            {
                "delete": {
                "sql_name": "DELETE FROM table_name WHERE condition"
                },
                "update": {
                "sql_name": "UPDATE table_name SET column1=value1 WHERE condition"
                },
                "insert": {
                "sql_name": "INSERT INTO table_name (column1, column2) VALUES (value1, value2)"
                },
                "select": {
                "sql_name": "SELECT * FROM table_name WHERE condition"
                }
            }

        Returns:
            执行结果字典
            {
                "sql_name": [result1, result2, ...]
            }
        """
        if not sql:
            return
        try:
            for method, sql_data in sql.items():
                execute_method = getattr(self, f"_execute_{method}", None)
                if not execute_method:
                    InvalidParameterFormatError(sql, "sql字典集编写格式不符合规范")
                    raise ValueError("| Invalid SQL method")
                execute_method(sql_data)
            self.cursor.close()
            self.conn.close()
            return self.result

        except Exception as e:
            DatabaseExceptionError(sql, e)
            raise

    def _execute_write(self, sql_data):
        """
        执行通用的写入操作（INSERT、UPDATE、DELETE）
        """
        for sql_name, sql_ in sql_data.items():
            try:
                self.cursor.execute(str(sql_))
            except Exception as err:
                DatabaseExceptionError(sql_, err)
                raise err
        self.cursor.connection.commit()

    def _execute_select(self, sql_data):
        """
        执行 SELECT 语句

        Args:
            cursor: 数据库游标
            sql_data: SQL 语句数据字典
            {
                "sql_name": "SELECT * FROM table_name WHERE condition"
            }
            result: 字典结果

        Raises:
            Exception: 执行异常
        """
        for sql_name, sql_ in sql_data.items():
            try:
                self.cursor.execute(sql_)
                self.result[sql_name] = self.cursor.fetchall()

            except Exception as err:
                DatabaseExceptionError(sql_, err)
                raise err


if __name__ == '__main__':
    sql_2 = {
        "select":
            {
                # "select_one": "select username,password as pwd  from lea.user where username ='luoshunwen003';"
            }
    }
    database_2 = {
        "host": "localhost",
        "port": 3306,
        "database": "lea",
        "user": "root",
        "password": "admin"
    }
    res = MysqlClient(database_2).execute_sql(sql_2)
    print("数据执行结果", res)

# t = DataExtractor()
# t.substitute_data(res, jp_dict={"total": "$.select_sale[0].total", "total_1": "$..total"})
# print(Environments.get_environments())
