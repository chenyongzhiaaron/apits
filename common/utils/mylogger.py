"""
@author: 测试玩家勇哥
@contact:262667641@qq.com
@file:mylogger.py
@time:2023/6/12 9:59
@desc: 日志封装
"""
import os
from functools import wraps
from time import perf_counter

from loguru import logger

from common.config import Config
from common.utils.singleton import singleton

LOG_DIR = Config.log_path


@singleton
class MyLogger:
	"""
	根据时间、文件大小切割日志
	"""
	
	def __init__(self, log_dir=LOG_DIR, max_size=20, retention='7 days'):
		self.log_dir = log_dir
		self.max_size = max_size
		self.retention = retention
		self.logger = self.configure_logger()
	
	def configure_logger(self):
		"""
		Returns:
		"""
		# 创建日志目录
		os.makedirs(self.log_dir, exist_ok=True)
		
		shared_config = {
			"level": "ERROR",
			"enqueue": True,
			"backtrace": False,
			"format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
		}
		
		# 添加按照日期和大小切割的文件 handler
		logger.add(
			sink=f"{self.log_dir}/{{time:YYYY-MM-DD}}.log",
			rotation=f"{self.max_size} MB",
			retention=self.retention,
			**shared_config
		)
		
		# 配置按照等级划分的文件 handler 和控制台输出
		logger.add(sink=self.get_log_path, **shared_config)
		
		return logger
	
	def get_log_path(self, message: str) -> str:
		"""
		根据等级返回日志路径
		Args:
		    message:
		Returns:
		"""
		log_level = message.record["level"].name.lower()
		log_file = f"{log_level}.log"
		log_path = os.path.join(self.log_dir, log_file)
		
		return log_path
	
	def __getattr__(self, level: str):
		return getattr(self.logger, level)
	
	def log_decorator(self, msg="快看，异常了，别唧唧哇哇，快排查！！"):
		"""
		 日志装饰器，记录函数的名称、参数、返回值、运行时间和异常信息
	    Args:
		logger: 日志记录器对象
	    Returns:
		"""
		
		def decorator(func):
			@wraps(func)
			def wrapper(*args, **kwargs):
				# self.logger.info(f'-----------分割线-----------')
				self.logger.info(f'| 调用函数： {func.__name__} | args: {args} kwargs:{kwargs}')
				start = perf_counter()  # 开始时间
				try:
					result = func(*args, **kwargs)
					end = perf_counter()  # 结束时间
					duration = end - start
					self.logger.info(f"| 结束调用函数： {func.__name__}, duration：{duration:4f}s")
					return result
				except Exception as e:
					self.logger.error(f"| called {func.__name__} | error: {msg}: {e}")
			
			# self.logger.info(f"-----------分割线-----------")
			
			return wrapper
		
		return decorator


if __name__ == '__main__':
	log = MyLogger()
	
	
	@log.log_decorator("勇哥也不知道错在哪里")
	def test_zero_division_error(a, b):
		return a / b
	
	
	for i in range(1000):
		log.error('错误信息')
		log.critical('严重错误信息')
		test_zero_division_error(1, 0)
		log.debug('调试信息')
		log.info('普通信息')
		log.success('成功信息')
		log.warning('警告信息')
