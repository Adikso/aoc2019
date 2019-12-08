import numpy as np

with open('input') as file:
    input_data = list(map(int, file.readline().strip()))

width = 25
height = 6

layers_count = len(input_data) / (width * height)


def part1():
    layers = np.array_split(input_data, layers_count)

    layer = min(layers, key=lambda x: (x == 0).sum())
    checksum = (layer == 1).sum() * (layer == 2).sum()
    return checksum


def part2():
    layers = np.array_split(input_data, layers_count)
    image = np.copy(layers[0])

    mask = np.zeros(width * height)
    mask[image == 2] = 1

    for layer in layers[1:]:
        image[mask == 1] = layer[mask == 1]
        mask[layer != 2] = 0

    image = image.reshape((height, width))

    return np.array2string(image, precision=0, separator=' ') \
        .replace('0', ' ').replace('1', '█') \
        .replace('[', ' ').replace(']', ' ')


print(part1())
print(part2())
