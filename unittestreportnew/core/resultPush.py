import base64
import hashlib
import hmac
import smtplib
import time
import urllib.parse
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests

from config import Config

#
#
# if __name__ == '__main__':
#     # r'D:\app\apitest\cases\cases\test_cases.xlsx',r"D:\app\apitest\OutPut\reports\report.html"
#     sm = SendEmail()
#     sm.send_mail("111", [])
