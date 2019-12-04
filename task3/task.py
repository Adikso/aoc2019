from collections import defaultdict

with open('input') as file:
    data = [[(x[0], int(x[1:])) for x in line.split(",")] for line in file.readlines()]


def manhattan_distance(x, y):
    return sum(abs(a - b) for a, b in zip(x, y))


def task1():
    points = defaultdict(int)
    distances = [{}, {}]

    for num, path in enumerate(data):
        x, y = 0, 0
        path_points = []
        distance = 0
        for instr, value in path:
            instr_points = []
            if instr == 'U':
                instr_points = [(x, c) for c in range(y - 1, y - value - 1, -1)]
                y -= value
            elif instr == 'D':
                instr_points = [(x, c) for c in range(y + 1, y + value + 1, 1)]
                y += value
            elif instr == 'L':
                instr_points = [(c, y) for c in range(x - 1, x - value - 1, -1)]
                x -= value
            elif instr == 'R':
                instr_points = [(c, y) for c in range(x + 1, x + value + 1, 1)]
                x += value

            for i, point in enumerate(instr_points):
                if point in distances[num]:
                    continue
                distances[num][point] = distance + i + 1

            path_points += instr_points
            distance += value

        for point in set(path_points):
            points[point] += 1

    cross = filter(lambda x: x[1] >= 2, points.items())
    closest = min(cross, key=lambda x: manhattan_distance((0, 0), x[0]))[0]

    cross = filter(lambda x: x[1] >= 2, points.items())
    less_steps = min(cross, key=lambda x: distances[0][x[0]] + distances[1][x[0]])[0]
    min_steps = distances[0][less_steps] + distances[1][less_steps]

    return manhattan_distance((0, 0), closest), min_steps


print(task1())
