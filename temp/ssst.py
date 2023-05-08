import copy

lit = [1, 2, 3, [4, 5, 6, [7, 8, 9]]]

cl = copy.copy(lit)

lit.append("new")
print(cl)

a = 1
while a <= 9:
    for i in range(1, a + 1):
        print(f"{a}*{i}\t", end="")
    print("")
    a += 1
