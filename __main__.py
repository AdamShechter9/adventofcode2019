import os
import sys
from day1 import Day01
from day2 import Day02
from day3 import Day03
from day4 import Day04
from day5 import Day05
from day6 import Day06
from day7 import Day07
from day8 import Day08
from day9 import Day09


def read_file(day_n):
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{day_n}', 'input.txt')
    try:
        with open(file_path, 'r') as f:
            load_data = f.read()
    except FileNotFoundError:
        print('File Not Found!')
        sys.exit(1)
    return load_data


def main():
    day_n = sys.argv[1]
    if day_n[:-1] == 'day1':
        day = Day01(read_file)
    elif day_n[:-1] == 'day2':
        day = Day02(read_file)
    elif day_n[:-1] == 'day3':
        day = Day03(read_file)
    elif day_n[:-1] == 'day4':
        day = Day04()
    elif day_n[:-1] == 'day5':
        day = Day05(read_file)
    elif day_n[:-1] == 'day6':
        day = Day06(read_file)
    elif day_n[:-1] == 'day7':
        day = Day07(read_file)
    elif day_n[:-1] == 'day8':
        day = Day08(read_file)
    elif day_n[:-1] == 'day9':
        day = Day09(read_file)

    if day_n[-1:] == 'a':
        print(day.run_solution1())
    elif day_n[-1:] == 'b':
        print(day.run_solution2())


if __name__ == '__main__':
    main()
