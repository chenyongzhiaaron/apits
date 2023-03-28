# -*- coding:utf-8 -*-
import re
import sys

sys.path.append("./")
sys.path.append("./common")


class Dependence:
    dependence = {}  # 定义依赖表
    PATTERN = re.compile(r"{{(.*?)}}")  # 预编译正则表达式
    pattern = re.compile(r'({)')

    def update_dependence(self, key, value):
        self.dependence[f"{{{{{key}}}}}"] = value

    def get_dependence(self):
        return self.dependence


if __name__ == '__main__':
    dependence = getattr(Dependence, "dependence")
    print(dependence)
    setattr(Dependence, "dependence", {"123": "32"})
    dependence = getattr(Dependence, "dependence")
    print(dependence)
