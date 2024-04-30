# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         comparators.py
# Description:  内建比较器
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2020/2/25 16:48
# -------------------------------------------------------------------------------
import json
import re


def p_string(a, e, failed_info_ignore=None):
    ta = str(type(a)).replace("<", "(").replace(">", ")")
    te = str(type(e)).replace("<", "(").replace(">", ")")
    return f"<span style='color:red' >实际: {a} -> {ta}, 预期: {e} -> {te}, 失败信息及忽略字段: {failed_info_ignore}</span>"


def eq(actual_value, expect_value, ignore=None):
    """
    实际值与期望值相等
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert actual_value == expect_value, p_string(actual_value, expect_value, ignore)


def lt(actual_value, expect_value, ignore=None):
    """
    实际值小于期望值
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert actual_value < expect_value, p_string(actual_value, expect_value, ignore)


def lte(actual_value, expect_value, ignore=None):
    """
    实际值小于或等于期望值
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert actual_value <= expect_value, p_string(actual_value, expect_value, ignore)


def gt(actual_value, expect_value, ignore=None):
    """
    实际值大于期望值
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert actual_value > expect_value, p_string(actual_value, expect_value, ignore)


def gte(actual_value, expect_value, ignore=None):
    """
    实际值大于或等于期望值
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert actual_value >= expect_value, p_string(actual_value, expect_value, ignore)


def neq(actual_value, expect_value, ignore=None):
    """
    实际值与期望值不相等
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert actual_value != expect_value, p_string(actual_value, expect_value, ignore)


def str_eq(actual_value, expect_value, ignore=None):
    """
    字符串实际值与期望值相同
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert str(actual_value) == str(expect_value), p_string(actual_value, expect_value, ignore)


def length_eq(actual_value, expect_value, ignore=None):
    """
    实际值的长度等于期望长度
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(expect_value, (int,)), p_string(actual_value, expect_value, ignore)
    assert len(actual_value) == expect_value, p_string(actual_value, expect_value, ignore)


def length_gt(actual_value, expect_value, ignore=None):
    """
    实际值的长度大于期望长度
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(expect_value, (int,)), p_string(actual_value, expect_value, ignore)
    assert len(actual_value) > expect_value, p_string(actual_value, expect_value, ignore)


def length_gte(actual_value, expect_value, ignore=None):
    """
    实际值的长度大于或等于期望长度
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(expect_value, (int,)), p_string(actual_value, expect_value, ignore)
    assert len(actual_value) >= expect_value, p_string(actual_value, expect_value, ignore)


def length_lt(actual_value, expect_value, ignore=None):
    """
    实际值的长度小于期望长度
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(expect_value, (int,)), p_string(actual_value, expect_value, ignore)
    assert len(actual_value) < expect_value, p_string(actual_value, expect_value, ignore)


def length_lte(actual_value, expect_value, ignore=None):
    """
    实际值的长度小于或等于期望长度
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(expect_value, (int,)), p_string(actual_value, expect_value, ignore)
    assert len(actual_value) <= expect_value, p_string(actual_value, expect_value, ignore)


def contains(actual_value, expect_value, ignore=None):
    """
    期望值包含在实际值中
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(actual_value, (list, tuple, dict, str, bytes)), p_string(actual_value, expect_value, ignore)
    assert expect_value in actual_value, p_string(actual_value, expect_value, ignore)


def contained_by(actual_value, expect_value, ignore=None):
    """
    实际值被包含在期望值中
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert isinstance(expect_value, (list, tuple, dict, str, bytes)), p_string(actual_value, expect_value, ignore)
    assert actual_value in expect_value, p_string(actual_value, expect_value, ignore)


def type_match(actual_value, expect_value, ignore=None):
    """
    实际值的类型与期望值的类型相匹配
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """

    def get_type(name):
        if isinstance(name, type):
            return name
        elif isinstance(name, (str, bytes)):
            try:
                return __builtins__[name]
            except KeyError:
                raise ValueError(name)
        else:
            raise ValueError(name)

    assert isinstance(actual_value, get_type(expect_value)), p_string(actual_value, expect_value, ignore)


