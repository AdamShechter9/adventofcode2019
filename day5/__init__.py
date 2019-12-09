

class Day05(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day5').split('\n')[0]
        # self.raw_data = '3,0,4,0,99'
        # self.raw_data = '1002,4,3,4,33'
        # self.raw_data = '1101,100,-1,4,0'
        # self.raw_data = '3,9,8,9,10,9,4,9,99,-1,8'
        # self.raw_data = '3,9,7,9,10,9,4,9,99,-1,8'
        # self.raw_data = '3,3,1108,-1,8,3,4,3,99'
        # self.raw_data = '3,3,1107,-1,8,3,4,3,99'
        # self.raw_data = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'

        self.data = [int(x) for x in self.raw_data.split(',')]

    def run_solution1(self):
        """
        :return:
        """
        print('Enter 1 for input')
        intcode_comp = IntCode2(self.data)
        intcode_comp.run_program()
        return

    def run_solution2(self):
        """
        :return:
        """
        print('Enter 5 for input')
        intcode_comp = IntCode2(self.data)
        intcode_comp.run_program()
        return


class IntCode2(object):
    def __init__(self, data):
        self.memory = data
        self._cursor = 0
        self._halt = False

    def run_program(self):
        while True:
            self.opcode(self.memory[self._cursor])
            if self._halt:
                break
        return self.memory[0]

    def opcode(self, n):
        opcode_value = n % 100
        arg_mode = [n // 100 % 10, n // 1000 % 10, n // 10000 % 10]
        if opcode_value == 1:
            self.add_operation(arg_mode)
        elif opcode_value == 2:
            self.mult_operation(arg_mode)
        elif opcode_value == 3:
            self.input_operation(arg_mode)
        elif opcode_value == 4:
            self.output_operation(arg_mode)
        elif opcode_value == 5:
            self.jump_if_true(arg_mode)
        elif opcode_value == 6:
            self.jump_if_false(arg_mode)
        elif opcode_value == 7:
            self.less_than(arg_mode)
        elif opcode_value == 8:
            self.equals(arg_mode)
        elif opcode_value == 99:
            self.halt()
        else:
            raise UnknownOperationException

    def add_operation(self, arg_mode):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        The three integers immediately after the opcode tell you these three positions -
        the first two indicate the positions from which you should read the input values,
        and the third indicates the position at which the output should be stored.
        :return:
        """
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        arg3 = self.memory[self._cursor + 3]
        self.memory[arg3] = arg1 + arg2
        print(f'Cursor: {self._cursor}\tAssigning position {arg3} with value {arg1 + arg2}')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def mult_operation(self, arg_mode):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
        Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
        :return:
        """
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        arg3 = self.memory[self._cursor + 3]
        self.memory[arg3] = arg1 * arg2
        print(f'Cursor: {self._cursor}\tAssigning position {arg3} with value {arg1 * arg2}')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def input_operation(self, arg_mode):
        """
        Opcode 3 takes a single integer as input and saves it to the address given by its only parameter.
        For example, the instruction 3,50 would take an input value and store it at address 50.
        :return:
        """
        number_input = input('Please enter integer input: ')
        int_input = int(number_input)
        arg1 = self.memory[self._cursor + 1]
        self.memory[arg1] = int_input
        if arg1 != self._cursor:
            self._cursor += 2
        return

    def output_operation(self, arg_mode):
        """
        Opcode 4 outputs the value of its only parameter.
        For example, the instruction 4,50 would output the value at address 50.
        :return:
        """
        if arg_mode[0] == 0:
            output_number = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
            output_number = arg1
        print('*'*50)
        print(f'REQUESTED: OUTPUT {output_number}')
        print('*'*50)
        self._cursor += 2
        return

    def jump_if_true(self, arg_mode):
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero,
        it sets the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing.
        :return:
        """
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        if arg1 != 0:
            print(f'Cursor: {self._cursor}\tJumping to position {arg2}')
            self._cursor = arg2
        else:
            print(f'Cursor: {self._cursor}\tNot Jumping')
            self._cursor += 3
        return

    def jump_if_false(self, arg_mode):
        """
        Opcode 6 is jump-if-false: if the first parameter is zero,
        it sets the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing.
        :return:
        """
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        if arg1 == 0:
            print(f'Cursor: {self._cursor}\tJumping to position {arg2}')
            self._cursor = arg2
        else:
            print(f'Cursor: {self._cursor}\tNot Jumping')
            self._cursor += 3
        return

    def less_than(self, arg_mode):
        """
        Opcode 7 is less than: if the first parameter is less than the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        :return:
        """
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        arg3 = self.memory[self._cursor + 3]
        if arg1 < arg2:
            self.memory[arg3] = 1
            print(f'Cursor: {self._cursor}\tAssigning position {arg3} with 1')
        else:
            self.memory[arg3] = 0
            print(f'Cursor: {self._cursor}\tAssigning position {arg3} with 0')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def equals(self, arg_mode):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        :return:
        """
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        arg3 = self.memory[self._cursor + 3]
        if arg1 == arg2:
            self.memory[arg3] = 1
            print(f'Cursor: {self._cursor}\tAssigning position {arg3} with 1')
        else:
            self.memory[arg3] = 0
            print(f'Cursor: {self._cursor}\tAssigning position {arg3} with 0')
        if arg3 != self._cursor:
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


class UnknownOperationException(BaseException):
    pass
