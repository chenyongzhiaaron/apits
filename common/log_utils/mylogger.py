"""
@author: 测试玩家勇哥
@contact:262667641@qq.com
@file:mylogger.py
@time:2023/6/12 9:59
@desc: 日志封装
"""
import os

from loguru import logger

from common.utils.decorators import singleton
from config.config import Config


@singleton
class MyLogger:
	"""
	根据时间、文件大小以及日志等级切割日志
	"""
	
	def __init__(self, log_dir=Config.LOG_PATH):
		self.log_dir = log_dir
		self.logger = self.configure_logger()
	
	def configure_logger(self):
		"""
		Returns:
		"""
		# 创建日志目录
		os.makedirs(self.log_dir, exist_ok=True)
		shared_config = {
			"level": "DEBUG",
			"enqueue": True,
			"backtrace": False,
			"encoding": "utf-8",
			"rotation": "50 MB",
			"retention": "7 days",
			"format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {file} | {module} | {message}",
		}
		# 添加按照等级划分以及日期和大小切割的文件 handler
		for level in ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"]:
			logger.add(
				sink=self.get_log_path(f"{level}.log"),
				filter=self.level_filter(level),  # 使用 level_filter 方法
				**shared_config
			)
		return logger
	
	def level_filter(self, level):
		"""过滤日志等级"""
		
		def is_level(record):
			return record["level"].name == level
		
		return is_level
	
	def get_log_path(self, filename):
		return os.path.join(self.log_dir, filename)
	
	def trace(self, msg):
		self.logger.trace(msg)
	
	def __getattr__(self, level):
		return getattr(self.logger, level)
	
	def catch(self, *args, **kwargs):
		return self.logger.catch(*args, **kwargs)


if __name__ == '__main__':
	log = MyLogger()
	
	
	@log.catch
	def test_zero_division_error(a, b):
		return a / b
	
	
	for i in range(1):
		test_zero_division_error(1, 0)
		log.debug('调试信息')
		log.info('普通信息')
		log.success('成功信息')
		log.warning('警告信息')
		log.error('错误信息')
		log.critical('严重错误信息')
