from day5 import IntCode2
from itertools import permutations


class Day07(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day7').split('\n')[0]
        # self.raw_data = '3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0'
        # self.raw_data = '3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0'
        # self.raw_data = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
        # self.raw_data = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
        # self.raw_data = '3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10'
        self.data = [int(x) for x in self.raw_data.split(',')]

    def run_solution1(self):
        """
        :return:
        """
        amplifier_controller = AmplifierController(self.data)
        return amplifier_controller.run_program()

    def run_solution2(self):
        """
        :return:
        """
        amplifier_controller2 = AmplifierControllerFeedback(self.data)
        return amplifier_controller2.run_program()


class IntCode3(IntCode2):
    def __init__(self, data):
        super(IntCode3, self).__init__(data)
        self.output_value = 0
        self.num_gen = None
        self._pause = False

    @staticmethod
    def value_generator(vals):
        """Simple generator to yield values for input"""
        while True:
            for n in vals:
                yield n

    def run_program(self, *vals):
        self.num_gen = self.value_generator(vals)
        self._halt = False
        self._pause = False
        while True:
            self.opcode(self.memory[self._cursor])
            if self._pause:
                break
            if self._halt:
                break
        return self.output_value, self._halt

    def input_operation(self, arg_mode, input_value=None):
        """Overriding IntCode2 input operation"""
        number_input = next(self.num_gen)
        print(f'INPUT {number_input}')
        int_input = int(number_input)
        arg1 = self.memory[self._cursor + 1]
        self.memory[arg1] = int_input
        if arg1 != self._cursor:
            self._cursor += 2

    def output_operation(self, arg_mode):
        """Overriding IntCode2 output function"""
        if arg_mode[0] == 0:
            output_number = self.memory[self.memory[self._cursor + 1]]
        elif arg_mode[0] == 1:
            arg1 = self.memory[self._cursor + 1]
            output_number = arg1
        print(f'REQUESTED: OUTPUT {output_number}')
        self._cursor += 2
        self.output_value = output_number
        self._pause = True


class AmplifierController(object):
    def __init__(self, data):
        self.instructions = data
        self.input_combinations = list(permutations(range(5)))
        self.solution_map = {}

    @classmethod
    def computer_factory(cls, instructions):
        return IntCode3(instructions.copy())

    def run_program(self):
        max_answer = -1
        answer_index = -1
        for i, input_comb in enumerate(self.input_combinations):
            self.solution_map[i] = 0
            serial_value = 0
            for comb_n in input_comb:
                intcode_computer = self.computer_factory(self.instructions)
                serial_value = intcode_computer.run_program(comb_n, serial_value)
            self.solution_map[i] = serial_value
            if serial_value > max_answer:
                max_answer = serial_value
                answer_index = i
        print(f'highest signal: {max_answer} achieved with combination: {self.input_combinations[answer_index]}')
        return max_answer


class AmplifierControllerFeedback(object):
    def __init__(self, data):
        self.instructions = data
        self.input_combinations = list(permutations(range(5, 10)))
        self.solution_map = {}

    @classmethod
    def computer_factory(cls, instructions):
        return IntCode3(instructions.copy())

    def run_program(self):
        max_answer = -1
        answer_index = -1
        for i, input_comb in enumerate(self.input_combinations):
            self.solution_map[i] = 0
            serial_value = 0
            amplifier_computers = [self.computer_factory(self.instructions) for x in range(5)]
            amplifier_state = [False for x in range(5)]
            # Run through all amplifiers for the first time, inputting phase
            for j, comb_n in enumerate(input_comb):
                serial_value, amplifier_state[j] = amplifier_computers[j].run_program(comb_n, serial_value)
            # Loop through all amplifiers until all reach a 'halted' state
            j = 0
            while not all(amplifier_state):
                serial_value, amplifier_state[j] = amplifier_computers[j].run_program(serial_value)
                if j < 4:
                    j += 1
                else:
                    j = 0
            self.solution_map[i] = serial_value
            if serial_value > max_answer:
                max_answer = serial_value
                answer_index = i
        print(f'highest signal: {max_answer} achieved with combination: {self.input_combinations[answer_index]}')
        return max_answer
