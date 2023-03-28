# -*-coding:utf-8-*-
import re
import csv
import random
from datetime import datetime, timedelta


class IdCard(object):
    """身份证号"""

    id_number_15_regex = r"^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$"
    id_number_18_regex = r"^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$"

    def __init__(self, id_number):
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    @property
    def birthday(self):
        """通过身份证号获取出生日期"""
        birth_year = str(self.birth_year)
        birth_month = "0" + str(self.birth_month) if len(str(self.birth_month)) == 1 else str(self.birth_month)
        birth_day = "0" + str(self.birth_day) if len(str(self.birth_day)) == 1 else str(self.birth_day)

        return "{0}-{1}-{2}".format(birth_year, birth_month, birth_day)

    @property
    def age(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    @property
    def sex(self):
        """通过身份证号获取性别, 0: 女生, 1: 男生"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @classmethod
    def verify_id(cls, id_number):
        """校验身份证是否正确
        Args：
            id_number: str, 身份证号.
        Returns:
            bool
        """
        if re.match(cls.id_number_18_regex, id_number):
            check_digit = cls(id_number).get_check_digit()
            return str(check_digit) == id_number[-1]
        else:
            return bool(re.match(cls.id_number_15_regex, id_number))


class RandomIdCard(object):
    """随机身份证号"""

    def __init__(self, csv_path=""):
        """
        Args:
            area_csv: 地区编号和名称csv文件
            area_head: 地区编号和名称csv字段名称
            area_data: 地区编号和名称数据集
            id_number_15_regex: 15位身份证号码校验正则
            id_number_18_regex: 18位身份证号码校验正则
        """
        self.area_csv = csv.reader(open("{0}area.csv".format(csv_path), "r", encoding='utf-8'))
        self.area_head = next(self.area_csv)
        self.area_data = [item for item in self.area_csv]

    def get_generate_id(self, sex=None, birth_days=None, arrer_numbers=None):
        """随机生成身份证号, 
        Args：
            sex: int, 0表示女性, 1表示男性.
            birth_days: list, ["1990-01-01"]长度为1表示生成指定日期身份证号, ["1990-01-01", "1995-12-31"]长度为2表示生成指定范围日期身份证号.
            arrer_numbers: list, 生成指定区域编号的身份证号, 默认全部.
        Returns:
            id_number: str, 身份证号.
        """
        if not arrer_numbers:
            arrer_number = str(random.choice([item[0] for item in self.area_data]))
        else:
            arrer_number = str(random.choice(arrer_numbers))

        if isinstance(birth_days, list) and len(birth_days) == 1:
            birth_day = datetime.strftime(datetime.strptime(birth_days[0], "%Y-%m-%d"), "%Y%m%d")
        elif isinstance(birth_days, list) and len(birth_days) == 2:
            start, end = datetime.strptime(birth_days[0], "%Y-%m-%d"), datetime.strptime(birth_days[1], "%Y-%m-%d")
            birth_day = datetime.strftime(start + timedelta(random.randint(0, (end - start).days)), "%Y%m%d")
        else:
            start, end = datetime.strptime("1960-01-01", "%Y-%m-%d"), datetime.strptime("2000-12-31", "%Y-%m-%d")
            birth_day = datetime.strftime(start + timedelta(random.randint(0, (end - start).days)), "%Y%m%d")

        if not sex:
            sex = random.randint(0, 1)

        id_number = str(arrer_number)
        id_number += birth_day
        id_number += str(random.randint(10, 99))
        id_number += str(random.randrange(sex, 10, step=2))
        return id_number + str(IdCard(id_number).get_check_digit())

    def get_birthday(self, id_number):
        return IdCard(id_number).birthday

    def get_age(self, id_number):
        return IdCard(id_number).age

    def get_sex(self, id_number):
        return IdCard(id_number).sex

    def get_area_id(self, id_number):
        return IdCard(id_number).area_id

    def get_area_name(self, id_number):
        area_ids = [int(item[0]) for item in self.area_data]
        area_names = [item[1] for item in self.area_data]
        return area_names[area_ids.index(IdCard(id_number).area_id)]


if __name__ == "__main__":
    random_idcard_obj = RandomIdCard()

    print(random_idcard_obj.get_generate_id())  # 随机生成男或女, 出生日期在1960~2000, 区域地址为全国的身份证号.
    print(random_idcard_obj.get_generate_id(sex=1))  # 生成性别为男的身份证号, 出生日期在1960~2000, 区域地址为全国的身份证号.
    print(random_idcard_obj.get_generate_id(birth_days=["1993-03-18"]))  # 随机生成男或女, 出生日期是"1993-03-18", 区域地址为全国的身份证号.
    print(random_idcard_obj.get_generate_id(
        birth_days=["1990-01-01", "1995-12-31"]))  # 随机生成男或女, 出生日期在1990~1995之间, 区域地址为全国的身份证号. 
    print(random_idcard_obj.get_generate_id(arrer_numbers=["110108"]))  # 随机生成男或女, 出生日期在1960~2000, 区域地址为北京海淀区的身份证号.

    id_number = random_idcard_obj.get_generate_id()
    print(random_idcard_obj.get_area_id(id_number))  # 根据身份证号获取区域地址编号.
    print(random_idcard_obj.get_area_name(id_number))  # 根据身份证号获取区域地址.
    print(random_idcard_obj.get_birthday(id_number))  # 根据身份证号获取出生日期.
    print(random_idcard_obj.get_age(id_number))  # 根据身份证号获取年龄.
    print("男" if random_idcard_obj.get_sex(id_number) else "女")  # 根据身份证号获取性别, 0表示女, 1表示男.
