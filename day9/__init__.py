

class Day09(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day9').split('\n')[0]
        # self.raw_data = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
        # self.raw_data = '1102,34915192,34915192,7,4,7,99,0'
        # self.raw_data = '104,1125899906842624,99'
        self.data = [int(x) for x in self.raw_data.split(',')]

    def run_solution1(self):
        """
        :return:
        """
        int_code = IntCode9(self.data)
        int_code.run_program()
        return

    def run_solution2(self):
        """
        :return:
        """
        return


class IntCode9(object):
    def __init__(self, data):
        self.memory = data.copy()
        self.memory.extend([0 for _ in range(100000)])
        self._cursor = 0
        self._relative_position = 0
        self._halt = False

    def run_program(self):
        while True:
            self.opcode(self.memory[self._cursor])
            if self._halt:
                break
        return

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
        elif opcode_value == 9:
            self.relative_pos_offset(arg_mode)
        elif opcode_value == 99:
            self.halt()
        else:
            raise UnknownOperationException

    def arg_value_calc(self, arg_mode, arg_count=3):
        """
        Determines values of arguments based on argument mode values.
        Making two assumptions:
        1.  Arg1 and Arg2 will return the VALUE whether absolute / relative position or direct value
        2.  Arg3 will always return the POSITION value whether absolute or relative position
        """
        arg1, arg2, arg3 = None, None, None
        if arg_mode[0] == 0:
            arg1 = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
        elif arg_mode[0] == 2:
            arg1 = self.memory[self._relative_position + self.memory[self._cursor + 1]]
        # Exit point for 1 argument.  might be more elegant way to do this
        if arg_count == 1:
            return arg1
        if arg_mode[1] == 0:
            arg2 = self.memory[self.memory[self._cursor + 2]]
        elif arg_mode[1] == 1:
            arg2 = self.memory[self._cursor + 2]
        elif arg_mode[1] == 2:
            arg2 = self.memory[self._relative_position + self.memory[self._cursor + 2]]
        # Exit point for 2 arguments.  might be more elegant way to do this
        if arg_count == 2:
            return arg1, arg2
        if arg_mode[2] == 0:
            arg3 = self.memory[self._cursor + 3]
        elif arg_mode[2] == 2:
            arg3 = self._relative_position + self.memory[self._cursor + 3]
        return arg1, arg2, arg3

    def add_operation(self, arg_mode):
        """
        Opcode 1 adds together numbers read from two positions and stores the result in a third position.
        The three integers immediately after the opcode tell you these three positions -
        the first two indicate the positions from which you should read the input values,
        and the third indicates the position at which the output should be stored.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}\targ2: {self.memory[self._cursor+2]}\targ3: {self.memory[self._cursor+3]}')
        arg1, arg2, arg3 = self.arg_value_calc(arg_mode)
        self.memory[arg3] = arg1 + arg2
        print(f'Assigning position {arg3} with value {arg1} + {arg2} = {arg1 + arg2}')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def mult_operation(self, arg_mode):
        """
        Opcode 2 works exactly like opcode 1, except it multiplies the two inputs instead of adding them.
        Again, the three integers after the opcode indicate where the inputs and outputs are, not their values.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}\targ2: {self.memory[self._cursor+2]}\targ3: {self.memory[self._cursor+3]}')
        arg1, arg2, arg3 = self.arg_value_calc(arg_mode)
        self.memory[arg3] = arg1 * arg2
        print(f'Assigning position {arg3} with value {arg1} * {arg2} = {arg1 * arg2}')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def input_operation(self, arg_mode, input_value=None):
        """
        Opcode 3 takes a single integer as input and saves it to the address given by its only parameter.
        For example, the instruction 3,50 would take an input value and store it at address 50.
        instruction 203, 0
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}')
        if input_value is None:
            number_input = input('Please enter integer input: ')
        else:
            number_input = input_value
        int_input = int(number_input)
        if arg_mode[0] == 0:
            position = self.memory[self._cursor+1]
        elif arg_mode[0] == 2:
            position = self._relative_position + self.memory[self._cursor + 1]
        self.memory[position] = int_input
        print(f'Assigning position {position} with value {int_input}')
        if position != self._cursor:
            self._cursor += 2
        return

    def output_operation(self, arg_mode):
        """
        Opcode 4 outputs the value of its only parameter.
        For example, the instruction 4,50 would output the value at address 50.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}')
        arg1 = self.arg_value_calc(arg_mode, 1)
        output_number = arg1
        print('*'*50)
        print(f'OUTPUT {output_number}')
        print('*'*50)
        self._cursor += 2
        return output_number

    def jump_if_true(self, arg_mode):
        """
        Opcode 5 is jump-if-true: if the first parameter is non-zero,
        it sets the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}\targ2: {self.memory[self._cursor+2]}')
        arg1, arg2 = self.arg_value_calc(arg_mode, 2)
        if arg1 != 0:
            print(f'{arg1} != 0\tJumping to position {arg2}')
            self._cursor = arg2
        else:
            print(f'{arg1} == 0\tDoing nothing')
            self._cursor += 3
        return

    def jump_if_false(self, arg_mode):
        """
        Opcode 6 is jump-if-false: if the first parameter is zero,
        it sets the instruction pointer to the value from the second parameter.
        Otherwise, it does nothing.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}\targ2: {self.memory[self._cursor+2]}')
        arg1, arg2 = self.arg_value_calc(arg_mode, 2)
        if arg1 == 0:
            print(f'{arg1} == 0\tJumping to position {arg2}')
            self._cursor = arg2
        else:
            print(f'{arg1} != 0\tDoing nothing')
            self._cursor += 3
        return

    def less_than(self, arg_mode):
        """
        Opcode 7 is less than: if the first parameter is less than the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}\targ2: {self.memory[self._cursor+2]}\targ3: {self.memory[self._cursor+3]}')
        arg1, arg2, arg3 = self.arg_value_calc(arg_mode)
        if arg1 < arg2:
            self.memory[arg3] = 1
            print(f'{arg1} < {arg2}\tAssigning position {arg3} with 1')
        else:
            self.memory[arg3] = 0
            print(f'{arg1} > {arg2}\tAssigning position {arg3} with 0')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def equals(self, arg_mode):
        """
        Opcode 8 is equals: if the first parameter is equal to the second parameter,
        it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        :return:
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}\targ2: {self.memory[self._cursor+2]}\targ3: {self.memory[self._cursor+3]}')
        arg1, arg2, arg3 = self.arg_value_calc(arg_mode)
        if arg1 == arg2:
            self.memory[arg3] = 1
            print(f'{arg1} == {arg2}\tAssigning position {arg3} with 1')
        else:
            self.memory[arg3] = 0
            print(f'{arg1} != {arg2}\tAssigning position {arg3} with 0')
        if arg3 != self._cursor:
            self._cursor += 4
        return

    def relative_pos_offset(self, arg_mode):
        """
        Opcode 9 adjusts the relative base by the value of its only parameter.
        The relative base increases (or decreases, if the value is negative) by the value of the parameter.
        """
        print(f'Cursor: {self._cursor}\tOpcode: {self.memory[self._cursor]}\targ1: {self.memory[self._cursor+1]}')
        arg1 = self.arg_value_calc(arg_mode, 1)
        print(f'Changing relative position {self._relative_position} by {arg1}')
        self._relative_position += arg1
        print(f'New relative position {self._relative_position}')
        if self._relative_position < 0:
            raise NegativeMemoryAddressException
        self._cursor += 2
        return

    def halt(self):
        print(f'Halting on cursor in {self._cursor}')
        self._halt = True

    def __str__(self):
        output_str = ''
        for i in range(len(self.memory)):
            output_str += f'[{i}]\t{self.memory[i]}\n'
        return output_str


class UnknownOperationException(Exception):
    pass


class NegativeMemoryAddressException(Exception):
    pass
