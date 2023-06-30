def sum(x, y):
    return x + y


def generate():
    for i in range(4):
        yield i


res = generate()

for n in [0, 1, 2, 3]:
    base =(sum(i, n) for i in res)


print(base)
