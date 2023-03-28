import os
from .id_card import RandomIdCard

idcard = RandomIdCard(csv_path=f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}")
