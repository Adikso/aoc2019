with open('input') as file:
    input_data = list(map(int, file.readline().split(",")))


def execute(memory):
    ip = 0
    while ip < len(memory):
        opcode = memory[ip]
        if opcode == 99:
            break

        a, b, target = memory[ip + 1:ip + 4]
        if opcode == 1:
            memory[target] = memory[a] + memory[b]
        elif opcode == 2:
            memory[target] = memory[a] * memory[b]

        ip += 4

    return memory


def part1():
    return execute(input_data[:])[0]


def part2():
    for noun in range(100):
        for verb in range(100):
            data = input_data[:]
            data[1], data[2] = noun, verb

            if execute(data)[0] == 19690720:
                return 100 * noun + verb


if __name__ == '__main__':
    print(part1())
    print(part2())
