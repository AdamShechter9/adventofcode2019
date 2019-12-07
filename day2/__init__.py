from itertools import product


class Day02(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day2').split('\n')[0]
        self.data = [int(x) for x in self.raw_data.split(',')]

    def run_solution1(self):
        """
        :return:
        """
        int_code_computer = IntCode(self.data)
        exit_code_value = int_code_computer.run_program()
        return exit_code_value

    def run_solution2(self):
        """
        :return:
        """
        int_code_computer = IntCodeB(self.data, 19690720)
        exit_code_value = int_code_computer.run_program()
        return exit_code_value


class IntCode(object):
    def __init__(self, data):
        self.memory = data
        self._cursor = 0
        self._halt = False

    def run_program(self):
        self.memory_init()
        while True:
            self.opcode(self.memory[self._cursor])
            if self._halt:
                break
        return self.memory[0]

    def memory_init(self):
        self.memory[1] = 12
        self.memory[2] = 2

    def opcode(self, n):
        if n == 1:
            self.add_operation()
        elif n == 2:
            self.mult_operation()
        elif n == 99:
            self.halt()
        else:
            raise UnknownOperationException

    def add_operation(self):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        The three integers immediately after the opcode tell you these three positions -
        the first two indicate the positions from which you should read the input values,
        and the third indicates the position at which the output should be stored.
        :return:
        """
        arg1 = self.memory[self.memory[self._cursor + 1]]
        arg2 = self.memory[self.memory[self._cursor + 2]]
        arg3 = self.memory[self._cursor + 3]
        self.memory[arg3] = arg1 + arg2
        # print(f'Cursor: {self._cursor}\tAssigning position {position} with value {n1 + n2}')
        self._cursor += 4
        return

    def mult_operation(self):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
        Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
        :return:
        """
        arg1 = self.memory[self.memory[self._cursor + 1]]
        arg2 = self.memory[self.memory[self._cursor + 2]]
        arg3 = self.memory[self._cursor + 3]
        self.memory[arg3] = arg1 * arg2
        print(f'Cursor: {self._cursor}\tAssigning position {arg3} with value {arg1 * arg2}')
        self._cursor += 4
        return

    def halt(self):
        print(f'Halting on cursor in {self._cursor}')
        self._halt = True

    def __str__(self):
        output_str = ''
        for i in range(len(self.memory)):
            output_str += f'[{i}]\t{self.memory[i]}\n'
        return output_str


class IntCodeB(object):
    def __init__(self, data, target_value):
        self._init_memory = data
        self._cursor = 0
        self._halt = False
        self._stop_execution = False
        self.memory = None
        self.target_value = target_value
        self.combinations_bank = list(product(range(100), repeat=2))
        self.combinations_bank_index = 0

    def run_program(self):
        result = 0
        while result != self.target_value and not self._stop_execution:
            self.memory_init()
            print(f'noun: {self.memory[1]}    verb: {self.memory[2]}')
            for i in range(0, len(self.memory), 4):
                self._cursor = i
                self.opcode(self.memory[self._cursor])
                if self._halt:
                    break
                result = self.memory[0]
                if result == self.target_value:
                    print('#' * 50)
                    print('FOUND RESULT')
                    print(f'result: {result}\tcursor: {self._cursor}')
                    return result
            self._halt = False
            # response = input('next set')
        return result

    def memory_init(self):
        self.memory = self._init_memory.copy()
        try:
            self.memory[1] = self.combinations_bank[self.combinations_bank_index][0]
            self.memory[2] = self.combinations_bank[self.combinations_bank_index][1]
        except IndexError:
            print('Out of values to try')
            self._halt = True
            self._stop_execution = True
        self.combinations_bank_index += 1

    def opcode(self, n):
        if n == 1:
            self.add_operation()
        elif n == 2:
            self.mult_operation()
        elif n == 99:
            self.halt()
        else:
            raise UnknownOperationException

    def add_operation(self):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        The three integers immediately after the opcode tell you these three positions -
        the first two indicate the positions from which you should read the input values,
        and the third indicates the position at which the output should be stored.
        :return:
        """
        n1 = self.memory[self.memory[self._cursor + 1]]
        n2 = self.memory[self.memory[self._cursor + 2]]
        position = self.memory[self._cursor + 3]
        self.memory[position] = n1 + n2
        # print(f'Cursor: {self._cursor}\tAssigning position {position} with value {n1} + {n2} = {n1 + n2}')
        return

    def mult_operation(self):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
        Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
        :return:
        """
        n1 = self.memory[self.memory[self._cursor + 1]]
        n2 = self.memory[self.memory[self._cursor + 2]]
        position = self.memory[self._cursor + 3]
        self.memory[position] = n1 * n2
        # print(f'Cursor: {self._cursor}\tAssigning position {position} with value {n1} * {n2} = {n1 * n2}')
        return

    def halt(self):
        print(f'Halting on cursor in {self._cursor}')
        self._halt = True

    def __str__(self):
        output_str = ''
        for i in range(len(self.memory)):
            output_str += f'[{i}] {self.memory[i]}   '
        return output_str


class UnknownOperationException(BaseException):
    pass
