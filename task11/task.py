import sys
from collections import defaultdict

from task11.interpreter import Interpreter
import numpy as np

with open('input') as file:
    input_data = list(map(int, file.readline().split(",")))


def paint(area):
    robot = Interpreter(input_data)
    v_x, v_y = 0, -1
    position = 0, 0

    while robot.running:
        robot.write(area[position])
        color, dir_change = robot.read(2)
        area[position] = color

        if v_x != 0:
            v_y = -v_x if dir_change == 0 else v_x
            v_x = 0
        elif v_y != 0:
            v_x = -v_y if dir_change == 1 else v_y
            v_y = 0

        position = position[0] + v_x, position[1] + v_y


def part1():
    area = defaultdict(int)
    area[(0, 0)] = 0
    paint(area)
    return len(area.keys())


def part2():
    np.set_printoptions(threshold=sys.maxsize)

    area = defaultdict(int)
    area[(0, 0)] = 1
    paint(area)

    map = np.zeros((64, 64), dtype='int')
    for point, value in area.items():
        map[point[1], point[0]] = value

    return np.array2string(map, precision=2, separator='',)\
        .replace("[", " ").replace("]", "")\
        .replace("1", "█").replace("0", " ")


print(part1())
print(part2())
