# coding: utf-8

# -------------------------------------------------------------------------------
# Name:         bif_time.py
# Description:
# Author:       kira
# EMAIL:        262667641@qq.com
# Date:         2021/1/12 14:03
# -------------------------------------------------------------------------------
import time

from common.bif_functions import logger

__all__ = ['get_timestamp', 'ms_fmt_hms']


@logger.log_decorator("错误原因：时间戳的长度只能在10到16位之间，默认返回长度为13位的时间戳")
def get_timestamp(length=13):
	"""
	获取时间戳字符串，长度最多为16位；默认13位
	Args:
	    length: 时间戳长度
    
	Returns:
 
	"""
	if isinstance(length, (int,)) and 10 <= length <= 16:
		power = length - 10
		timestamp = time.time()
		return int(timestamp * 10 ** power)
	else:
		get_timestamp(13)


@logger.log_decorator()
def ms_fmt_hms(ms):
	"""
	将毫秒转换成 h:m:s.ms格式字符串
	Args:
	    ms:
    
	Returns:
 
	"""
	ms = int(ms)
	sec = ms // 1000
	hour = sec // 3600
	minute = (sec - hour * 3600) // 60
	sec = sec % 60
	ms = ms % 1000
	
	hour = str(hour).rjust(2, '0')
	minute = str(minute).rjust(2, '0')
	sec = str(sec).rjust(2, '0')
	ms = str(ms).rjust(2, '0')
	return f"{hour}:{minute}:{sec}.{ms}"


if __name__ == '__main__':
	get_timestamp()
