import glob
import os

import pymysql

from common.database import logger


@logger.log_decorator()
def execute_sql_files(sql_path, db_config):
	"""
	批量执行sql语句
	Args:
	    sql_path:文件夹
	    db_config: 数据库配置
    
	Returns:
 
	"""
	connection = pymysql.connect(**db_config)
	
	try:
		with connection.cursor() as cur:
			# 获取指定目录下的所有SQL文件
			sql_files = glob.glob(os.path.join(sql_path, "*.sql"))
			
			for file in sql_files:
				with open(file, "r", encoding="utf-8") as f:
					sql_statements = f.read().strip().split(";")
					
					for sql_statement in sql_statements:
						if sql_statement:
							cur.execute(sql_statement)
			
			connection.commit()
	
	finally:
		connection.close()


if __name__ == '__main__':
	config = {
		"host": "xxxx.xxx.xxx.xx",
		"port": 3306,
		"database": "db_name",
		"user": "root",
		"password": "xxxx"
	}
	
	execute_sql_files('./sql.sql', config)
