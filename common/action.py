#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: action.py
@time: 2023/6/21 17:44
@desc:
"""

from common.crypto.encrypt_data import EncryptData
from common.utils.load_and_execute_script import LoadScript
from common.utils.singleton import singleton
from common.validation.extractor import Extractor
from common.validation.validator import Validator


@singleton
class Action(Extractor, LoadScript, Validator):
    def __init__(self):
        super().__init__()
        self.encrypt_data = EncryptData()
