import math
from collections import defaultdict, OrderedDict

import numpy as np
with open('input', 'r') as file:
    arr = np.array([list(x.strip()) for x in file.readlines()], dtype='str')
    arr[arr == '.'] = 0
    arr[arr == '#'] = 1
    arr = np.array(arr, dtype='int')


def get_angles():
    results = []
    for x1, y1 in np.ndindex(arr.shape):
        if arr[y1, x1] == 0:
            continue

        visibility = defaultdict(list)
        for x2, y2 in np.ndindex(arr.shape):
            if (x1, y1) == (x2, y2) or arr[y2, x2] == 0:
                continue

            angle = (math.atan2(y2 - y1, x2 - x1) * 180 / math.pi + 360 + 90) % 360
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            visibility[angle].append(((x2, y2), distance))

        results.append(((x1, y1), len(visibility.keys()), visibility))
    return results


def part1():
    results = get_angles()
    return max(results, key=lambda x: x[1])[0]


def part2():
    results = get_angles()
    station = max(results, key=lambda x: x[1])
    angles = OrderedDict(sorted(station[2].items()))
    count = 0

    while True:
        for angle, asteroids in angles.items():
            if not asteroids:
                continue

            asteroids.sort(key=lambda x: x[1])
            point, distance = asteroids.pop(0)
            count += 1

            if count == 200:
                return point[0] * 100 + point[1]


print(part1())
print(part2())
