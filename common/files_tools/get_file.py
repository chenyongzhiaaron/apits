# -*- coding: utf-8 -*-
# @Time : 2021/7/15 14:51
# @Author : kira
# @Email : 262667641@qq.com
# @File : get_file.py
# @Project : api-test-project


import os


def get_file(file_path):
    """
    获取指定目录内的所有文件
    Returns:

    """
    base_path = os.path.dirname(os.path.dirname(__file__))
    upload_order = os.path.join(base_path, file_path)
    file_list = []
    for filename in os.listdir(upload_order):
        file_list.append(filename)
    return file_list


if __name__ == '__main__':
    f_p = 'data/booking/booking_upload_order'
    print(get_file(f_p))
