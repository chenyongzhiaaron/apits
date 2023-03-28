# -*- coding:utf-8 -*-
import re
import sys

sys.path.append("./")
sys.path.append("./common")


class Dependence:
    dependence = {}  # 定义依赖表
    PATTERN = re.compile(r"{{(.*?)}}")  # 预编译正则表达式
    pattern = re.compile(r'({)')

    def update_dep(self, key, value):
        """更新依赖表"""
        self.dependence[f"{{{{{key}}}}}"] = value

    def get_dep(self, key=None):
        """获取依赖表 或 依赖表中key对应的值"""
        return self.dependence if key else self.dependence.get(key)

    def set_dep(self, value):
        """设置依赖表"""
        self.dependence = value


if __name__ == '__main__':
    dependence = getattr(Dependence, "dependence")
    print(dependence)
    setattr(Dependence, "dependence", {"123": "32"})
    dependence = getattr(Dependence, "dependence")
    print(dependence)
