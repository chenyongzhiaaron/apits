import csv
import random


class RandomBankCard(object):
    def __init__(self, csv_path=""):
        self.card_bin_csv = csv.reader(open("{0}cardbin.csv".format(csv_path), "r", encoding='utf-8'))
        self.card_bin_head = next(self.card_bin_csv)
        self.card_bin_data = [item for item in self.card_bin_csv]
        # print(self.card_bin_data)

    def _get_bank_card(self, bank_name=""):
        bank_card_list = []
        if bank_name:
            for item in self.card_bin_data:
                if item[0] == bank_name and item[2] == "银行卡":
                    bank_card_list.append(item)
        else:
            for item in self.card_bin_data:
                if item[2] == "银行卡":
                    bank_card_list.append(item)
        return bank_card_list

    def _get_credit_card(self, bank_name=""):
        bank_card_list = []
        if bank_name:
            for item in self.card_bin_data:
                if item[0] == bank_name and item[2] == "信用卡":
                    bank_card_list.append(item)
        else:
            for item in self.card_bin_data:
                if item[2] == "信用卡":
                    bank_card_list.append(item)
        return bank_card_list

    def _get_check_num(self, bank_card):
        check_sum = 0
        for i in bank_card[-1::-2]:
            for m in str(int(i) * 2):
                check_sum = check_sum + int(m)

        for j in bank_card[-2::-2]:
            check_sum = check_sum + int(j)

        if check_sum % 10 == 0:
            check_num = '0'
        else:
            check_num = str(10 - check_sum % 10)
        return check_num

    def _get_card_num(self, bank_item):
        bin_num = bank_item[1]
        mid_num = "".join([str(random.randint(0, 9)) for i in range(int(bank_item[3]) - len(bin_num))])
        check_num = self._get_check_num("".join([bin_num, mid_num]))
        return "".join([bin_num, mid_num, check_num])

    def get_bank_card(self, bank_name="", bank_type=""):
        if bank_type == "银行卡":
            bank_card = self._get_bank_card(bank_name)
        elif bank_type == "信用卡":
            bank_card = self._get_credit_card(bank_name)
        else:
            bank_card = self.card_bin_data

        bank_card_num = self._get_card_num(random.choice(bank_card))
        return bank_card_num


if __name__ == '__main__':
    bank_card_obj = RandomBankCard()
    print(bank_card_obj.get_bank_card())
