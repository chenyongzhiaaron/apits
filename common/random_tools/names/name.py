#-*-coding:utf-8-*-
import csv
import random


class RandomName(object):
    '''随机姓名'''
    def __init__(self, csv_path=""):
        '''
        Args:
            last_name_csv: 姓氏csv文件
            last_name_head: 姓氏csv字段名称
            last_name_data: 姓氏数据集
            first_name_girl_csv: 女孩名字csv文件
            first_name_girl_head: 女孩名字csv字段名称
            first_name_girl_data: 女孩名字数据集
            first_name_boy_csv: 男孩名字csv文件
            first_name_boy_head: 男孩名字csv字段名称
            first_name_boy_data: 男孩名字csv文件
        '''
        self.last_name_csv = csv.reader(open("{0}last_name.csv".format(csv_path), "r", encoding='utf-8'))
        self.last_name_head = next(self.last_name_csv)
        self.last_name_data = [item for item in self.last_name_csv]

        self.first_name_girl_csv = csv.reader(open("{0}first_name_girl.csv".format(csv_path), "r", encoding='utf-8'))
        self.first_name_girl_head = next(self.first_name_girl_csv)
        self.first_name_girl_data = [item for item in self.first_name_girl_csv]

        self.first_name_boy_csv = csv.reader(open("{0}first_name_boy.csv".format(csv_path), "r", encoding='utf-8'))
        self.first_name_boy_head = next(self.first_name_boy_csv)
        self.first_name_boy_data = [item for item in self.first_name_boy_csv]

    def get_girl(self, name_len=None):
        '''随机生成女孩名字
        Args：
            name_len: int, 名字长度
        Returns:
            name: str, 女孩名字
        '''
        name = random.choices([item[1] for item in self.last_name_data], weights=[int(item[0]) for item in self.last_name_data])[0]
        name_length = name_len if name_len else random.randint(1, 2)
        for i in range(name_length):
            name +=  random.choices([item[1] for item in self.first_name_girl_data], weights=[int(item[0]) for item in self.first_name_girl_data])[0]
        return name
    
    def get_boy(self, name_len=None):
        '''随机生成男孩名字
        Args：
            name_len: int, 名字长度
        Returns:
            name: str, 男孩名字
        '''
        name = random.choices([item[1] for item in self.last_name_data], weights=[int(item[0]) for item in self.last_name_data])[0]
        name_length = name_len if name_len else random.randint(1, 2)
        for i in range(name_length):
            name +=  random.choices([item[1] for item in self.first_name_boy_data], weights=[int(item[0]) for item in self.first_name_boy_data])[0]
        return name


if __name__ == "__main__":
    random_name_obj = RandomName()

    for i in range(10):                     # 生成10个姓名.
        if random.randint(0, 1) == 0:       # 随机男女, 0表示女, 1表示男.
            print("{:6}\t{:2}".format(random_name_obj.get_girl(), "女"))
        else:
            print("{:6}\t{:2}".format(random_name_obj.get_boy(), "男"))
