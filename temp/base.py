class Fa:
    maxDiff = None
    age = 19

    def get_age(self):
        print(self.age)


class So(Fa):
    age = 20


if __name__ == '__main__':
    So().get_age()
    Fa().get_age()
