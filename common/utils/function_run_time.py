import time
from functools import wraps


def fn_time(func):
	def inner(*args, **kwargs):
		t0 = time.time()
		func(*args, **kwargs)
		t1 = time.time()
		print(f"{func.__name__}总共运行:{str(t1 - t0)}")
		# return func(*args, **kwargs)
	
	return inner
