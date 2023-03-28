import base64
import hashlib


class HashTools:
    @staticmethod
    def hash_tools(file):
        with open(file, "rb") as f:
            # 获取 base64 码
            base64_data = base64.b64encode(f.read())
        with open(file, "rb") as f:
            md = hashlib.md5()
            md.update(f.read())
            res_md5 = md.hexdigest()

        return str(base64_data, "utf-8"), res_md5
