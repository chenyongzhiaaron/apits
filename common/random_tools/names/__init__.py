import os
from .name import RandomName

name = RandomName(csv_path=f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}")
