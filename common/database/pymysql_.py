#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: pymysql_.py
@time: 2023/6/14 17:58
@desc:
"""
import json
import logging
from functools import wraps

import pymysql
from dbutils.pooled_db import PooledDB

logger = logging.getLogger(__name__)


def singleton(cls):
    instances = {}

    @wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


@singleton
class DoMysql:
    def __init__(self, db_base):
        """
        Args:
            db_base: 数据库字典
            {
                "host": "xxxx.xxx.xxx.xx",
                "port": 3306,
                "database": "db_name",
                "user": "root",
                "password": "xxxx"
            }
        """
        if not db_base:
            return

        try:
            self.db_base = db_base if isinstance(db_base, dict) else json.loads(db_base)
            self.pool = PooledDB(
                creator=pymysql,
                maxconnections=10,
                host=self.db_base['host'],
                port=self.db_base['port'],
                user=self.db_base['user'],
                password=self.db_base['password'],
                database=self.db_base['database']
            )
        except Exception as e:
            logger.error(f"数据库链接失败: {e}")
            raise

    def execute_sql(self, sql):
        if not sql:
            return

        try:
            conn = self.pool.connection()
            cur = conn.cursor(pymysql.cursors.DictCursor)

            method_mapping = {
                "delete": self.execute_delete,
                "update": self.execute_update,
                "insert": self.execute_insert,
                "select": self.execute_select
            }

            result = {}
            for method, sql_data in sql.items():
                if method not in method_mapping:
                    logger.error("sql字典集编写格式不符合规范")
                    raise ValueError("Invalid SQL method")

                execute_method = method_mapping[method]
                execute_method(cur, sql_data, result)

            cur.close()
            conn.close()

            return result

        except Exception as e:
            logger.error(f"数据库操作异常: {e}")
            raise

    def execute_delete(self, cursor, sql_data, result):
        for sql_name, sql_ in sql_data.items():
            try:
                cursor.execute(str(sql_))
            except Exception as err:
                logger.error("执行 SQL 异常: {}".format(sql_))
                raise err
        cursor.connection.commit()

    def execute_update(self, cursor, sql_data, result):
        self.execute_delete(cursor, sql_data, result)

    def execute_insert(self, cursor, sql_data, result):
        self.execute_delete(cursor, sql_data, result)

    def execute_select(self, cursor, sql_data, result):
        for sql_name, sql_ in sql_data.items():
            try:
                cursor.execute(sql_)
                result[sql_name] = cursor.fetchall()
            except Exception as err:
                logger.error(f"查询异常 sql: {sql_}")
                raise err
