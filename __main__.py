import os
import sys
from day1 import Day01
from day2 import Day02


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
        day1 = Day01(read_file)
        if day_n[-1:] == 'a':
            print(day1.run_solution1())
        elif day_n[-1:] == 'b':
            print(day1.run_solution2())
    elif day_n[:-1] == 'day2':
        day2 = Day02(read_file)
        if day_n[-1:] == 'a':
            print(day2.run_solution1())
        elif day_n[-1:] == 'b':
            print(day2.run_solution2())


if __name__ == '__main__':
    main()
