import csv
import random
import pypinyin


class RandomEmail(object):
	'''随机Email'''
	
	def __init__(self, csv_path=""):
		'''
		Args:
		    email_csv: 邮箱csv文件
		    email_head: 邮箱csv字段名称
		    email_data: 邮箱数据集
		'''
		self.email_csv = csv.reader(open("{0}free_email.csv".format(csv_path), "r", encoding='utf-8'))
		self.email_head = next(self.email_csv)
		self.email_data = [item for item in self.email_csv]
	
	def _chinese_to_pinyin(self, chinese_name):
		'''中文转拼音
		Args：
		    chinese_name: str, 中文名字
		Returns:
		    pinyin_name: str, 拼音名字
		'''
		pinyin_name = ''
		for i in pypinyin.pinyin(chinese_name, style=pypinyin.NORMAL):
			pinyin_name += ''.join(i)
		return pinyin_name
	
	def get_email(self, chinese_name, email_types=None):
		'''随机生成邮箱地址,
		Args:
		    chinese_name: str, 中文名字
		    email_types: list, ["163"]类型为@163.com的邮箱地址, 随机范围
		Returns:
		    email: str, 邮箱地址
		'''
		if email_types:
			email_address = [item[1] for item in self.email_data if item[0] in email_types]
		else:
			email_address = [item[1] for item in self.email_data]
		email = self._chinese_to_pinyin(chinese_name) + random.choice(email_address)
		return email


if __name__ == "__main__":
	random_email_obj = RandomEmail()
	name_list = ["焦荷丹", "李咏叶", "罗红", "蔡朋", "杨浩伦", "李峰", "牛玉美", "孔群", "李巧"]
	for name in name_list:
		email = random_email_obj.get_email(name, email_types=["sina_cn", "gmail"])
		print(email)
