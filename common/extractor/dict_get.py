# -*- coding: utf-8 -*-
# @Time : 2020/1/20 15:50
# @Author : kira
# @Email : 262667641@qq.com
# @File : dict_get.py
# @Project : api_project


def dict_get(dic, locators, default=None):
    """
    以参数形式获取字典中特定的值
    :param dic: 输入需要在其中取值的原始字典 <dict>
    :param locators: 输入取值定位器, 如:['result', 'msg', '-1', 'status'] <list>
    :param default: 进行取值中报错时所返回的默认值 (default: None)
    :return: 返回根据参数locators找出的值

    """

    if not isinstance(dic, dict) or not isinstance(locators, list):
        return default

    value = None

    for locator in locators:
        if not type(value) in [dict, list] and isinstance(locator, str) and not can_convert_to_int(locator):
            try:
                value = dic[locator]
            except KeyError:
                return default
            continue
        if isinstance(value, dict):
            try:
                value = dict_get(value, [locator])
            except KeyError:
                return default
            continue
        if isinstance(value, list) and can_convert_to_int(locator):
            try:
                value = value[int(locator)]
            except IndexError:
                return default
            continue

    return value


def can_convert_to_int(input_s):
    try:
        int(input_s)
        return True
    except Exception:
        return False


if __name__ == '__main__':
    # dict_test = {"result": {"code": "110002", "msg": [{'status': 'ok'}, {'status': 'failed'}]}}
    # result = dict_get(dict_test, ['result', 'msg', '-1', 'status'])
    dict_test = {"data": {"result": [{"taskId": 1, "taskName": "2020-01-23 调研任务", "taskStatus": 2}], "totalCount": 1,
                          "pageSize": 20},"taskId":2, "msg": "操作成功!", "status": 200}
    result = dict_get(dict_test, ['data', 'result', 0, 'taskId'])
    print(result)
