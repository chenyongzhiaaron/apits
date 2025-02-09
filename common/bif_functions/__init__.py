# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         __init__.py.py
# Description:
# Author:       chenyongzhi
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 14:02
# -------------------------------------------------------------------------------
from common.log_utils.mylogger import MyLogger

logger = MyLogger()
from .bif_datetime import *
from .bif_hashlib import *
from .bif_json import *
from .bif_list import *
from .bif_other import *
from .bif_re import *
from .bif_str import *
from .bif_time import *
from .bif_faker import *
