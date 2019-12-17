import fractions
import math
from operator import itemgetter


class Day10(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day10').split('\n')
        # 3,4 = 8
        # Pass
        # self.raw_data = ['.#..#', '.....', '#####', '....#', '...##']
        # 5,8 = 33
        # PASS
        # self.raw_data = [
        #     '......#.#.',
        #     '#..#.#....',
        #     '..#######.',
        #     '.#.#.###..',
        #     '.#..#.....',
        #     '..#....#.#',
        #     '#..#....#.',
        #     '.##.#..###',
        #     '##...#..#.',
        #     '.#....####'
        # ]
        # 1,2 = 35
        # PASS
        # self.raw_data = [
        #     '#.#...#.#.',
        #     '.###....#.',
        #     '.#....#...',
        #     '##.#.#.#.#',
        #     '....#.#.#.',
        #     '.##..###.#',
        #     '..#...##..',
        #     '..##....##',
        #     '......#...',
        #     '.####.###.'
        # ]
        # 6,3 = 41
        # Pass
        # self.raw_data = [
        #     '.#..#..###',
        #     '####.###.#',
        #     '....###.#.',
        #     '..###.##.#',
        #     '##.##.#.#.',
        #     '....###..#',
        #     '..#.#..#.#',
        #     '#..#.#.###',
        #     '.##...##.#',
        #     '.....#.#..'
        # ]
        # 11, 13 = 210
        # PASS
        # self.raw_data = [
        #     '.#..##.###...#######',
        #     '##.############..##.',
        #     '.#.######.########.#',
        #     '.###.#######.####.#.',
        #     '#####.##.#.##.###.##',
        #     '..#####..#.#########',
        #     '####################',
        #     '#.####....###.#.#.##',
        #     '##.#################',
        #     '#####.##.###..####..',
        #     '..######..##.#######',
        #     '####.##.####...##..#',
        #     '.#####..#.######.###',
        #     '##...#.##########...',
        #     '#.##########.#######',
        #     '.####.#.###.###.#.##',
        #     '....##.##.###..#####',
        #     '.#.#.###########.###',
        #     '#.#.#.#####.####.###',
        #     '###.##.####.##.#..##'
        # ]
        # part 2
        # self.raw_data = [
        #     '.#....#####...#..',
        #     '##...##.#####..##',
        #     '##...#...#.#####.',
        #     '..#.....#...###..',
        #     '..#.#.....#....##'
        # ]
        self.data = []
        for line in self.raw_data:
            self.data.append([_ for _ in line])

    def run_solution1(self):
        """
        :return:
        """
        asteroid_monitoring_station = AsteroidMonitoringStation(self.data)
        answer_coord, answer_max = asteroid_monitoring_station.calculate_asteroid_line_of_sight()
        print(f'answer: {answer_coord}\tvisible asteroids: {answer_max}')
        return answer_coord, answer_max

    def run_solution2(self):
        """
        :return:
        """
        asteroid_monitoring_station = AsteroidMonitoringStation(self.data)
        answer_coord, answer_max = asteroid_monitoring_station.calculate_asteroid_line_of_sight()
        print('*' * 50)
        print(f'answer: {answer_coord}\tvisible asteroids: {answer_max}')
        print('*' * 50)
        return asteroid_monitoring_station.calculate_vaporization_order(answer_coord)


class AsteroidMonitoringStation(object):
    PRIMES = (1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29)

    def __init__(self, data):
        self.asteroid_map = data
        self.asteroid_answer = {}
        for y, row in enumerate(self.asteroid_map):
            for x, col in enumerate(row):
                if self.asteroid_map[y][x] == '#':
                    self.asteroid_answer[(x, y)] = 0

    def calculate_asteroid_line_of_sight(self):
        greedy_index = -1
        greedy_max = -1
        for current_asteroid in self.asteroid_answer:
            asteroids_coords_bank = list(self.asteroid_answer.keys())
            # Remove current asteroid from bank
            asteroids_coords_bank.remove(current_asteroid)
            print(f'Evaluating {current_asteroid}')
            for asteroids_coord in self.asteroid_answer:
                if asteroids_coord == current_asteroid:
                    continue
                print(f'{asteroids_coord}')
                x = asteroids_coord[0]
                y = asteroids_coord[1]
                is_blocked_flag = False
                # Checking for parallel lines
                # on x plane
                if x < current_asteroid[0] and y == current_asteroid[1]:
                    for i in range(x + 1, current_asteroid[0]):
                        if (i, y) in asteroids_coords_bank:
                            print(f'Blocked by {i}, {y}')
                            is_blocked_flag = True
                elif x > current_asteroid[0] and y == current_asteroid[1]:
                    for i in range(x - 1, current_asteroid[0], -1):
                        if (i, y) in asteroids_coords_bank:
                            print(f'Blocked by {i}, {y}')
                            is_blocked_flag = True
                # on y plane
                if y < current_asteroid[1] and x == current_asteroid[0]:
                    for i in range(y + 1, current_asteroid[1]):
                        if (x, i) in asteroids_coords_bank:
                            print(f'Blocked by {x}, {i}')
                            is_blocked_flag = True
                elif y > current_asteroid[1] and x == current_asteroid[0]:
                    for i in range(y - 1, current_asteroid[1], -1):
                        if (x, i) in asteroids_coords_bank:
                            print(f'Blocked by {x}, {i}')
                            is_blocked_flag = True
                # Checking for diagonals
                # We perform tests in reverse.  Going from test coordinate backwards to origin (current_asteroid)
                # Down-Right Diagonal    x+n y+n
                if not is_blocked_flag and x != current_asteroid[0] and y != current_asteroid[1]:
                    if x > current_asteroid[0] and y > current_asteroid[1] and x - current_asteroid[0] == y - current_asteroid[1]:
                        for i in range(1, x - current_asteroid[0]):
                            if (x - i, y - i) in asteroids_coords_bank:
                                print(f'Blocked by {x - i}, {y - i}')
                                is_blocked_flag = True
                    # Up-Right Diagonal      x+n y-n
                    if x > current_asteroid[0] and y < current_asteroid[1] and x - current_asteroid[0] == current_asteroid[1] - y:
                        for i in range(1, x - current_asteroid[0]):
                            if (x - i, y + i) in asteroids_coords_bank:
                                print(f'Blocked by {x - i}, {y + i}')
                                is_blocked_flag = True
                    # Down-Left Diagonal    x-n y+n
                    if x < current_asteroid[0] and y > current_asteroid[1] and current_asteroid[0] - x == y - current_asteroid[1]:
                        for i in range(1, current_asteroid[0] - x):
                            if (x + i, y - i) in asteroids_coords_bank:
                                print(f'Blocked by {x + i}, {y - i}')
                                is_blocked_flag = True
                    # Up-Left Diagonal    x-n y-n
                    if x < current_asteroid[0] and y < current_asteroid[1] and current_asteroid[0] - x == current_asteroid[1] - y:
                        for i in range(1, current_asteroid[0] - x):
                            if (x + i, y + i) in asteroids_coords_bank:
                                print(f'Blocked by {x + i}, {y + i}')
                                is_blocked_flag = True
                # Checking Angles through steps
                if not is_blocked_flag and x != current_asteroid[0] and y != current_asteroid[1] and abs(current_asteroid[0] - x) != abs(current_asteroid[1] - y):
                    total_x = x - current_asteroid[0]
                    total_y = y - current_asteroid[1]
                    fraction1 = fractions.Fraction(abs(total_x), abs(total_y))
                    step_x = fraction1.numerator
                    step_y = fraction1.denominator
                    if total_x < 0 and step_x > 0:
                        step_x *= -1
                    if total_y < 0 and step_y > 0:
                        step_y *= -1
                    print(f'Calculating angles\tstep x: {step_x}\t step y: {step_y}')
                    steps_needed = abs(total_x // step_x)

                    for i in range(1, steps_needed):
                        curr_x = i * step_x
                        curr_y = i * step_y
                        if (x - curr_x, y - curr_y) in asteroids_coords_bank:
                            print(f'Blocked by {x - curr_x}, {y - curr_y}')
                            is_blocked_flag = True
                            break
                if is_blocked_flag:
                    asteroids_coords_bank.remove(asteroids_coord)
                else:
                    print('Pass')
            self.asteroid_answer[current_asteroid] = len(asteroids_coords_bank)
            print('*'*25)
            print(f'{current_asteroid}\tVisible Asteroids: {len(asteroids_coords_bank)}')
            # print(f'{asteroids_coords_bank}')
            print('*'*25)
            if greedy_max < self.asteroid_answer[current_asteroid]:
                greedy_max = self.asteroid_answer[current_asteroid]
                greedy_index = current_asteroid
        print(self.asteroid_answer)
        return greedy_index, greedy_max

    def calculate_vaporization_order(self, station_coords):
        asteroids_coords_bank = list(self.asteroid_answer.keys())
        asteroids_coords_bank.remove(station_coords)
        ordered_angle_list = []
        for coords in asteroids_coords_bank:
            total_x = coords[0] - station_coords[0]
            total_y = coords[1] - station_coords[1]
            degrees_angle = math.degrees(math.atan2(total_x, total_y))
            line_length_from_origin = math.sqrt(pow(total_x, 2) + pow(total_y, 2))
            ordered_angle_list.append((coords, round(degrees_angle, 3), round(line_length_from_origin, 3)))
        ordered_angle_list.sort(key=itemgetter(1, 2), reverse=True)
        coordinate_bank = []
        current_index = 0
        current_angle = 180
        while True:
            current_angle_coords = list(filter(lambda x: x[1] == current_angle, ordered_angle_list))
            current_angle_coords.sort(key=itemgetter(2), reverse=False)
            coordinate_bank.append(current_angle_coords[0])
            ordered_angle_list.remove(current_angle_coords[0])
            if len(ordered_angle_list) == 1:
                coordinate_bank.append(ordered_angle_list[0])
                ordered_angle_list.remove(ordered_angle_list[0])
                break
            if current_index < len(ordered_angle_list):
                try:
                    current_angle = ordered_angle_list[current_index + len(current_angle_coords) - 1][1]
                    current_index += len(current_angle_coords) - 1
                except IndexError:
                    current_index = 0
                    current_angle = ordered_angle_list[0][1]
            else:
                current_index = 0
                current_angle = ordered_angle_list[0][1]
        for i, point_tuple in enumerate(coordinate_bank):
            print(f'{i+1}\tcoord: {point_tuple[0]}\tangle: {point_tuple[1]}\tlength: {point_tuple[2]}')
            coord = point_tuple[0]
            self.asteroid_map[coord[1]][coord[0]] = str(i + 1)
        for line in self.asteroid_map:
            for c in line:
                str1 = c + (' ' * (3 - len(c)))
                print(f'{str1}', end='')
        print()
        return coordinate_bank[199]
