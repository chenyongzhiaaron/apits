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

import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

from common.database import logger
from common.utils.singleton import singleton


@singleton
class MysqlClient:
	def __init__(self, db_config):
		"""
		初始化连接配置
		Args:
		    db_config: 数据库连接配置字典
			{
			    "host": "xxxx.xxx.xxx.xx",
			    "port": 3306,
			    "database": "db_name",
			    "user": "root",
			    "password": "xxxx"
			}
		"""
		if not db_config:
			return
		
		try:
			self.db_base = db_config if isinstance(db_config, dict) else json.loads(db_config)
			self.pool = PooledDB(creator=pymysql, maxconnections=10, **self.db_base)
		except Exception as e:
			logger.error(f"数据库链接失败: {e}")
			raise
	
	@logger.log_decorator()
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
			conn = self.pool.connection()
			cur = conn.cursor(DictCursor)
			
			result = {}
			for method, sql_data in sql.items():
				execute_method = getattr(self, f"_execute_{method}", None)
				if not execute_method:
					logger.error("sql字典集编写格式不符合规范")
					raise ValueError("Invalid SQL method")
				
				execute_method(cur, sql_data, result)
			
			cur.close()
			conn.close()
			
			return result
		
		except Exception as e:
			logger.error(f"数据库操作异常: {e}")
			raise
	
	def _execute_delete(self, cursor, sql_data, result):
		"""
		执行 DELETE 语句
		"""
		for sql_name, sql_ in sql_data.items():
			try:
				cursor.execute(str(sql_))
			except Exception as err:
				logger.error(f"执行 SQL 异常: {sql_}")
				raise err
		cursor.connection.commit()
	
	def _execute_update(self, cursor, sql_data, result):
		"""
		执行 UPDATE 语句
		"""
		self.execute_delete(cursor, sql_data, result)
	
	def _execute_insert(self, cursor, sql_data, result):
		"""
		执行 INSERT 语句
		"""
		self.execute_delete(cursor, sql_data, result)
	
	def _execute_select(self, cursor, sql_data, result):
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
				cursor.execute(sql_)
				result[sql_name] = cursor.fetchall()
			except Exception as err:
				logger.error(f"查询异常 sql: {sql_}")
				raise err


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
	res = MysqlClient(database_2).execute_sql(sql_2)
	print("数据执行结果", res)
	from common.data_extraction.data_extractor import DataExtractor
	from common.variables import Variables
	
	t = DataExtractor()
	t.substitute_data(res, jp_dict={"total": "$.select_sale[0].total", "total_1": "$..total"})
	print(Variables.get_variable())
