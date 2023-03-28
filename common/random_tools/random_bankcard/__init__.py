import os
from .bankcard import RandomBankCard

bankcard = RandomBankCard(csv_path=f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}")
