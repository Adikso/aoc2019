from collections import defaultdict
from scipy.spatial import distance

with open('input') as file:
    data = [[(x[0], int(x[1:])) for x in line.split(",")] for line in file.readlines()]


def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def task1():
    points = defaultdict(int)

    for path in data:
        x, y = 0, 0
        local_points = []
        for instr, value in path:
            if instr == 'U':
                local_points += [(x, c) for c in range(y - 1, y - value - 1, -1)]
                y -= value
            elif instr == 'D':
                local_points += [(x, c) for c in range(y + 1, y + value + 1, 1)]
                y += value
            elif instr == 'L':
                local_points += [(c, y) for c in range(x - 1, x - value - 1, -1)]
                x -= value
            elif instr == 'R':
                local_points += [(c, y) for c in range(x + 1, x + value + 1, 1)]
                x += value

        for point in set(local_points):
            points[point] += 1

    cross = filter(lambda x: x[1] >= 2, points.items())
    closest = min(cross, key=lambda x: distance.cityblock((0, 0), x[0]))[0]

    return distance.cityblock((0, 0), closest)


print(task1())
