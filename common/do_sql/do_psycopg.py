# -*- coding: utf-8 -*-
# @Time : 2019/12/6 9:16
# @Author : kira
# @Email : 262667641@qq.com
# @File : do_psycopg.py
# @Project : risk_api_project
# import psycopg2
# import psycopg2.extras


# class DoPostgreSQL:
#
#     def __init__(self):
#         postgre_config = BaseDates.postgreSql
#         self.connection = psycopg2.connect(**postgre_config)
#
#     def do_postgre_sql(self, sql_file):
#         curs = self.connection.cursor()
#         curs.execute(sql_file)
#         select_value = curs.fetchone()
#         # select_value = curs.fetchall()
#         # self.connection.close()
#         return select_value
#
#
# class Yoy:
#     def yoy(self, current, yesteryear):
#         return current / yesteryear
#
#
# if __name__ == '__main__':
#     test = DoPostgreSQL()
