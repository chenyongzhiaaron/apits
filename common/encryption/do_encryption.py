import sys

sys.path.append("./common")
sys.path.append("../")
from common.tools.logger import MyLog
from ext_script import sign


def do_encrypt(method, data):
    if method == "MD5":
        try:
            res = sign.md5_sign(data)
        except Exception as e:
            MyLog().my_log(f"MD5加密失败:{e},{data}", "error")
        else:
            return res
    elif method == "sha1":
        try:
            res = sign.sha1_sign(data)
        except Exception as e:
            MyLog().my_log(f"sha1加密失败参数:{e},{data}", "error")
        else:
            return res


if __name__ == '__main__':
    print(do_encrypt("sha1", {}))
