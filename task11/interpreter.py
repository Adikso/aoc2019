class Parameter:
    def __init__(self, interpreter, position, mode):
        self.interpreter = interpreter
        self.memory = interpreter.memory
        self.position = position
        self.mode = mode

    def get(self):
        if self.mode == 1:
            return self.interpreter.get(self.position)
        elif self.mode == 2:
            return self.interpreter.get(self.memory[self.position] + self.interpreter.relative_base)
        else:
            return self.interpreter.get(self.memory[self.position])

    def set(self, value):
        if self.mode == 0:
            self.interpreter.set(self.memory[self.position], value)
        elif self.mode == 2:
            self.interpreter.set(self.memory[self.position] + self.interpreter.relative_base, value)


class Instruction:
    def __init__(self, interpreter, position):
        self.interpreter = interpreter
        self.memory = interpreter.memory
        self.position = position
        self.opcode = int(str(self.memory[position])[-2:])
        self.params = []

    def parse_params(self, param_count):
        raw_opcode = str(self.memory[self.position]).zfill(2 + param_count)

        for i in range(1, param_count + 1):
            self.params.append(Parameter(self.interpreter, self.position + i, int(raw_opcode[-i-2])))

        return self.params


class Interpreter:
    def __init__(self, memory, input=[]):
        self.memory = memory
        self.input = input
        self.output = []
        self.ip = 0
        self.relative_base = 0
        self.paused = False
        self.running = True
        self.fetch_count = None

    def get(self, position):
        if position >= len(self.memory):
            return 0
        return self.memory[position]

    def set(self, position, value):
        if position >= len(self.memory):
            self.memory.extend([0] * (position + 1 - len(self.memory)))

        self.memory[position] = value

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
        if self.fetch_count is not None:
            if self.fetch_count > 0:
                self.fetch_count -= 1
            else:
                self.paused = True
                self.fetch_count = None

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

    def change_relative(self, a):
        self.relative_base += a.get()

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
            9: (1, self.change_relative)
        }

        while self.ip < len(self.memory):
            saved_ip = self.ip
            instr = Instruction(self, self.ip)
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

    def read(self, count):
        self.fetch_count = count
        out = self.execute()[:]
        self.output.clear()
        return out

    def write(self, *data):
        self.input += data
