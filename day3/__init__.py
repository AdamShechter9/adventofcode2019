

class Day03(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day3').split('\n')
        # self.raw_data = ['R8,U5,L5,D3', 'U7,R6,D4,L4']
        # self.raw_data = ['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']
        # self.raw_data = ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']
        self.data = [x for x in self.raw_data if len(x) > 0]
        for i in range(len(self.data)):
            self.data[i] = self.data[i].split(',')

    def run_solution1(self):
        """
        :return:
        """
        wireboard = WireBoardA(self.data)
        return wireboard.run_wires()

    def run_solution2(self):
        """
        :return:
        """
        wireboard = WireBoardB(self.data)
        return wireboard.run_wires()


class WireBoardA(object):
    def __init__(self, instructions):
        self._path_instructions = instructions
        self._size_x = self.calculate_max_left_right(self._path_instructions)
        self._size_y = self.calculate_max_up_down(self._path_instructions)
        print(self._size_x)
        print(self._size_y)
        self.grid = [{'x': 0, 'y': 0}]
        self.grid_wire_ref = [[0, 1]]
        self.cursor = {'x': 0, 'y': 0}

    @staticmethod
    def calculate_max_left_right(instructions):
        max_right = 0
        max_left = 0
        for wire_instr in instructions:
            cursor = 0
            for instr in wire_instr:
                direction = instr[:1]
                distance = int(instr[1:])
                if direction in ('R', 'L'):
                    if direction == 'R':
                        cursor += distance
                    elif direction == 'L':
                        cursor -= distance
                    if cursor > max_right:
                        max_right = cursor
                    elif cursor < max_left:
                        max_left = cursor
        return {'max_left': max_left, 'max_right': max_right}

    @staticmethod
    def calculate_max_up_down(instructions):
        max_up = 0
        max_down = 0
        for wire_instr in instructions:
            cursor = 0
            for instr in wire_instr:
                direction = instr[:1]
                distance = int(instr[1:])
                if direction in ('U', 'D'):
                    if direction == 'U':
                        cursor += distance
                    elif direction == 'D':
                        cursor -= distance
                    if cursor > max_up:
                        max_up = cursor
                    elif cursor < max_down:
                        max_down = cursor
        return {'max_up': max_up, 'max_down': max_down}

    def run_wires(self):
        wire_num = -1
        for wire_inst in self._path_instructions:
            wire_num += 1
            print(f'Processing Wire {wire_num}')
            self.cursor = {'x': 0, 'y': 0}
            number_of_instructions = len(wire_inst)
            for i, instr in enumerate(wire_inst, 0):
                print(f'{i}/{number_of_instructions} {instr}')
                direction = instr[:1]
                distance = int(instr[1:])
                self._create_wire(direction, distance, wire_num)
        # print(self.grid)
        # print(self.grid_wire_ref)
        answer_index, distance = self._find_nearest_intersections()
        print(f'answer: {self.grid[answer_index]}\t{distance}')
        return distance

    def _create_wire(self, direction, distance, wire_num):
        # UP
        if direction == 'U':
            for i in range(self.cursor['y'] + 1, self.cursor['y'] + distance + 1):
                try:
                    index = self.grid.index({'x': self.cursor['x'], 'y': i})
                    if wire_num not in self.grid_wire_ref[index]:
                        self.grid_wire_ref[index].append(wire_num)
                except ValueError:
                    self.grid.append({'x': self.cursor['x'], 'y': i})
                    self.grid_wire_ref.append([wire_num])
            self.cursor['y'] += distance
        # DOWN
        elif direction == 'D':
            for i in range(self.cursor['y'] - 1, self.cursor['y'] - distance - 1, -1):
                try:
                    index = self.grid.index({'x': self.cursor['x'], 'y': i})
                    if wire_num not in self.grid_wire_ref[index]:
                        self.grid_wire_ref[index].append(wire_num)
                except ValueError:
                    self.grid.append({'x': self.cursor['x'], 'y': i})
                    self.grid_wire_ref.append([wire_num])
            self.cursor['y'] -= distance
        # RIGHT
        elif direction == 'R':
            for i in range(self.cursor['x'] + 1, self.cursor['x'] + distance + 1):
                try:
                    index = self.grid.index({'x': i, 'y': self.cursor['y']})
                    if wire_num not in self.grid_wire_ref[index]:
                        self.grid_wire_ref[index].append(wire_num)
                except ValueError:
                    self.grid.append({'x': i, 'y': self.cursor['y']})
                    self.grid_wire_ref.append([wire_num])
            self.cursor['x'] += distance
        # LEFT
        elif direction == 'L':
            for i in range(self.cursor['x'] - 1, self.cursor['x'] - distance - 1, -1):
                try:
                    index = self.grid.index({'x': i, 'y': self.cursor['y']})
                    if wire_num not in self.grid_wire_ref[index]:
                        self.grid_wire_ref[index].append(wire_num)
                except ValueError:
                    self.grid.append({'x': i, 'y': self.cursor['y']})
                    self.grid_wire_ref.append([wire_num])
            self.cursor['x'] -= distance

    def _find_nearest_intersections(self):
        print(f'intersection coordinates')
        shortest_distance = -1
        shortest_index = -1
        for i in range(1, len(self.grid_wire_ref)):
            if len(self.grid_wire_ref[i]) > 1:
                print(self.grid[i])
                distance = abs(self.grid[i]['x']) + abs(self.grid[i]['y'])
                if shortest_distance == -1:
                    shortest_index = i
                    shortest_distance = distance
                elif distance < shortest_distance:
                    shortest_index = i
                    shortest_distance = distance
        return shortest_index, shortest_distance


class WireBoardB(object):
    def __init__(self, instructions):
        self._path_instructions = instructions
        self._size_x = self.calculate_max_left_right(self._path_instructions)
        self._size_y = self.calculate_max_up_down(self._path_instructions)
        print(self._size_x)
        print(self._size_y)
        # a coordinate list for the wires
        self.grid = [{'x': 0, 'y': 0}]
        # A list mirroring the coordinate list.
        # It stores a tuple [(wire number, steps to get there)]
        self.grid_wire_ref = [[(0, 0), (1, 0)]]
        self.cursor = {'x': 0, 'y': 0}

    @staticmethod
    def calculate_max_left_right(instructions):
        max_right = 0
        max_left = 0
        for wire_instr in instructions:
            cursor = 0
            for instr in wire_instr:
                direction = instr[:1]
                distance = int(instr[1:])
                if direction in ('R', 'L'):
                    if direction == 'R':
                        cursor += distance
                    elif direction == 'L':
                        cursor -= distance
                    if cursor > max_right:
                        max_right = cursor
                    elif cursor < max_left:
                        max_left = cursor
        return {'max_left': max_left, 'max_right': max_right}

    @staticmethod
    def calculate_max_up_down(instructions):
        max_up = 0
        max_down = 0
        for wire_instr in instructions:
            cursor = 0
            for instr in wire_instr:
                direction = instr[:1]
                distance = int(instr[1:])
                if direction in ('U', 'D'):
                    if direction == 'U':
                        cursor += distance
                    elif direction == 'D':
                        cursor -= distance
                    if cursor > max_up:
                        max_up = cursor
                    elif cursor < max_down:
                        max_down = cursor
        return {'max_up': max_up, 'max_down': max_down}

    def run_wires(self):
        wire_num = -1
        for wire_inst in self._path_instructions:
            wire_num += 1
            steps = 0
            print(f'Processing Wire {wire_num}')
            self.cursor = {'x': 0, 'y': 0}
            number_of_instructions = len(wire_inst)
            for i, instr in enumerate(wire_inst, 0):
                print(f'{i + 1}/{number_of_instructions} {instr}')
                direction = instr[:1]
                distance = int(instr[1:])
                self._create_wire(direction, distance, wire_num, steps)
                steps += distance
        # print(self.grid)
        # print(self.grid_wire_ref)
        answer_index, shortest_steps = self._find_nearest_shortest_path_intersections()
        print(f'answer: {self.grid[answer_index]}\t{shortest_steps}')
        return shortest_steps

    def _create_wire(self, direction, distance, wire_num, steps):
        # UP
        if direction == 'U':
            for i in range(self.cursor['y'] + 1, self.cursor['y'] + distance + 1):
                steps += 1
                try:
                    index = self.grid.index({'x': self.cursor['x'], 'y': i})
                    if self.grid_wire_ref[index][0][0] != wire_num and len(self.grid_wire_ref[index]) < 2:
                        self.grid_wire_ref[index].append((wire_num, steps))
                except ValueError:
                    self.grid.append({'x': self.cursor['x'], 'y': i})
                    self.grid_wire_ref.append([(wire_num, steps)])
            self.cursor['y'] += distance
        # DOWN
        elif direction == 'D':
            for i in range(self.cursor['y'] - 1, self.cursor['y'] - distance - 1, -1):
                steps += 1
                try:
                    index = self.grid.index({'x': self.cursor['x'], 'y': i})
                    if self.grid_wire_ref[index][0][0] != wire_num and len(self.grid_wire_ref[index]) < 2:
                        self.grid_wire_ref[index].append((wire_num, steps))
                except ValueError:
                    self.grid.append({'x': self.cursor['x'], 'y': i})
                    self.grid_wire_ref.append([(wire_num, steps)])

            self.cursor['y'] -= distance
        # RIGHT
        elif direction == 'R':
            for i in range(self.cursor['x'] + 1, self.cursor['x'] + distance + 1):
                steps += 1
                try:
                    index = self.grid.index({'x': i, 'y': self.cursor['y']})
                    if self.grid_wire_ref[index][0][0] != wire_num and len(self.grid_wire_ref[index]) < 2:
                        self.grid_wire_ref[index].append((wire_num, steps))
                except ValueError:
                    self.grid.append({'x': i, 'y': self.cursor['y']})
                    self.grid_wire_ref.append([(wire_num, steps)])
            self.cursor['x'] += distance
        # LEFT
        elif direction == 'L':
            for i in range(self.cursor['x'] - 1, self.cursor['x'] - distance - 1, -1):
                steps += 1
                try:
                    index = self.grid.index({'x': i, 'y': self.cursor['y']})
                    if self.grid_wire_ref[index][0][0] != wire_num and len(self.grid_wire_ref[index]) < 2:
                        self.grid_wire_ref[index].append((wire_num, steps))
                except ValueError:
                    self.grid.append({'x': i, 'y': self.cursor['y']})
                    self.grid_wire_ref.append([(wire_num, steps)])
            self.cursor['x'] -= distance

    def _find_nearest_shortest_path_intersections(self):
        print(f'intersection coordinates')
        shortest_steps = -1
        shortest_index = -1
        for i in range(1, len(self.grid_wire_ref)):
            if len(self.grid_wire_ref[i]) > 1:
                print(self.grid[i])
                combined_steps = self.grid_wire_ref[i][0][1] + self.grid_wire_ref[i][1][1]
                if shortest_steps == -1:
                    shortest_index = i
                    shortest_steps = combined_steps
                elif combined_steps < shortest_steps:
                    shortest_index = i
                    shortest_steps = combined_steps
        return shortest_index, shortest_steps
