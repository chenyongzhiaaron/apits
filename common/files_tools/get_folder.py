#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 15:29
# @Author  : kira
import os


def get_folder(dir_path):
    folder = os.listdir(dir_path)
    return folder


if __name__ == '__main__':
    from common.base_datas import BaseDates

    d_path = os.path.join(BaseDates.base_path, "data", "bgy", "excel_file", "wifi_import_file")
    print(get_folder(d_path))
