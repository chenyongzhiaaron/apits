# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_json.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 14:02
# -------------------------------------------------------------------------------
import json

from common.bif_functions import logger

__all__ = ['json_dumps', 'json_loads']


@logger.log_decorator()
def json_dumps(obj):
    """
    Serialize ``obj`` to a JSON formatted ``str``.
    Args:
        obj:

    Returns:

    """
    return json.dumps(obj, ensure_ascii=False)


@logger.log_decorator()
def json_loads(obj):
    """
    Deserialize ``obj`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python object.
    Args:
        obj:

    Returns:

    """
    return json.loads(obj)
