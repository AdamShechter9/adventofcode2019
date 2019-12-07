

class Day04(object):
    def __init__(self):
        self.data = (248345, 746315)

    def run_solution1(self):
        """
        It is a six-digit number.
        Two adjacent digits are the same (like 22 in 122345).
        Going from left to right, the digits never decrease; they only ever increase or stay the same
        (like 111123 or 135679
        :return:
        """
        valid_count = 0
        for n in range(self.data[0], self.data[1] + 1):
            str_n = str(n)
            if len(str_n) != 6:
                continue
            adjacent_digits = False
            valid_order = True
            for i in range(1, 6):
                if str_n[i - 1] == str_n[i]:
                    adjacent_digits = True
                if str_n[i - 1] > str_n[i]:
                    valid_order = False
                    break
            if not adjacent_digits or not valid_order:
                continue
            print(n)
            valid_count += 1
        print(f'Answer: {valid_count}')
        return valid_count

    def run_solution2(self):
        """
        :return:
        """
        valid_count = 0
        for n in range(self.data[0], self.data[1] + 1):
            str_n = str(n)
            if len(str_n) != 6:
                continue
            adjacent_digits = False
            valid_order = True
            for i in range(1, 6):
                if str_n[i - 1] == str_n[i]:
                    if str_n.count(str_n[i]) == 2:
                        adjacent_digits = True
                if str_n[i - 1] > str_n[i]:
                    valid_order = False
                    break
            if not adjacent_digits or not valid_order:
                continue
            print(n)
            valid_count += 1
        print(f'Answer: {valid_count}')
        return valid_count
