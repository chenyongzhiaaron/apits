import pymysql
import os

"""
批量读取文件下的 sql 文件并打开文件执行文件内的每条 sql
"""
sql_path = "/backend/sql"
files = os.listdir(sql_path)
connection = pymysql.connect(host='172.17.0.1', user='root', password='root', db='QAPlatform', port=3308)
cur = connection.cursor()
for file in files:
    with open(file, "r", encoding="utf-8") as f:
        a1 = f.read()
    a2 = a1.strip().split(";")
    for i in a2:
        if i:
            cur.execute("%s;" % i)
            connection.commit()
cur.close()
connection.close()
