import itertools

with open('input') as file:
    input_data = list(map(int, file.readline().split(",")))


class Parameter:
    def __init__(self, memory, position, immediate):
        self.memory = memory
        self.position = position
        self.immediate = immediate

    def get(self):
        if self.immediate:
            return self.memory[self.position]
        else:
            return self.memory[self.memory[self.position]]

    def set(self, value):
        self.memory[self.memory[self.position]] = value


class Instruction:
    def __init__(self, memory, position):
        self.memory = memory
        self.position = position
        self.opcode = int(str(memory[position])[-2:])
        self.params = []

    def parse_params(self, param_count):
        raw_opcode = str(self.memory[self.position]).zfill(2 + param_count)

        for i in range(1, param_count + 1):
            self.params.append(Parameter(self.memory, self.position + i, raw_opcode[-i-2] == '1'))

        return self.params


class Interpreter:
    def __init__(self, memory, input=None):
        self.memory = memory
        self.input = input
        self.output = []
        self.ip = 0
        self.paused = False
        self.running = True

    def add(self, a, b, c):
        a = a.get()
        b = b.get()
        c.set(a + b)

    def mul(self, a, b, c):
        a = a.get()
        b = b.get()
        c.set(a * b)

    def input_value(self, c):
        if self.input:
            c.set(self.input.pop(0))
        else:
            self.paused = True

    def output_value(self, c):
        self.output.append(c.get())

    def jump_if_true(self, a, b):
        if a.get() != 0:
            self.ip = b.get()

    def jump_if_false(self, a, b):
        if a.get() == 0:
            self.ip = b.get()

    def less_than(self, a, b, c):
        c.set(int(a.get() < b.get()))

    def equals(self, a, b, c):
        c.set(int(a.get() == b.get()))

    def execute(self):
        self.paused = False

        instrs = {
            1: (3, self.add),
            2: (3, self.mul),
            3: (1, self.input_value),
            4: (1, self.output_value),
            5: (2, self.jump_if_true),
            6: (2, self.jump_if_false),
            7: (3, self.less_than),
            8: (3, self.equals),
        }

        while self.ip < len(self.memory):
            saved_ip = self.ip
            instr = Instruction(self.memory, self.ip)
            if instr.opcode == 99:
                self.running = False
                break

            param_count, func = instrs[instr.opcode]
            params = instr.parse_params(param_count)
            func(*params)

            if self.paused:
                return self.output

            if self.ip == saved_ip:
                self.ip += 1 + len(params)

        return self.output


def part1():
    combinations = itertools.permutations(range(5), 5)
    highest_signal = 0

    for combination in combinations:
        prev_output = 0
        for amplifier in combination:
            inter = Interpreter(input_data[:], [amplifier, prev_output])
            prev_output = inter.execute()[-1]
            highest_signal = max(highest_signal, prev_output)

    return highest_signal


def part2():
    combinations = itertools.permutations(range(5, 10), 5)
    highest_signal = 0

    for combination in combinations:
        prev_output = 0

        interpreters = []
        for amplifier in combination:
            inter = Interpreter(input_data[:], [amplifier, prev_output])
            interpreters.append(inter)
            prev_output = inter.execute()[-1]
            highest_signal = max(highest_signal, prev_output)

        while True:
            for interpreter in interpreters:
                if not interpreter.running:
                    break

                interpreter.input = [prev_output]
                prev_output = interpreter.execute()[-1]
                highest_signal = max(highest_signal, prev_output)
            else:
                continue
            break

    return highest_signal


if __name__ == '__main__':
    print(part1())
    print(part2())
