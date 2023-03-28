# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_json.py
# Description:
# Author:       XiangjunZhao
# EMAIL:        2419352654@qq.com
# Date:         2021/1/12 14:02
# -------------------------------------------------------------------------------
import json
import logging

__all__ = ['json_dumps', 'json_loads']

logger = logging.getLogger(__name__)


def json_dumps(obj):
    """
    Serialize ``obj`` to a JSON formatted ``str``.
    Args:
        obj:

    Returns:

    """
    logger.info(f'执行方法：json_dumps({obj})')
    return json.dumps(obj, ensure_ascii=False)


def json_loads(obj):
    """
    Deserialize ``obj`` (a ``str``, ``bytes`` or ``bytearray`` instance containing a JSON document) to a Python object.
    Args:
        obj:

    Returns:

    """
    logger.info(f'执行方法：json_loads({obj})')
    return json.loads(obj)
