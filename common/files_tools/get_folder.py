#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/22 15:29
# @Author  : kira
import os


def get_folder(dir_path):
    """
    获取指定路径下的所有文件夹
    Args:
        dir_path:

    Returns:

    """
    folder = os.listdir(dir_path)
    return folder


if __name__ == '__main__':
    from common.base_datas import BaseDates

    d_path = os.path.join(BaseDates.base_path)
    print(get_folder(d_path))