def regex_match(actual_value, expect_value, ignore=None):
    """
    正则匹配(从字符串的起始位置匹配)
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    if not isinstance(actual_value, str):
        actual_value = json.dumps(actual_value, ensure_ascii=False)
    if not isinstance(expect_value, str):
        expect_value = json.dumps(expect_value, ensure_ascii=False)
    assert re.match(expect_value, actual_value), p_string(actual_value, expect_value, ignore)


def regex_search(actual_value, expect_value, ignore=None):
    """
    正则匹配(从字符串的任意位置匹配)
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    if not isinstance(actual_value, str):
        actual_value = json.dumps(actual_value, ensure_ascii=False)
    if not isinstance(expect_value, str):
        expect_value = json.dumps(expect_value, ensure_ascii=False)
    assert re.search(expect_value, actual_value), p_string(actual_value, expect_value, ignore)


def startswith(actual_value, expect_value, ignore=None):
    """
    实际值是以期望值开始
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert str(actual_value).startswith(str(expect_value)), p_string(actual_value, expect_value, ignore)


def endswith(actual_value, expect_value, ignore=None):
    """
    实际值是以期望值结束
    Args:
        ignore:
        actual_value: 实际值
        expect_value: 期望值

    Returns:

    """
    assert str(actual_value).endswith(str(expect_value)), p_string(actual_value, expect_value, ignore)


def check(actual_value, expect_value, ignore=None):
    """
    查两个复杂的对象是否一致，支持忽略不进行比较的 key。
    Args:
        actual_value: 实际结果对象。
        expect_value: 期望结果对象。
        ignore (list): 要忽略比较的 key 列表。

    Returns:
        tuple:
            - bool: 表示比较结果的布尔值。True 表示一致，False 表示不一致。
            - list: 包含失败信息的列表。
    """
    failed_info = []
    check_rest = True

    def check_data(actual, expect, ignore=None, path='', current_level_failed_info=None):
        """
        递归比较两个对象。

        Args:
            actual: 实际对象。
            expect: 期望对象。
            ignore (list): 要忽略比较的 key 列表。
            path (str): 当前比较路径。
            current_level_failed_info (list): 当前级别的失败信息列表。

        Returns:
            tuple:
                - bool: 表示比较结果的布尔值。True 表示一致，False 表示不一致。
                - list: 包含失败信息的列表。
        """
        if current_level_failed_info is None:
            current_level_failed_info = []
        ignore = ignore if ignore else []

        dict_type = [dict]
        array_type = [list, tuple, set]

        actual_type = type(actual)
        expect_type = type(expect)

        if actual_type == expect_type:
            check_ret = True

            if actual_type in array_type:
                is_homogeneous = all(isinstance(item, (str, int, float)) for item in actual) and all(
                    isinstance(item, (str, int, float)) for item in expect)

                # 检查长度
                actual_len = len(actual)
                expect_len = len(expect)
                if actual_len != expect_len:
                    current_level_failed_info.append(
                        {"status": "Mismatch", "message": f"预期值长度:{expect_len}, 不等于实际值长度:{actual_len}",
                         "path": path, "actual_value": actual, "expect_value": expect})
                    return False, current_level_failed_info

                # 无序对比
                if is_homogeneous:
                    set_actual = set(actual)
                    set_expect = set(expect)

                    if set_actual == set_expect:
                        return True, current_level_failed_info
                    else:
                        current_level_failed_info.append(
                            {"status": "Mismatch", "message": "预期值不等于实际值", "path": path,
                             "actual_value": actual, "expect_value": expect})
                        return False, current_level_failed_info

                elif all(isinstance(item, dict) for item in actual) and all(
                        isinstance(item, dict) for item in expect):
                    # 循环递归
                    for act_item in actual:
                        match_found = False
                        for exp_item in expect:
                            ret, _ = check_data(act_item, exp_item, ignore=ignore, path=path,
                                                current_level_failed_info=current_level_failed_info)
                            if ret:
                                expect.remove(exp_item)
                                match_found = True
                                break

                        if not match_found:
                            current_level_failed_info.append(
                                {"status": "Mismatch", "message": "预期值与实际不相等", "path": path,
                                 "actual_value": act_item, "expect_value": None})
                            return False, current_level_failed_info

                    return True, current_level_failed_info

                else:
                    # 开始循环递归，并移除对比过的元素
                    for act_item in actual:
                        match_found = False
                        for exp_item in expect:
                            ret, _ = check_data(act_item, exp_item, ignore=ignore, path=path,
                                                current_level_failed_info=current_level_failed_info)
                            if ret:
                                expect.remove(exp_item)
                                match_found = True
                                break

                        if not match_found:
                            current_level_failed_info.append(
                                {"status": "Mismatch", "message": "预期值与实际不相等", "path": path,
                                 "actual_value": act_item, "expect_value": None})
                            return False, current_level_failed_info

                    return True, current_level_failed_info

            elif actual_type in dict_type:
                common_keys = set(actual.keys()) & set(expect.keys())
                for key in sorted(common_keys):
                    if key not in ignore:
                        ret, _ = check_data(actual[key], expect[key], ignore=ignore,
                                            path="{}{}{}".format(path, '.' if path else '', key),
                                            current_level_failed_info=current_level_failed_info)
                        check_ret = ret if not ret and check_ret else check_ret

                extra_keys = set(expect.keys()) - common_keys
                if extra_keys:
                    for key in extra_keys:
                        path_with_key = "{}{}{}".format(path, '.' if path else '', key)
                        if key not in ignore:
                            current_level_failed_info.append(
                                {"status": "Mismatch", "message": "value_not_equal", "path": path_with_key,
                                 "actual_value": None, "expect_value": expect[key]})
                            check_ret = False

                return check_ret, current_level_failed_info

            else:
                if actual != expect:
                    current_level_failed_info.append(
                        {"status": "Mismatch", "message": "value_not_equal", "path": path,
                         "actual_value": actual, "expect_value": expect})
                    return False, current_level_failed_info
                else:
                    return True, current_level_failed_info
        else:
            current_level_failed_info.append(
                {"status": "Mismatch", "message": "预期值类型不等于实际值类型", "path": path,
                 "actual_type": str(actual_type),
                 "expect_type": str(expect_type)})
            return False, current_level_failed_info

    current_level_failed_info = []
    check_ret, _ = check_data(actual_value, expect_value, ignore=ignore,
                              current_level_failed_info=current_level_failed_info)

    if not check_ret:
        failed_info.extend(current_level_failed_info)

    failed_info.append({"ignore_field": ignore})
    check_rest = check_ret if not check_ret and check_rest else check_rest
    assert check_rest is True, p_string(actual_value, expect_value, failed_info)


if __name__ == '__main__':
    # 测试用例
    test_case_list = [
        # 简单数据匹配
        ("1", "1", None),  # 预期：true
        (1, "1", None),  # 预期：true
        (1, 1, None),  # 预期：true
        (1.0, 1, None),  # 预期：true
        # # # 字典匹配（无排除字段）
        ({'a': 1, 'b': 2}, {'a': 1, 'b': 2}, None),  # 预期: 匹配成功
        ({'a': {'c': 1}, 'b': 2}, {'a': {'c': 1}, 'b': 2}, []),  # 预期: 匹配成功

        # # 字典不匹配（部分或全部键值对不一致）
        ({'a': 1, 'b': 2}, {'a': 1, 'b': 3}, None),  # 预期: 不匹配
        ({'a': 1, 'b': 2}, {'a': 1, 'b': 3}, ["b"]),  # 预期: 不匹配
        ({'a': {'c': 1}, 'b': 2}, {'a': {'c': 2}, 'b': 2}, []),  # 预期: 不匹配
        ({'a': {'c': 1}, 'b': 2}, {'a': {'c': 2}, 'b': 2}, ['c']),  # 预期: 匹配成功
        #
        # # 列表中字典匹配（无排除字段）
        ([{'a': 1, 'b': 3}, {'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 1, 'b': 3}, {'a': 1, 'b': 3}],
         [{'a': 1, 'b': 2}, {'a': 1, 'b': 3}, {'a': 1, 'b': 3}, {'a': 1, 'b': 3}, {'a': 1, 'b': 3}], None),  # 预期: 匹配成功

        # 嵌套结构匹配并排除指定字段
        ([{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [1, {'f': 2}]}, 'b': 2}],
         [{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [2, {'f': 2}]}, 'b': 2}], ['c', 'e[0]']),  # 预期: 不匹配
        ([{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [1, {'f': 2}]}, 'b': 2}],
         [{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [2, {'f': 2}]}, 'b': 2}], ['c', 'e']),  # 预期: 匹成功
        ([{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [1, {'f': 2}]}, 'b': 2}],
         [{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [2, {'f': 2}]}, 'b': 2}], ['e']),  # 预期: 匹配成功

        ([{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [1, {'f': 2}, 'xxx']}, 'b': 2}],
         [{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [1, {'f': 2}, 'xxx']}, 'b': 2}], [1, 'xxxx']),  # 预期: 匹配成功
        ([{'b': 2, 'a': 1, 'c': {'d': 3}}, {'a': {'b': 2, 'e': [1, {'f': 2}]}}],
         [{'a': 1, 'b': 2, 'c': {'d': 3}}, {'a': {'e': [2, {'f': 2}]}, 'b': 2}], ['e', "b"]),  # 预期: 匹配成功
        ({'childStock': True, 'childComposeList': [{'childSkuCode': '1684379802095', 'childSkuPriceId': None}],
          'skuCode': '1684379802095'},
         {'childStock': True, 'childComposeList': [
             {'childSkuId': None, 'childSkuName': '', 'childSkuCode': '1684379802095', 'id': None,
              'childSkuPriceId': None}], 'id': None, 'skuId': None},
         ['childSkuId', 'childSkuName', 'id', 'skuId', 'skuCode']),  # 预期: 匹配成功
        # # 简单类型列表匹配
        ([1, 2, 3], [1, 2, 3], None),  # 预期: 匹配成功
        (['a', 'b', 'c'], ['a', 'b', 'c'], None),  # 预期: 匹配成功
        ([{'a': 'a'}, {'b': 'b'}, {'c': 'c'}], [{'b': 'b'}, {'a': 'a'}, {'c': 'c'}], None),  # 预期: 匹配成功
        # 简单类型列表不匹配
        ([1, 2, 3], [1, 2, 4], None),  # 预期: 不匹配
        ([1, 2, 3], [1, 2, 4], [3, 4]),  # 预期: 匹配成功
        (['a', 'b', 'c'], ['a', 'b', 'd'], None),  # 预期: 不匹配
        (['a', 'b', 'c'], ['a', 'b', 'd'], ['c', 'd']),  # 预期: 匹配成功
        ([3, 2, 1], [1, 2, 3], None),  # 预期: 匹配成功
        # 无序字段匹配
        ({'b': 2, 'a': {'c': 1}, }, {'a': {'c': 1}, 'b': 2}, []),  # 预期: 匹配成功
        ({'b': 2, 'a': {'c': 2}}, {'a': {'c': 1}, 'b': 2}, ['c']),  # 预期: 匹配成功
        ({'b': 2, 'a': {'c': 2}, 'd': [3, 2, 1]}, {'a': {'c': 1}, 'b': 2, 'd': [2, 1, 3]}, ['c']),  # 预期: 匹配成功
        ([{"bindingCode": "MoonPromotion", "updateTime": "2013-12-16T23:11:14", "id": 7, "status": 1},
          {"bindingCode": "84097&80462一并销售", "updateTime": "2013-12-16T23:11:13", "id": 1, "status": 1},
          {"bindingCode": "Amway710Promotion", "updateTime": "2013-12-16T23:11:13", "id": 3, "status": 1},
          {"bindingCode": "AtriSummer", "updateTime": "2013-12-16T23:11:13", "id": 5, "status": 1}],

         [{"bindingCode": "MoonPromotion", "updateTime": "2013-12-16T23:11:14", "id": 7, "status": 1},
          {"bindingCode": "AtriSummer", "updateTime": "2013-12-16T23:11:13", "id": 5, "status": 1},
          {"bindingCode": "Amway710Promotion", "updateTime": "2013-12-16T23:11:13", "id": 3, "status": 1},
          {"bindingCode": "84097&80462一并销售", "updateTime": "2013-12-16T23:11:13", "id": 1, "status": 1}], None),
        (["AONV", "AO", "AOHD"], ["AO", "AONV", "AOHD"], None),  # 预期：匹配成功
        ([], ["AO", "AONV", "AOHD"], None),  # 预期：匹配失败，长度不同
        ([], [{"AO": "AO"}, {"AONV": "AONV"}, {"AOHD": "AOHD"}], None),  # 预期：匹配失败,长度不同
        ([], [{"AO": "AO"}, {"AONV": "AONV"}, {"AOHD": "AOHD"}], ['AO', 'AONV', 'AOHD']),  # 预期：匹配失败
        ([{"bindingCode": "222", "updateTime": "2023-11-17T16:20:52", "id": 200016, "status": True},
          {"bindingCode": "87476&87477一并销售", "updateTime": "2022-11-21T18:42:39", "id": 200014, "status": True},
          {"bindingCode": "WOKPromotion", "updateTime": "2022-11-21T18:25:36", "id": 200012, "status": True},
          {"bindingCode": "不粘锅86808&10413&86841", "updateTime": "2021-11-14T00:55:56", "id": 48, "status": True},
          {"bindingCode": "GooseneckKit", "updateTime": "2021-08-19T18:28:26", "id": 43, "status": True},
          {"bindingCode": "GooseneckWaterPurifier", "updateTime": "2021-08-19T18:28:25", "id": 41, "status": True},
          {"bindingCode": "110003", "updateTime": "2020-10-20T12:28:50", "id": 81, "status": True}],
         [{"bindingCode": "222", "updateTime": "2023-11-17T16:20:52", "id": 200016, "status": 1},
          {"bindingCode": "WOKPromotion", "updateTime": "2022-11-21T18:25:36", "id": 200012, "status": 1},
          {"bindingCode": "不粘锅86808&10413&86841", "updateTime": "2021-11-14T00:55:56", "id": 48, "status": 1},
          {"bindingCode": "87476&87477一并销售", "updateTime": "2022-11-21T18:42:39", "id": 200014, "status": 1},
          {"bindingCode": "GooseneckKit", "updateTime": "2021-08-19T18:28:26", "id": 43, "status": 1},
          {"bindingCode": "GooseneckWaterPurifier", "updateTime": "2021-08-19T18:28:25", "id": 41, "status": 1},
          {"bindingCode": "110003", "updateTime": "2020-10-20T12:28:50", "id": 81, "status": 1}], ["status"]),
        # 预期，匹配成功
        ([{"tagCode": "AO", "role": "", "productCode": "9752_base", "startTime": "2021-05-29T19:09:46",
           "endTime": "2026-11-19T19:09:46", "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"},
          {"role": "ABO", "tagCode": "PROMOTIONS", "productCode": "9752_base", "startTime": "2024-01-29T15:09:16",
           "endTime": "2024-03-29T15:09:16", "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"}],
         [{"tagCode": "AO", "role": "", "productCode": "9752_base", "startTime": "2021-05-29T19:09:46",
           "endTime": "2026-11-19T19:09:46", "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"},
          {"tagCode": "PROMOTIONS", "role": "ABO", "productCode": "9752_base", "startTime": "2024-01-29T15:09:16",
           "endTime": "2024-03-29T15:09:16", "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"}], None),
        # 预期，匹配成功
        ([{"tagCode": "PROMOTIONS", "role": "ABO", "productCode": "20508_base",
           "endTime": "2024-04-03T11:12:18", "skuCode": "20508", "channelCode": "DEFAULT"}],
         [{"tagCode": "PROMOTIONS", "role": "ABO", "productCode": "20508_base", "startTime": "2024-02-03T11:12:18",
           "endTime": "2024-04-03T11:12:18", "skuCode": "20508", "channelCode": "DEFAULT"}], ["startTime"]),  # 预期，匹配成功

        ([
             {"tagCode": "AO", "role": "", "productCode": "9752_base", "startTime": "2021-05-29T19:09:46",
              "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"},

             {"role": "ABO", "tagCode": "PROMOTIONS", "productCode": "9752_base", "startTime": "2024-01-29T15:09:16",
              "endTime": "2024-03-29T15:09:16", "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"}
         ],
         [
             {"tagCode": "AO", "role": "", "productCode": "9752_base", "startTime": "2021-05-29T19:09:46",
              "endTime": "2026-11-19T19:09:46", "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"},
             {"tagCode": "PROMOTIONS", "role": "ABO", "productCode": "9752_base", "startTime": "2024-01-29T15:09:16",
              "skuCode": "AUQMSU7iu4TgJLoJL", "channelCode": "DEFAULT"}
         ], ["endTime"]),  # 预期，匹配成功

        ([{"micro_sort_value": 257, "sort_number_value": 10238, "skuCode": "41374"},
          {"micro_sort_value": 257, "sort_number_value": 10238, "skuCode": "41375"},
          {"micro_sort_value": 252, "sort_number_value": 10233, "skuCode": "999785"},
          {"micro_sort_value": 245, "sort_number_value": 10223, "skuCode": "41131"},
          {"micro_sort_value": 244, "sort_number_value": 10221, "skuCode": "41333"},
          {"micro_sort_value": 243, "sort_number_value": 10220, "skuCode": "41211"},
          {"micro_sort_value": 243, "sort_number_value": 10220, "skuCode": "41213"},
          {"micro_sort_value": 242, "sort_number_value": 10218, "skuCode": "40822"},
          {"micro_sort_value": 242, "sort_number_value": 10218, "skuCode": "40823"},
          {"micro_sort_value": 242, "sort_number_value": 10218, "skuCode": "40824"}],

         [{"micro_sort_value": 257, "sort_number_value": 10238, "skuCode": "41374"},
          {"micro_sort_value": 257, "sort_number_value": 10238, "skuCode": "41375"},
          {"micro_sort_value": 252, "sort_number_value": 10233, "skuCode": "999785"},
          {"micro_sort_value": 245, "sort_number_value": 10223, "skuCode": "41131"},
          {"micro_sort_value": 244, "sort_number_value": 10221, "skuCode": "41333"},
          {"micro_sort_value": 243, "sort_number_value": 10220, "skuCode": "41211"},
          {"micro_sort_value": 243, "sort_number_value": 10220, "skuCode": "41213"},
          {"micro_sort_value": 242, "sort_number_value": 10218, "skuCode": "40822"},
          {"micro_sort_value": 242, "sort_number_value": 10218, "skuCode": "40823"},
          {"micro_sort_value": 242, "sort_number_value": 10218, "skuCode": "40824"}], None)  # 预期，匹配成功
    ]
    # 运行测试用例
    for case in test_case_list:
        exp, act, exclude_fields = case
        try:
            check(exp, act, exclude_fields)
            print(f'Passed: {case}')
        except Exception as e:
            print(f'Failed: {case}, {e}')
