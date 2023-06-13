#-*-coding:utf-8-*-
import csv
import random


class RandomPhone(object):
    """随机电话号码"""
    def __init__(self, csv_path=""):
        self.tele_phone_csv = csv.reader(open("{0}phone_area.csv".format(csv_path), "r", encoding='utf-8'))
        self.tele_phone_head = next(self.tele_phone_csv)
        self.tele_phone_data = [item for item in self.tele_phone_csv]
    
    def _number_start(self):
        """获取手机号码前三位"""
        one_number = 1
        two_number = [3, 4, 5, 7, 8][random.randint(0, 4)]
        three_number = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9),
        }[two_number]
        return one_number, two_number, three_number

    def get_mobile_number(self):
        """随机获取手机号码"""
        one_number, two_number, three_number = self._number_start()
        phone_number = [str(one_number), str(two_number), str(three_number)]
        phone_number.extend([str(random.randint(0, 9)) for n in range(8)])
        return "".join(phone_number)
    
    def get_tele_number(self, area_ids=None):
        if area_ids:
            area_id = random.choice(area_ids)
            if len(area_id) != 3 or len(area_id) != 4:
                area_id  = str(random.choice([item[0] for item in self.tele_phone_data]))
        else:
            area_id = str(random.choice([item[0] for item in self.tele_phone_data]))
            
        if len(area_id) == 3:
            number = [str(random.randint(0, 9)) for n in range(8)]
            return "{0}-{1}".format(area_id, "".join(number))
        elif len(area_id) == 4:
            number = [str(random.randint(0, 9)) for n in range(7)]
            return "{0}-{1}".format(area_id, "".join(number))
        

if __name__ == "__main__":
    random_phone_obj = RandomPhone()

    for i in range(10):        # 随机生成10个电话号和手机
        tele_number = random_phone_obj.get_tele_number()
        mobile_number = random_phone_obj.get_mobile_number()
        print("电话: {0}  手机: {1}".format(tele_number, mobile_number))
        