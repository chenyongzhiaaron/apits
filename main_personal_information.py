# -*-coding:utf-8-*-
import random
import sys

# sys.path.append('./')
# sys.path.append('./common')

from prettytable import PrettyTable
from faker import Faker
from common.random_tools.names import name
from common.random_tools.emails import email
from common.random_tools.phone_numbers import phone
from common.random_tools.identification import idcard
from common.random_tools.credit_cards import bankcard
from common.random_tools.credit_identifiers import credit_identifier

if __name__ == "__main__":
    f = Faker(locale="zh_CN")
    number = int(input("请输入大于2的数字以便生成随机用户信息:"))
    table = PrettyTable(
        ("序号", "用户名", "性别", "年龄", "生日", "身份证", "银行卡或信用卡", "座机", "手机号", "邮箱", "地址",
         "统一社会信用代码"))
    for i in range(number):
        sex_id = random.randint(0, 1)
        user_name = name.get_girl() if sex_id == 0 else name.get_boy()
        user_sex = "女" if sex_id == 0 else "男"
        user_id_card = idcard.get_generate_id(sex=sex_id)
        user_age = str(idcard.get_age(user_id_card))
        user_birthday = idcard.get_birthday(user_id_card)
        user_tele = phone.get_tele_number()
        user_mobile = phone.get_mobile_number()
        user_email = email.get_email(user_name)
        user_address = f.address()
        user_bank_card = bankcard.get_bank_card()
        try:
            unified_social_credit_code = credit_identifier.unified_social_credit_code()
        except:
            unified_social_credit_code = None
        else:
            table.add_row([i, user_name, user_sex, user_age, user_birthday, user_id_card, user_bank_card, user_tele,
                           user_mobile, user_email, user_address, unified_social_credit_code])
    print(table)
