with open('input') as file:
    content = map(int, file.readlines())


def fuel(mass):
    return mass // 3 - 2


def recur_fuel(mass):
    f = fuel(mass)
    return f + recur_fuel(f) if f > 0 else 0


print(sum(map(fuel, content)))
print(sum(map(recur_fuel, content)))
