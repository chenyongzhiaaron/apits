import os
from .email import RandomEmail

email = RandomEmail(csv_path=f"{os.path.dirname(os.path.realpath(__file__))}{os.sep}")
