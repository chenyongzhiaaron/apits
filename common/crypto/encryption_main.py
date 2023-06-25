import sys

sys.path.append("./common")
sys.path.append("../")
from common.crypto import logger
from extensions import sign
from common.crypto.encryption_rsa import Rsa


@logger.log_decorator()
def do_encrypt(method, data):
	if method == "MD5":
		try:
			res = sign.md5_sign(data)
			return res
		except Exception as e:
			logger.error(f"MD5 加密失败：{e}")
	elif method == "sha1":
		try:
			res = sign.sha1_sign(data)
			return res
		except Exception as e:
			logger.error(f"sha1 加密失败：{e}")
	elif method == 'rsa':
		try:
			res = Rsa(data).rsa_encrypt()
			return res
		except Exception as e:
			logger.error(f"Rsa 加密失败：{e}")
	else:
		return data


if __name__ == '__main__':
	do_encrypt("sha1", {})
