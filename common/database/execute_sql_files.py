"""
@author: kira
@contact: 262667641@qq.com
@file: execute_sql_files.py
@time: 2023/3/24 10:32
@desc: sql 语句批量执行小工具
"""

import glob
import os

import pymysql


def execute_sql_files(sql_path, error_log_dir, db_config):
    """
    批量执行sql语句
    Args:
        sql_path:文件夹
        db_config: 数据库配置

    Returns:

    """
    connection = pymysql.connect(**db_config)
    error_sql_list = []
    try:
        with connection.cursor() as cur:
            # 获取指定目录下的所有SQL文件
            sql_files = glob.glob(os.path.join(sql_path, "*.sql"))
            print(f"current executing sql_files is {sql_files}\n")

            for file in sql_files:
                base_name = os.path.basename(file)
                error_log_file = os.path.join(error_log_dir, os.path.splitext(base_name)[0] + "_error.sql")  # 收集错误sql文件
                with open(error_log_file, 'w', encoding="utf-8") as error_log:
                    with open(file, "r", encoding="utf-8") as f:
                        # 按照分号拆分SQL语句
                        sql_statements = f.read().strip().split(";")

                        for sql_statement in sql_statements:
                            if sql_statement:
                                try:
                                    cur.execute(sql_statement)
                                    connection.commit()
                                    print(f"-----> Successfully executed SQL: \n {sql_statement} <-----\n")
                                except Exception as e:
                                    # 失败sql重写入错误sql收集文件
                                    error_log.write(f"{sql_statement};\n")
                                    print(f"Error executing SQL from {file}: {e};\n")
    except Exception as e:
        print(f'Error connecting to {sql_files}: {e}')
    finally:
        connection.close()


if __name__ == '__main__':
    config = {
        "host": "....com",
        "port": 3306,
        "database": "",
        "user": "",
        "password": ""
    }
    error_sql_dir = r'D:\apiProject\apitest\error_sql_dir'
    sql_files = r'D:\apiProject\apitest\sql_statements'
    execute_sql_files(sql_files, error_sql_dir, config)
