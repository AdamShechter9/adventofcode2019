from functools import reduce


class Day01(object):
    def __init__(self, read_file_fn):
        self.raw_data = read_file_fn('day1').split('\n')
        self.data = [int(x) for x in self.raw_data if len(x) > 0]

    @staticmethod
    def calculate_fuel(x):
        fuel = x // 3 - 2
        return fuel if fuel >= 0 else 0

    def run_solution1(self):
        """
        to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
        :return:
        """
        return reduce(lambda a, b: a + self.calculate_fuel(b), self.data, 0)

    @staticmethod
    def calculate_total_fuel(fuel):
        def recursive_fuel_calc(y):
            if y <= 0:
                return 0
            else:
                calculated_fuel = Day01.calculate_fuel(y)
                return calculated_fuel + recursive_fuel_calc(calculated_fuel)
        return recursive_fuel_calc(fuel)

    def run_solution2(self):
        total_fuel_sum = reduce(lambda a, b: a + self.calculate_total_fuel(b), self.data, 0)
        return total_fuel_sum

    def run_solution1_simple(self):
        """
        to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.
        :return:
        """
        fuel_sum = 0
        for n in self.data:
            fuel_sum += self.calculate_fuel(n)
        return fuel_sum

    def run_solution2_simple(self):
        """
        calculate its fuel and add it to the total. Then, treat the fuel amount you just calculated as the input mass
        and repeat the process, continuing until a fuel requirement is zero or negative.
        :return:
        """
        total_fuel_sum = 0
        for n in self.data:
            module_fuel = 0
            base_fuel = n
            while base_fuel > 0:
                base_fuel = self.calculate_fuel(base_fuel)
                module_fuel += base_fuel
            total_fuel_sum += module_fuel
        return total_fuel_sum
