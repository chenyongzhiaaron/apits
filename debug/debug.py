#!/usr/bin/env python
# encoding: utf-8
"""
@author: kira
@contact: 262667641@qq.com
@file: debug.py
@time: 2023/3/29 11:40
@desc:
"""
import random
import re
import types

import jsonpath

from common.dependence import Dependence
from common.comparator import loaders

# lo = loaders.set_bif_fun()
# pa = Dependence.PATTERN
# di = Dependence.get_dep()
# patten = re.compile(r"\{\{(\w+\(\))\}\}")
# jst = '{{get_current_time()}}'
# ret = patten.search(jst)
# print(ret)
# if ret:
#     if jst in di.keys():
#         print(di.get(jst))
#         jst = jst.replace(jst, di.get(jst)())
# print(jst)

#
# print([name for name in dir(random) if callable(getattr(random, name))])

# result = jsonpath.jsonpath(resp_obj if isinstance(resp_obj, (dict, list)) else json.dumps(resp_obj), expr)

