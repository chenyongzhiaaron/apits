#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/29 8:50
# @Author  : kira
import os
import random
import sys

sys.path.append('../../../')
sys.path.append('../..')

from common.config import Config


class Social(object):
    '''
    统一社会信用代码 + 组织结构代码校验
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # 统一社会信用代码中不使用I,O,S,V,Z
        # ''.join([str(i) for i in range(10)])
        # import string
        # string.ascii_uppercase  # ascii_lowercase |  ascii_letters
        # dict([i for i in zip(list(self.string), range(len(self.string)))])
        # dict(enumerate(self.string))
        # list(d.keys())[list(d.values()).index(10)]
        # chr(97)  --> 'a'
        self.string1 = '0123456789ABCDEFGHJKLMNPQRTUWXY'
        self.SOCIAL_CREDIT_CHECK_CODE_DICT = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17,
            'J': 18, 'K': 19, 'L': 20, 'M': 21, 'N': 22, 'P': 23, 'Q': 24,
            'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30}
        # 第i位置上的加权因子
        self.social_credit_weighting_factor = [1, 3, 9, 27, 19, 26, 16, 17, 20, 29, 25, 13, 8, 24, 10, 30, 28]

        # GB11714-1997全国组织机构代码编制规则中代码字符集
        self.string2 = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.ORGANIZATION_CHECK_CODE_DICT = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
            'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26,
            'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}
        # 第i位置上的加权因子
        self.organization_weighting_factor = [3, 7, 9, 10, 5, 8, 4, 2]

    def gen_check_code(self, weighting_factor, ontology_code, modulus, check_code_dict):
        '''
        @param weighting_factor: 加权因子
        @param ontology_code:本体代码
        @param modulus:  模数(求余用)
        @param check_code_dict: 字符字典
        '''
        total = 0
        for i in range(len(ontology_code)):
            if ontology_code[i].isdigit():
                # print(ontology_code[i], weighting_factor[i])
                total += int(ontology_code[i]) * weighting_factor[i]
            else:
                num = check_code_dict.get(ontology_code[i], -1)
                if num < 0:
                    return -1
                total += num * weighting_factor[i]
        diff = modulus - total % modulus

        return diff


def unified_social_credit_code():
    """统一社会信用代码"""

    department = "123456789999999999999999"  # 登记管理部门代码
    agency = "11111111111111112121212345999"  # 机构类别
    organization_num = str(random.randint(11111111, 99999999))
    u = Social()
    # 组织机构代码校验位
    check_code = u.gen_check_code(u.organization_weighting_factor, organization_num, 11, u.ORGANIZATION_CHECK_CODE_DICT)
    organization_code = organization_num + str(check_code)  # 组织机构代码
    address_code = get_address(True)
    # 没有校验码的社会统一代码
    un_code = random.choice(department) + random.choice(agency) + str(address_code) + organization_code
    # 社会 校验位
    social_num = u.gen_check_code(u.social_credit_weighting_factor, un_code, 31, u.SOCIAL_CREDIT_CHECK_CODE_DICT)
    if social_num == 31:
        social_num = 0
    social_dict = {value: key for key, value in u.SOCIAL_CREDIT_CHECK_CODE_DICT.items()}
    # 两位证书 转换成 协议里面的值
    social_key = social_dict[social_num]
    code = un_code + social_key
    return code


def get_address(code=False, random_switch=True, all_info=False, **kwargs):
    """
    :param code: 只返回 地区码
    :param random_switch: 自定义区域 然后随机地区
    :param kwargs: province_num = 省 city_info = 市 district_info = 区
    :return: code False 省市区 code True 地区吗
    """
    import json
    address_path = os.path.join(os.path.dirname(__file__), "address.json")
    with open(address_path, 'r', encoding='UTF-8') as file:
        info = json.load(file)
    i = 0
    province_num = None
    city_info = None
    district_info = None
    error_num = 0
    while True:
        try:
            if random_switch:
                province_num = random.randint(0, len(info) - 1)
            else:
                for address_info in info:

                    if kwargs['province_name'] == address_info['name']:
                        province_num = i
                        break
                    i += 1
            province_date = info[province_num]

            province_name = province_date['name']
            if 'city_name' in kwargs.keys():
                for city in province_date['child']:
                    if city['name'] == kwargs['city_name']:
                        city_info = city
                        break
                city_name = kwargs['city_name']
            else:
                city_info = random.choice(province_date['child'])
                city_name = city_info['name']

            if 'district_name' in kwargs.keys():
                for district in city_info['child']:
                    if district['name'] == kwargs['district_name']:
                        district_info = district
            else:
                district_info = random.choice(city_info['child'])
            district_name = district_info['name'].replace('　', '')
            if code and not all_info:
                return district_info['code']
            elif code and all_info:
                return province_name, city_name, district_name, district_info['code']
            else:
                return province_name, city_name, district_name
        except Exception as e:
            error_num += 1
            if error_num >= 3:
                raise Exception(e)


if __name__ == '__main__':
    t = get_address()
    c = unified_social_credit_code()
    # print(t)
    print(c)
