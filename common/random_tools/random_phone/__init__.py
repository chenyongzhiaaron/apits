import os
from .phone import RandomPhone

phone = RandomPhone(csv_path=f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}")
