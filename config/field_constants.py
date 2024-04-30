#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: field_names.py
@time: 2023/8/17 17:39
@desc:
"""


class FieldNames:
    """sheet字段"""
    INIT = "init"
    SHEETS = "Sheets"
    SHEET = "Sheet"
    ITEM_ID = "Id"
    RUN_CONDITION = "Run"
    SLEEP_TIME = "Time"
    NAME = "Name"
    DESCRIPTION = "Description"
    METHOD = "Method"
    EXPECTED = "Expected"
    SQL = "SQL"
    SQL_PARAMS_DICT = "SqlParamsDict"
    REGEX = "Regex"
    REGEX_PARAMS_LIST = "RegexParamsList"
    RETRIEVE_VALUE = "RetrieveValue"
    JSON_PATH_DICT = "Jsonpath"
    EXTRACT_REQUEST_DATA = "ExtractRequestData"
    URL = "Url"
    QUERY_STRING = "QueryString"
    REQUEST_DATA = "RequestData"
    HEADERS = "Headers"
    REQUEST_DATA_TYPE = "RequestDataType"
    HEADERS_CRYPTO = "HeadersCrypto"
    REQUEST_DATA_CRYPTO = "RequestDataCrypto"
    SETUP_SCRIPT = "SetupScript"
    TEARDOWN_SCRIPT = "TeardownScript"
    PARAMS = "params"
    RESPONSE = "response"
    RESULT = "result"
    ASSERTIONS = "assertions"
    YES = "YES"
    DATABASES = "Databases"
    INITIALIZE_DATA = "InitializeData"
    HOST = "Host"
    PATH = "Path"

    def __init__(self):
        super().__init__()
