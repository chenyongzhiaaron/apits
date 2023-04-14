#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: base.py
@time: 2023/4/14 11:19
@desc:
"""

import json
import unittest
from jsonpath import jsonpath
import setting
from common import logger, db
from common.data_handler import (
    replace_args_by_re,
    generate_no_usr_phone)
from common.encrypt_handler import generate_sign
import requests


class BaseCase(unittest.TestCase):
    """
    用例基类
    """
    db = db
    logger = logger
    setting = setting
    name = 'base_case'
    session = requests.session()  # 创建一个session对象用来处理session鉴权

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info('==========={}接口开始测试==========='.format(cls.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info('==========={}接口结束测试==========='.format(cls.name))

    def flow(self, item):
        """
        测试流程
        """
        self.logger.info('>>>>>>>用例{}开始执行>>>>>>>>'.format(item['title']))
        # 把测试数据绑定到方法属性case上,其他也要把一些变量绑定到对象的属性上
        self._case = item
        # 1. 处理测试数据
        self.process_test()
        # 2. 发送请求
        self.send_request()
        # 3. 断言
        self.assert_all()

    def process_test(self):
        """
        测试数据的处理
        """
        # 1.1 生成测试数据
        self.generate_test_data()
        # 1.2 替换依赖参数
        self.replace_args()
        # 1.3 处理url
        self.process_url()
        # 1.4 鉴权处理
        self.auth_process()

    def auth_process(self):
        """
        v3版本鉴权处理
        :return:
        """
        request_data = self._case.get('request_data')
        if request_data:
            headers = request_data.get('headers')
            if headers:
                if headers.get('X-Lemonban-Media-Type') == 'lemonban.v3':
                    # 获取token
                    token = self._case['request_data']['headers']['Authorization'].split(' ')[-1]
                    # 生成签名
                    sign, timestamp = generate_sign(token, self.setting.SERVER_RSA_PUB_KEY)
                    # 添加到请求数据中
                    self._case['request_data']['json']['sign'] = sign
                    self._case['request_data']['json']['timestamp'] = timestamp

        # if self._case['request_data']['headers']['X-Lemonban-Media-Type'] == 'lemonban.v3':
        #     # 获取token
        #     token = self._case['request_data']['headers']['Authorization'].split(' ')[-1]
        #     # 生成签名
        #     sign, timestamp = generate_sign(token, self.setting.SERVER_RSA_PUB_KEY)
        #     # 添加到请求数据中
        #     self._case['request_data']['json']['sign'] = sign
        #     self._case['request_data']['json']['timestamp'] = timestamp

    def generate_test_data(self):
        """
        生成测试数据
        """
        """
           生成测试数据,不是固定流程，有不同可以复写
           :return:
           """
        self._case = json.dumps(self._case)
        if '$phone_number$' in self._case:
            phone = generate_no_usr_phone()
            self._case = self._case.replace('$phone_number$', phone)
        self._case = json.loads(self._case)

    def replace_args(self):
        """
        替换参数
        """
        self._case = json.dumps(self._case)  # 把用例数据dumps成字符串，一次替换
        self._case = replace_args_by_re(self._case, self)
        self._case = json.loads(self._case)
        # 再将request_data, expect_data loads为字典
        try:
            self._case['request_data'] = json.loads(self._case['request_data'])
            self._case['expect_data'] = json.loads(self._case['expect_data'])
        except Exception as e:
            self.logger.error('{}用例的测试数据格式不正确'.format(self._case['title']))
            raise e

    def process_url(self):
        """
        处理url
        """

        if self._case['url'].startswith('http'):
            # 是否是全地址
            pass
        elif self._case['url'].startswith('/'):
            # 是否是短地址
            self._case['url'] = self.setting.PROJECT_HOST + self._case['url']
        else:
            # 接口名称
            try:
                self._case['url'] = self.setting.INTERFACES[self._case['url']]
            except Exception as e:
                self.logger.error('接口名称：{}不存在'.format(self._case['url']))
                raise e

    def send_request(self):
        """
        发送请求
        @return:
        """
        self._response = self.session.request(
            url=self._case['url'], method=self._case['method'], **self._case['request_data'])
        # self._response = send_http_request(url=self._case['url'], method=self._case['method'],
        #                                    **self._case['request_data'])

    def assert_all(self):
        try:
            # 3.1 断言响应状态码
            self.assert_status_code()
            # 3.2 断言响应数据
            self.assert_response()
            # 响应结果断言成功后就提取依赖数据
            self.extract_data()
            # 3.3 数据库断言后面的任务
            self.assert_sql()
        except  Exception as e:
            self.logger.error('++++++用例{}测试失败'.format(self._case['title']))
            raise e
        else:
            self.logger.info('<<<<<<<<<用例{}测试成功<<<<<<<'.format(self._case['title']))

    def assert_status_code(self):
        """
        断言响应状态码
        """
        try:
            self.assertEqual(self._case['status_code'], self._response.status_code)
        except AssertionError as e:
            self.logger.warning('用例【{}】响应状态码断言异常'.format(self._case['title']))
            raise e
        else:
            self.logger.info('用例【{}】响应状态码断言成功'.format(self._case['title']))

    def assert_response(self):
        """
        断言响应数据
        """
        if self._case['res_type'].lower() == 'json':
            res = self._response.json()
        elif self._case['res_type'].lower() == 'html':
            # 扩展思路
            res = self._response.text
        try:
            self.assertEqual(self._case['expect_data'], {'code': res['code'], 'msg': res['msg']})
        except AssertionError as e:
            self.logger.warning('用例【{}】响应数据断言异常'.format(self._case['title']))
            self.logger.warning('用例【{}】期望结果为:{}'.format(self._case['title'], self._case['expect_data']))
            self.logger.warning('用例【{}】的响应结果:{}'.format(self._case['title'], res))
            raise e
        else:
            self.logger.info('用例【{}】响应数据断言成功'.format(self._case['title']))

    def assert_sql(self):
        """
        断言数据库
        """
        if self._case.get('sql'):  # 返回指定键的值，如果键不在字典中返回默认值 None 或者设置的默认值。
            # 只有sql字段有sql的才需要校验数据库
            # 只有sql字段有sql的才需要校验数据库
            sqls = self._case['sql'].split(',')
            for sql in sqls:
                try:
                    self.assertTrue(self.db.exist(sql))
                except AssertionError as e:
                    self.logger.warning('用例【{}】数据库断言异常，执行的sql为:{}'.format(self._case['title'], sql))
                    raise e
                except Exception as e:
                    self.logger.warning('用例【{}】数据库断言异常，执行的sql为:{}'.format(self._case['title'], sql))
                    raise e

    def extract_data(self):
        """
        根据提取表达式提取对应的数据
        :return:
        """
        if self._case.get('extract'):
            if self._case['res_type'].lower() == 'json':
                self.extract_data_from_json()
            elif self._case['res_type'].lower() == 'html':
                self.extract_data_from_html()
            elif self._case['res_type'].lower() == 'xml':
                self.extract_data_from_xml()
            else:
                raise ValueError('res_type类型不正确，只支持json，html，xml')

    def extract_data_from_json(self):
        """
        从json数据中提取数据并绑定到类属性中
        :return:
        """
        try:
            rules = json.loads(self._case.get('extract'))
        except Exception as e:
            raise ValueError(
                '用例【{}】的extract字段数据：{}格式不正确'.format(self._case['title'], self._case['extract']))
        for rule in rules:
            # 类属性名
            name = rule[0]
            # 提取表达式
            exp = rule[1]
            # 根据jsonpath去响应中提取值
            value = jsonpath(self._response.json(), exp)
            # 如果能提取到值
            if value:
                # 把值绑定到对应的类属性上
                setattr(self.__class__, name, value[0])  # 注意value是个列表
            else:
                # 提取不到值，说明jsonpath写错了，或者是响应又问题
                raise ValueError(
                    '用例【{}】的提取表达式{}提取不到数据'.format(self._case['title'], self._case['extract']))

    def extract_data_from_html(self):
        """
        从html数据中提取数据并绑定到类属性中
        :return:
        """
        raise ValueError('请实现此方法')

    def extract_data_from_xml(self):
        """
        从xml数据中提取数据并绑定到类属性中
        :return:
        """
        raise ValueError('请实现此方法')
