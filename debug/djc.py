
class RootModel:
    _mapping_info = {}

    def __init__(self, **kwargs):
        """
        定义最基本的初始化方式
        :param kwargs: 参数字典
        """
        for k, v in kwargs.items():
            key = self.__class__._load_mapping_info(k)
            if key in self.__dict__.keys():
                self.__setattr__(key, v)

    @classmethod
    def _load_mapping_info(cls, key):
        """
        获取字段映射
        :param key: 键
        :return: 映射后的键
        """
        if key in cls._mapping_info.keys():
            return cls._mapping_info.get(key)
        else:
            return key


class A(RootModel):
    def __init__(self, **kwargs):
        self.a = []
        super().__init__(**kwargs)


class B(A):
    def __init__(self, **kwargs):
        self.b = []
        super().__init__(**kwargs)


class C(A):
    def __init__(self, **kwargs):
        self.c = []
        super().__init__(**kwargs)


class D(B, C):
    def __init__(self, **kwargs):
        # self.d = []
        super().__init__(**kwargs)


if __name__ == '__main__':
    d = D(**{"b": 4})
    print(d)
