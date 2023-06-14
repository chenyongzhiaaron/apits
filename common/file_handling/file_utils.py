#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: file_utils.py
@time: 2023/6/14 16:28
@desc:
"""

import json
import os
from configparser import RawConfigParser

import yaml


class FileUtils:
    @staticmethod
    def get_all_path(open_file_path):
        """
        递归获取目录下所有的文件的路径
        Args:
            open_file_path: 指定目录路径

        Returns:
            包含所有文件路径的列表
        """
        path_list = []
        for root, dirs, files in os.walk(open_file_path):
            path_list.extend([os.path.join(root, file) for file in files])
        return path_list

    @staticmethod
    def get_files_in_folder(folder_path):
        """
        获取指定文件夹内的所有文件
        Args:
            folder_path: 指定文件夹路径

        Returns:
            包含所有文件名的列表
        """
        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path")
        file_list = []
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                file_list.append(filename)
        return file_list

    @staticmethod
    def get_folders_in_path(dir_path):
        """
        获取指定路径下的所有文件夹
        Args:
            dir_path: 指定路径

        Returns:
            包含所有文件夹名的列表
        """
        if not os.path.isdir(dir_path):
            raise ValueError("Invalid directory path")
        folder_list = []
        for foldername in os.listdir(dir_path):
            folder_path = os.path.join(dir_path, foldername)
            if os.path.isdir(folder_path):
                folder_list.append(foldername)
        return folder_list

    @staticmethod
    def read_file(file_path):
        """
        读取文件内容
        Args:
            file_path: 文件路径

        Returns:
            文件内容的字符串
        """
        if not os.path.isfile(file_path):
            raise ValueError("Invalid file path")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def read_json_file(file_path):
        """
        读取 JSON 文件
        Args:
            file_path: JSON 文件路径

        Returns:
            解析后的 JSON 数据
        """
        content = FileUtils.read_file(file_path)
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON file: {}".format(e))

    @staticmethod
    def read_yaml_file(file_path):
        """
        读取 YAML 文件
        Args:
            file_path: YAML 文件路径

        Returns:
            解析后的 YAML 数据
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @staticmethod
    def get_value_from_dict(data, key_path):
        """
        从嵌套字典中获取指定键路径的值
        Args:
            data: 嵌套字典
            key_path: 键路径，可以是用点分隔的字符串或字符串列表

        Returns:
            指定键路径的值，如果路径不存在则返回 None
        """
        if isinstance(key_path, str):
            key_path = key_path.split('.')

        for key in key_path:
            if isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None

        return data

    @staticmethod
    def read_config_data(file_path, section, option):
        """
        读取配置文件中的数据
        Args:
            file_path: 配置文件路径
            section: 文件中的 section
            option: 文件中的 option

        Returns:
            配置文件中指定数据的值
        """
        cf = RawConfigParser()
        cf.read(file_path, encoding="UTF-8")
        return eval(cf.get(section, option))

    @staticmethod
    def read_json_data(file_path):
        """
        读取 JSON 文件中的数据
        Args:
            file_path: JSON 文件路径

        Returns:
            JSON 文件中的数据
        """
        with open(file_path, "r", encoding="utf-8") as fb:
            return json.load(fb)
